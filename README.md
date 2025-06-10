# AI-Powered Plastic Recycling Hybrid System

An advanced hybrid system that combines computer vision, robotics, and machine learning to automate plastic waste sorting and recycling. The system uses YOLOv11 for plastic type detection, multi-arm robotics for sorting, and provides real-time monitoring and analytics.

## 🎯 Key Features

- Real-time plastic type detection (PET, HDPE, PVC, LDPE, PP, PS)
- Multi-arm robotic sorting with safety controls
- Real-time monitoring with Prometheus & Grafana
- Kubernetes-ready microservices architecture
- Comprehensive testing and security scanning
- Performance metrics and contamination analysis

## 🛠️ Tech Stack

- **Backend**: Python 3.11, FastAPI, Pydantic, SQLAlchemy
- **Vision**: YOLOv11, OpenCV, PyTorch
- **Database**: PostgreSQL, Redis
- **Infrastructure**: Docker, Kubernetes
- **Monitoring**: Prometheus, Grafana
- **CI/CD**: GitHub Actions
- **Security**: JWT, API Keys, SSL/TLS

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- NVIDIA GPU with CUDA support (for vision system)
- Kubernetes cluster (for production deployment)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kingogie88/ai-plastic-recycling-hybrid.git
   cd ai-plastic-recycling-hybrid
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the services:
   ```bash
   docker-compose up -d
   ```

### Running Tests

```bash
# Run all tests with coverage
pytest tests/ --cov=src/ --cov-report=xml -v
```

## 🔒 Security Features

- API key authentication
- SSL/TLS encryption
- Input validation with Pydantic
- Regular security scans (Bandit, Safety, Semgrep)
- Rate limiting
- Secure secrets management

## 📊 Monitoring

Access the monitoring dashboards:
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090

## 🌐 API Documentation

Once running, access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🏗️ Project Structure

```
ai-plastic-recycling-hybrid/
├── src/
│   ├── api/            # FastAPI endpoints
│   ├── vision/         # Plastic detection
│   ├── robotics/       # Robot controller
│   ├── database/       # DB models
│   └── common/         # Shared utilities
├── tests/
│   └── unit/          # Unit tests
├── docker/            # Dockerfiles
├── k8s/               # Kubernetes configs
│   ├── config/        # ConfigMaps
│   ├── secrets/       # Secrets
│   ├── storage/       # PVCs
│   ├── deployments/   # Deployments
│   └── services/      # Services
├── monitoring/        # Prometheus & Grafana
└── .github/
    └── workflows/     # CI/CD pipelines
```

## 🔄 CI/CD Pipeline

The project uses GitHub Actions with:
- Manual trigger workflow
- Environment selection (staging/production)
- Comprehensive testing
- Security scanning
- Docker image building
- Kubernetes deployment

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📞 Support

For support:
1. Check the documentation
2. Search existing issues
3. Open a new issue if needed