# AI Models Directory

This directory contains the machine learning models used by the AI Plastic Recycling system.

## Required Models

1. `plastic_yolo11.pt` - YOLOv8 model for plastic type detection
   - Size: ~150MB
   - Format: PyTorch
   - Resolution: 640x640
   - Classes: 7 (PET, HDPE, PVC, LDPE, PP, PS, OTHER)

## Obtaining the Models

### Option 1: Automatic Download

Run the provided download script:

```bash
python download_models.py
```

This will download all required models from our secure storage and verify their checksums.

### Option 2: Manual Download

1. Download the models from our secure storage:
   - Development models: [https://dev-models.recycling-ai.com](https://dev-models.recycling-ai.com)
   - Production models: Request access from the system administrator

2. Place the downloaded models in this directory.

3. Verify the checksums:
   ```bash
   sha256sum -c checksums.txt
   ```

## Model Versioning

- Models are versioned using semantic versioning (MAJOR.MINOR.PATCH)
- The current production version is stored in `version.txt`
- Model updates are announced in the #model-updates Slack channel

## Custom Training

If you need to train custom models:

1. Follow the training instructions in `/docs/training/README.md`
2. Use the training scripts in `/src/training/`
3. Save your models in this directory with appropriate versioning

## Performance Metrics

Current model performance metrics:
- Accuracy: 95.8%
- Inference time: 45ms (GPU), 150ms (CPU)
- Memory usage: 2.1GB (GPU), 4GB (CPU) 