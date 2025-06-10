"""
Unit tests for vision system.
"""

import pytest
import numpy as np
import cv2
from unittest.mock import Mock, patch

from src.vision.plastic_classifier import PlasticClassifier


@pytest.fixture
def mock_model():
    """Create a mock YOLO model."""
    model = Mock()
    model.names = ["PET", "HDPE", "PVC", "LDPE", "PP", "PS", "OTHER"]
    return model


@pytest.fixture
def classifier(mock_model):
    """Create a PlasticClassifier instance with mocked model."""
    with patch('src.vision.plastic_classifier.PlasticClassifier._load_model') as mock_load:
        mock_load.return_value = mock_model
        classifier = PlasticClassifier()
        return classifier


def test_classifier_initialization(classifier):
    """Test classifier initialization."""
    assert classifier.confidence_threshold == 0.85
    assert len(classifier.class_names) == 7
    assert "PET" in classifier.class_names


def test_classify_plastic_valid_image(classifier, mock_model):
    """Test plastic classification with valid image."""
    # Create test image
    image = np.zeros((640, 640, 3), dtype=np.uint8)
    cv2.rectangle(image, (100, 100), (200, 200), (255, 255, 255), -1)

    # Mock model predictions
    mock_predictions = Mock()
    mock_predictions.xyxy = [np.array([[100, 100, 200, 200, 0.95, 0]])]
    mock_model.return_value = mock_predictions

    # Run classification
    detections = classifier.classify_plastic(image)

    assert len(detections) == 1
    assert detections[0]["plastic_type"] == "PET"
    assert detections[0]["confidence"] == pytest.approx(0.95)
    assert len(detections[0]["bbox"]) == 4


def test_classify_plastic_no_detections(classifier, mock_model):
    """Test classification with no detections."""
    image = np.zeros((640, 640, 3), dtype=np.uint8)
    
    # Mock empty predictions
    mock_predictions = Mock()
    mock_predictions.xyxy = [np.array([])]
    mock_model.return_value = mock_predictions

    detections = classifier.classify_plastic(image)
    assert len(detections) == 0


def test_classify_plastic_low_confidence(classifier, mock_model):
    """Test classification with low confidence detections."""
    image = np.zeros((640, 640, 3), dtype=np.uint8)

    # Mock low confidence predictions
    mock_predictions = Mock()
    mock_predictions.xyxy = [np.array([[100, 100, 200, 200, 0.5, 0]])]
    mock_model.return_value = mock_predictions

    detections = classifier.classify_plastic(image)
    assert len(detections) == 0


def test_get_contamination_level(classifier):
    """Test contamination level estimation."""
    # Create test image with some "contamination"
    image = np.zeros((640, 640, 3), dtype=np.uint8)
    cv2.circle(image, (150, 150), 50, (255, 255, 255), -1)
    bbox = [100, 100, 200, 200]

    contamination = classifier.get_contamination_level(image, bbox)
    assert 0 <= contamination <= 1


def test_get_contamination_level_invalid_bbox(classifier):
    """Test contamination level with invalid bbox."""
    image = np.zeros((640, 640, 3), dtype=np.uint8)
    bbox = [0, 0, 1000, 1000]  # Invalid bbox

    contamination = classifier.get_contamination_level(image, bbox)
    assert contamination == 0.0


@pytest.mark.parametrize("image_shape", [
    (100, 100, 3),
    (640, 480, 3),
    (1920, 1080, 3)
])
def test_classify_plastic_different_sizes(classifier, mock_model, image_shape):
    """Test classification with different image sizes."""
    image = np.zeros(image_shape, dtype=np.uint8)
    
    # Mock predictions
    mock_predictions = Mock()
    mock_predictions.xyxy = [np.array([[10, 10, 20, 20, 0.95, 0]])]
    mock_model.return_value = mock_predictions

    detections = classifier.classify_plastic(image)
    assert len(detections) == 1 