from flask import Flask, request, jsonify
from model import IrisClassifier
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# Initialize the classifier
classifier = IrisClassifier()

# Load the pre-trained model
try:
    classifier.load_model()
    print("Model loaded successfully!")
except FileNotFoundError:
    print("No pre-trained model found. Please train the model first.")
    classifier = None

@app.route('/')
def home():
    return jsonify({
        'message': 'Iris Classification API',
        'endpoints': [
            '/predict - POST: Make predictions',
            '/health - GET: Health check',
            '/info - GET: Model information'
        ]
    })

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'model_loaded': classifier is not None
    })

@app.route('/info')
def model_info():
    if classifier is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    return jsonify({
        'model_type': 'RandomForestClassifier',
        'features': classifier.feature_names,
        'classes': ['setosa', 'versicolor', 'virginica'],
        'description': 'Iris flower classification model'
    })

@app.route('/predict', methods=['POST'])
def predict():
    if classifier is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract features from request
        if 'features' not in data:
            return jsonify({'error': 'Missing features field'}), 400
        
        features = data['features']
        
        # Validate features
        if len(features) != 4:
            return jsonify({'error': 'Expected 4 features (sepal_length, sepal_width, petal_length, petal_width)'}), 400
        
        # Make prediction
        prediction, probability = classifier.predict(features)
        
        # Map prediction to class names
        class_names = ['setosa', 'versicolor', 'virginica']
        predicted_class = class_names[prediction]
        
        return jsonify({
            'prediction': int(prediction),
            'predicted_class': predicted_class,
            'probabilities': {
                'setosa': float(probability[0]),
                'versicolor': float(probability[1]),
                'virginica': float(probability[2])
            },
            'features': features
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/train', methods=['POST'])
def train_model():
    try:
        from model import main
        main()
        
        # Reload the model
        global classifier
        classifier = IrisClassifier()
        classifier.load_model()
        
        return jsonify({
            'message': 'Model trained successfully',
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
