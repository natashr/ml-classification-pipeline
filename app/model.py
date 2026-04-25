import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
import pickle
import os

class IrisClassifier:
    def __init__(self):
        self.model = None
        self.feature_names = None
        
    def load_data(self):
        """Load and prepare the iris dataset"""
        iris = load_iris()
        X = pd.DataFrame(iris.data, columns=iris.feature_names)
        y = pd.Series(iris.target)
        self.feature_names = iris.feature_names
        return X, y
    
    def train(self, X, y, test_size=0.2, random_state=42):
        """Train the Random Forest classifier"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        self.model = RandomForestClassifier(
            n_estimators=100, 
            random_state=random_state
        )
        self.model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        return accuracy, report, X_test, y_test
    
    def predict(self, features):
        """Make predictions on new data"""
        if self.model is None:
            raise ValueError("Model not trained yet!")
        
        # Ensure features is a DataFrame with correct column names
        if isinstance(features, (list, np.ndarray)):
            features = pd.DataFrame([features], columns=self.feature_names)
        
        prediction = self.model.predict(features)
        probability = self.model.predict_proba(features)
        
        return prediction[0], probability[0]
    
    def save_model(self, filepath="model.pkl"):
        """Save the trained model"""
        if self.model is None:
            raise ValueError("No model to save!")
        
        with open(filepath, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'feature_names': self.feature_names
            }, f)
    
    def load_model(self, filepath="model.pkl"):
        """Load a trained model"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file {filepath} not found!")
        
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.feature_names = data['feature_names']

def main():
    """Main function to train and evaluate the model"""
    classifier = IrisClassifier()
    
    # Load data
    print("Loading iris dataset...")
    X, y = classifier.load_data()
    
    # Train model
    print("Training Random Forest classifier...")
    accuracy, report, X_test, y_test = classifier.train(X, y)
    
    print(f"Model Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(report)
    
    # Save model
    classifier.save_model()
    print("Model saved as 'model.pkl'")
    
    # Test with a sample prediction
    sample_features = X_test.iloc[0].values
    prediction, probability = classifier.predict(sample_features)
    
    print(f"\nSample Prediction:")
    print(f"Features: {sample_features}")
    print(f"Predicted Class: {prediction}")
    print(f"Class Probabilities: {probability}")

if __name__ == "__main__":
    main()
