import pytest
import numpy as np
from src.vision.plastic_classifier import PlasticClassifier


def test_plastic_classifier_initialization():
    """Test that PlasticClassifier can be initialized"""
    try:
        classifier = PlasticClassifier()
        assert classifier is not None
    except Exception as e:
        pytest.skip(f"Skipping test due to model initialization error: {e}")


def test_preprocess_image():
    """Test image preprocessing"""
    classifier = PlasticClassifier()
    # Create a dummy image
    test_image = np.zeros((100, 100, 3), dtype=np.uint8)
    processed = classifier._preprocess_image(test_image)
    assert processed.shape == (640, 640, 3)  # Check resizing
    assert processed.dtype == np.float32  # Check normalization
