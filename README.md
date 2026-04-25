# ML Classification Pipeline

A complete machine learning pipeline that trains an Iris classification model, containerizes it with Docker, and deploys to Docker Desktop using GitHub Actions and Terraform.

## 🚀 Features

- **ML Model**: Random Forest classifier for Iris flower classification
- **REST API**: Flask-based API with prediction endpoints
- **Containerization**: Docker image with health checks
- **CI/CD**: GitHub Actions for automated building and deployment
- **Infrastructure as Code**: Terraform for Docker Desktop deployment
- **Automated Testing**: Health checks and API validation

## 📁 Project Structure

```
ml-classification-pipeline/
├── app/
│   ├── model.py          # ML model training and prediction logic
│   └── api.py            # Flask REST API
├── terraform/
│   ├── main.tf           # Main Terraform configuration
│   ├── variables.tf      # Input variables
│   └── outputs.tf        # Output definitions
├── .github/
│   └── workflows/
│       ├── docker-ci.yml        # Docker build and push workflow
│       └── terraform-deploy.yml # Terraform deployment workflow
├── Dockerfile              # Docker image configuration
├── requirements.txt        # Python dependencies
├── .dockerignore          # Docker ignore file
└── README.md              # This file
```

## 🛠️ Prerequisites

- Docker Desktop installed and running
- Terraform installed locally (for manual deployment)
- GitHub account with repository access
- Docker Hub account

## 🐳 Local Development

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd ml-classification-pipeline
```

### 2. Build and Run Locally

```bash
# Build the Docker image
docker build -t ml-iris-classifier .

# Run the container
docker run -p 5000:5000 --name ml-classifier ml-iris-classifier
```

### 3. Test the API

```bash
# Health check
curl http://localhost:5000/health

# Model info
curl http://localhost:5000/info

# Make a prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [5.1, 3.5, 1.4, 0.2]
  }'
```

## 🚀 Deployment Pipeline

### Step 1: Configure GitHub Secrets

Add these secrets to your GitHub repository:

- `DOCKER_HUB_USERNAME`: Your Docker Hub username
- `DOCKER_HUB_TOKEN`: Your Docker Hub access token

### Step 2: Update Terraform Configuration

Edit `terraform/main.tf` and update the `docker_image` variable:

```hcl
variable "docker_image" {
  default = "your-dockerhub-username/ml-iris-classifier:latest"
}
```

### Step 3: Push to GitHub

```bash
git add .
git commit -m "Add ML classification pipeline"
git push origin main
```

### Step 4: Automated Deployment

1. **Docker Build**: GitHub Actions builds and pushes the Docker image to Docker Hub
2. **Terraform Deploy**: Automatically triggers deployment to Docker Desktop
3. **Health Check**: Validates the deployed API

## 📊 API Endpoints

### GET `/`
Returns API information and available endpoints.

### GET `/health`
Health check endpoint. Returns service status and model loading state.

### GET `/info`
Returns model information including features and classes.

### POST `/predict`
Makes predictions on input features.

**Request Body:**
```json
{
  "features": [5.1, 3.5, 1.4, 0.2]
}
```

**Response:**
```json
{
  "prediction": 0,
  "predicted_class": "setosa",
  "probabilities": {
    "setosa": 0.95,
    "versicolor": 0.04,
    "virginica": 0.01
  },
  "features": [5.1, 3.5, 1.4, 0.2]
}
```

### POST `/train`
Trains the model from scratch (for development/testing).

## 🔧 Manual Terraform Deployment

If you want to deploy manually:

```bash
cd terraform

# Initialize Terraform
terraform init

# Plan the deployment
terraform plan -var="docker_image=your-username/ml-iris-classifier:latest"

# Apply the configuration
terraform apply -auto-approve
```

## 🧪 Testing

### Run Tests Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Test model import
python -c "from app.model import IrisClassifier; print('Model test passed')"

# Test API import
python -c "from app.api import app; print('API test passed')"
```

### Test Deployed Service

```bash
# Check service health
curl http://localhost:5000/health

# Test prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [6.0, 3.0, 4.8, 1.8]}'
```

## 📈 Model Details

- **Algorithm**: Random Forest Classifier
- **Dataset**: Iris (150 samples, 4 features)
- **Classes**: Setosa, Versicolor, Virginica
- **Features**: Sepal Length, Sepal Width, Petal Length, Petal Width
- **Accuracy**: ~96% on test set

## 🔒 Security Considerations

- Container runs as non-root user
- Input validation on API endpoints
- Health checks for container monitoring
- No sensitive data in container images

## 🐛 Troubleshooting

### Common Issues

1. **Docker Desktop not running**: Ensure Docker Desktop is started
2. **Port conflicts**: Change host port in Terraform variables
3. **Image pull failures**: Check Docker Hub credentials in GitHub secrets
4. **Container not starting**: Check logs with `docker logs ml-iris-classifier`

### Debug Commands

```bash
# Check container status
docker ps

# View container logs
docker logs ml-iris-classifier

# Access container shell
docker exec -it ml-iris-classifier /bin/bash

# Stop and remove container
docker stop ml-iris-classifier
docker rm ml-iris-classifier
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🔗 Resources

- [Docker Documentation](https://docs.docker.com/)
- [Terraform Docker Provider](https://registry.terraform.io/providers/kreuzwerker/docker/latest)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
