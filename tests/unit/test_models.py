"""
Unit tests for database models.
"""

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.database.models import Base, Facility, Batch, PlasticDetection, ProcessingMetrics


@pytest.fixture(scope="function")
def engine():
    """Create test database engine."""
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="function")
def session(engine):
    """Create test database session."""
    Base.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()
    Base.metadata.drop_all(engine)


def test_facility_creation(session):
    """Test creating a facility."""
    facility = Facility(
        name="Test Facility",
        location="Test Location",
        capacity=100.0
    )
    session.add(facility)
    session.commit()

    saved_facility = session.query(Facility).first()
    assert saved_facility.name == "Test Facility"
    assert saved_facility.location == "Test Location"
    assert saved_facility.capacity == 100.0
    assert isinstance(saved_facility.created_at, datetime)


def test_batch_creation(session):
    """Test creating a batch."""
    facility = Facility(name="Test Facility", location="Test Location")
    session.add(facility)
    session.commit()

    batch = Batch(
        batch_id="BATCH001",
        facility_id=facility.id,
        total_items=10,
        total_weight=5.5
    )
    session.add(batch)
    session.commit()

    saved_batch = session.query(Batch).first()
    assert saved_batch.batch_id == "BATCH001"
    assert saved_batch.facility_id == facility.id
    assert saved_batch.total_items == 10
    assert saved_batch.total_weight == 5.5
    assert isinstance(saved_batch.timestamp, datetime)


def test_plastic_detection_creation(session):
    """Test creating a plastic detection."""
    facility = Facility(name="Test Facility", location="Test Location")
    session.add(facility)
    session.commit()

    batch = Batch(batch_id="BATCH001", facility_id=facility.id)
    session.add(batch)
    session.commit()

    detection = PlasticDetection(
        batch_id=batch.id,
        plastic_type="PET",
        confidence=0.95,
        bbox={"x1": 100, "y1": 100, "x2": 200, "y2": 200},
        contamination_level=0.1
    )
    session.add(detection)
    session.commit()

    saved_detection = session.query(PlasticDetection).first()
    assert saved_detection.plastic_type == "PET"
    assert saved_detection.confidence == 0.95
    assert saved_detection.bbox == {"x1": 100, "y1": 100, "x2": 200, "y2": 200}
    assert saved_detection.contamination_level == 0.1
    assert isinstance(saved_detection.timestamp, datetime)


def test_processing_metrics_creation(session):
    """Test creating processing metrics."""
    facility = Facility(name="Test Facility", location="Test Location")
    session.add(facility)
    session.commit()

    metrics = ProcessingMetrics(
        facility_id=facility.id,
        throughput=100.0,
        accuracy=0.95,
        uptime=0.99,
        energy_consumption=50.5,
        maintenance_status="operational"
    )
    session.add(metrics)
    session.commit()

    saved_metrics = session.query(ProcessingMetrics).first()
    assert saved_metrics.facility_id == facility.id
    assert saved_metrics.throughput == 100.0
    assert saved_metrics.accuracy == 0.95
    assert saved_metrics.uptime == 0.99
    assert saved_metrics.energy_consumption == 50.5
    assert saved_metrics.maintenance_status == "operational"
    assert isinstance(saved_metrics.timestamp, datetime)


def test_facility_batch_relationship(session):
    """Test relationship between facility and batches."""
    facility = Facility(name="Test Facility", location="Test Location")
    session.add(facility)
    session.commit()

    batch1 = Batch(batch_id="BATCH001", facility_id=facility.id)
    batch2 = Batch(batch_id="BATCH002", facility_id=facility.id)
    session.add_all([batch1, batch2])
    session.commit()

    saved_facility = session.query(Facility).first()
    assert len(saved_facility.batches) == 2
    assert saved_facility.batches[0].batch_id == "BATCH001"
    assert saved_facility.batches[1].batch_id == "BATCH002"


def test_batch_detection_relationship(session):
    """Test relationship between batch and detections."""
    facility = Facility(name="Test Facility", location="Test Location")
    session.add(facility)
    session.commit()

    batch = Batch(batch_id="BATCH001", facility_id=facility.id)
    session.add(batch)
    session.commit()

    detection1 = PlasticDetection(
        batch_id=batch.id,
        plastic_type="PET",
        confidence=0.95
    )
    detection2 = PlasticDetection(
        batch_id=batch.id,
        plastic_type="HDPE",
        confidence=0.90
    )
    session.add_all([detection1, detection2])
    session.commit()

    saved_batch = session.query(Batch).first()
    assert len(saved_batch.detections) == 2
    assert saved_batch.detections[0].plastic_type == "PET"
    assert saved_batch.detections[1].plastic_type == "HDPE" 