"""
Unit tests for robot controller.
"""

import pytest
from unittest.mock import Mock, patch
import threading
import time

from src.robotics.robot_controller import MultiArmController


@pytest.fixture
def controller():
    """Create a robot controller instance."""
    return MultiArmController()


def test_controller_initialization(controller):
    """Test controller initialization."""
    assert controller.max_workers > 0
    assert not controller.emergency_stop
    assert not controller.running
    assert isinstance(controller.lock, threading.Lock)


@pytest.mark.asyncio
async def test_pick_and_sort_empty_detections(controller):
    """Test pick and sort with empty detections."""
    result = await controller.pick_and_sort([])
    assert not result


@pytest.mark.asyncio
async def test_pick_and_sort_valid_detections(controller):
    """Test pick and sort with valid detections."""
    detections = [
        {
            "plastic_type": "PET",
            "confidence": 0.95,
            "bbox": [100, 100, 200, 200]
        },
        {
            "plastic_type": "HDPE",
            "confidence": 0.90,
            "bbox": [300, 300, 400, 400]
        }
    ]

    result = await controller.pick_and_sort(detections)
    assert result


@pytest.mark.asyncio
async def test_pick_and_sort_emergency_stop(controller):
    """Test pick and sort with emergency stop."""
    detections = [
        {
            "plastic_type": "PET",
            "confidence": 0.95,
            "bbox": [100, 100, 200, 200]
        }
    ]

    # Activate emergency stop
    controller.stop()
    result = await controller.pick_and_sort(detections)
    assert not result


def test_emergency_stop(controller):
    """Test emergency stop functionality."""
    assert not controller.emergency_stop
    assert not controller.running

    # Start controller
    controller.reset()
    assert not controller.emergency_stop
    assert controller.running

    # Stop controller
    controller.stop()
    assert controller.emergency_stop
    assert not controller.running


def test_concurrent_sorting(controller):
    """Test concurrent sorting operations."""
    detections = [
        {"plastic_type": "PET", "confidence": 0.95, "bbox": [100, 100, 200, 200]}
        for _ in range(10)
    ]

    start_time = time.time()
    result = controller.pick_and_sort(detections)
    end_time = time.time()

    # Should take less time than sequential processing
    assert end_time - start_time < len(detections) * 0.5  # Each sort takes 0.5s
    assert result


def test_sort_item_success(controller):
    """Test successful item sorting."""
    detection = {
        "plastic_type": "PET",
        "confidence": 0.95,
        "bbox": [100, 100, 200, 200]
    }

    # Should not raise any exceptions
    controller._sort_item(detection)


def test_sort_item_emergency_stop(controller):
    """Test item sorting during emergency stop."""
    detection = {
        "plastic_type": "PET",
        "confidence": 0.95,
        "bbox": [100, 100, 200, 200]
    }

    controller.stop()
    with pytest.raises(Exception) as exc_info:
        controller._sort_item(detection)
    assert "Emergency stop activated" in str(exc_info.value)


def test_controller_thread_safety(controller):
    """Test thread safety of controller operations."""
    def worker():
        controller._sort_item({
            "plastic_type": "PET",
            "confidence": 0.95,
            "bbox": [100, 100, 200, 200]
        })

    threads = []
    for _ in range(10):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    # Stop controller while threads are running
    time.sleep(0.1)
    controller.stop()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    assert controller.emergency_stop
    assert not controller.running 