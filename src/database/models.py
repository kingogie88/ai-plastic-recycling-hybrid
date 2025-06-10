"""
Database models for AI Circo Recycling System.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime


Base = declarative_base()


class Facility(Base):
    """Processing facility model"""
    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    capacity = Column(Float)  # Tons per day
    created_at = Column(DateTime, default=datetime.utcnow)

    batches = relationship("Batch", back_populates="facility")


class Batch(Base):
    """Processing batch model"""
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True)
    batch_id = Column(String, unique=True, nullable=False)
    facility_id = Column(Integer, ForeignKey("facilities.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    total_items = Column(Integer, default=0)
    total_weight = Column(Float)  # kg

    facility = relationship("Facility", back_populates="batches")
    detections = relationship("PlasticDetection", back_populates="batch")


class PlasticDetection(Base):
    """Individual plastic detection model"""
    __tablename__ = "plastic_detections"

    id = Column(Integer, primary_key=True)
    batch_id = Column(Integer, ForeignKey("batches.id"))
    plastic_type = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    bbox = Column(JSON)  # Bounding box coordinates
    contamination_level = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    batch = relationship("Batch", back_populates="detections")


class ProcessingMetrics(Base):
    """System performance metrics model"""
    __tablename__ = "processing_metrics"

    id = Column(Integer, primary_key=True)
    facility_id = Column(Integer, ForeignKey("facilities.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    throughput = Column(Float)  # Items per minute
    accuracy = Column(Float)  # Detection accuracy
    uptime = Column(Float)  # System uptime percentage
    energy_consumption = Column(Float)  # kWh
    maintenance_status = Column(String)

    facility = relationship("Facility")
