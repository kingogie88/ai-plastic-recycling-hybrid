"""
Vision system for plastic classification.
"""

import cv2
import numpy as np
import torch
from pathlib import Path
from typing import List, Dict, Any
import logging

from src.common.config import settings

logger = logging.getLogger(__name__)


class PlasticClassifier:
    """AI vision system for plastic classification."""

    def __init__(self):
        """Initialize the classifier."""
        self.model = self._load_model()
        self.confidence_threshold = settings.CONFIDENCE_THRESHOLD
        self.class_names = self._load_class_names()

    def _load_model(self) -> torch.nn.Module:
        """Load the YOLO model."""
        try:
            model = torch.hub.load(
                'ultralytics/yolov5',
                'custom',
                path=str(settings.MODEL_PATH)
            )
            model.conf = self.confidence_threshold
            return model
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def _load_class_names(self) -> List[str]:
        """Load class names from model."""
        try:
            return self.model.names
        except Exception as e:
            logger.error(f"Failed to load class names: {e}")
            return []

    def classify_plastic(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        Classify plastic items in image.

        Args:
            image: Input image as numpy array

        Returns:
            List of detections with plastic type and confidence
        """
        try:
            # Run inference
            predictions = self.model(image)

            # Process detections
            detections = []
            for pred in predictions.xyxy[0]:
                x1, y1, x2, y2, conf, cls = pred.tolist()
                if conf >= self.confidence_threshold:
                    detections.append({
                        "plastic_type": self.class_names[int(cls)],
                        "confidence": float(conf),
                        "bbox": [float(x1), float(y1), float(x2), float(y2)]
                    })

            return detections

        except Exception as e:
            logger.error(f"Classification failed: {e}")
            return []

    def get_contamination_level(
        self,
        image: np.ndarray,
        bbox: List[float]
    ) -> float:
        """
        Estimate contamination level of plastic item.

        Args:
            image: Input image
            bbox: Bounding box coordinates [x1, y1, x2, y2]

        Returns:
            Contamination level (0-1)
        """
        try:
            x1, y1, x2, y2 = map(int, bbox)
            roi = image[y1:y2, x1:x2]

            # Convert to grayscale
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

            # Calculate contamination metrics
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            edges = cv2.Canny(blur, 50, 150)

            # Estimate contamination based on edge density
            edge_density = np.sum(edges > 0) / float(edges.size)

            return float(edge_density)

        except Exception as e:
            logger.error(f"Contamination analysis failed: {e}")
            return 0.0

    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for optimal detection

        Args:
            image: Input image

        Returns:
            Preprocessed image
        """
        try:
            # Input validation
            if image is None or image.size == 0:
                raise ValueError("Invalid input image")

            # Resize to model input size
            image = cv2.resize(image, (640, 640))

            # Normalize pixel values
            image = image.astype(np.float32) / 255.0

            # Color space conversion if needed
            if len(image.shape) == 3 and image.shape[2] == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            return image

        except Exception as e:
            logger.error(f"Image preprocessing failed: {e}")
            raise

    def _assess_contamination(self, image: np.ndarray, bbox: List[float]) -> float:
        """
        Assess contamination level of detected plastic

        Args:
            image: Original image
            bbox: Bounding box coordinates [x1, y1, x2, y2]

        Returns:
            Contamination score between 0 and 1
        """
        try:
            x1, y1, x2, y2 = map(int, bbox)
            roi = image[y1:y2, x1:x2]

            # Simple contamination assessment based on color variance
            if roi.size > 0:
                hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                contamination_score = np.std(hsv) / 255.0
                return min(contamination_score, 1.0)

            return 0.0

        except Exception as e:
            logger.error(f"Contamination assessment failed: {e}")
            return 0.0

    def train_model(self, train_data_path: str, epochs: int = 100) -> bool:
        """
        Train or fine-tune the model on custom data

        Args:
            train_data_path: Path to training data directory
            epochs: Number of training epochs

        Returns:
            Training success status
        """
        try:
            # Validate training data path
            if not Path(train_data_path).exists():
                raise ValueError(
                    f"Training data path does not exist: {train_data_path}"
                )

            # Configure training parameters
            training_args = {
                "data": train_data_path,
                "epochs": epochs,
                "imgsz": 640,
                "batch": 16,
                "device": "cuda:0" if torch.cuda.is_available() else "cpu",
            }

            # Start training
            logger.info(f"Starting model training for {epochs} epochs...")
            results = self.model.train(**training_args)

            # Save trained model
            self.model.save("models/plastic_yolo11_trained.pt")

            return True

        except Exception as e:
            logger.error(f"Model training failed: {e}")
            return False


if __name__ == "__main__":
    # Example usage
    classifier = PlasticClassifier()

    # Test on sample image
    test_image = cv2.imread("test_plastic.jpg")
    if test_image is not None:
        results = classifier.classify_plastic(test_image)
        for detection in results:
            print(
                f"Found {detection['plastic_type']} with {detection['confidence']:.2f} confidence"
            )
