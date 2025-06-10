"""
API schemas and documentation.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class PlasticDetection(BaseModel):
    """Schema for plastic detection results."""

    plastic_type: str = Field(
        ...,
        description="Type of plastic detected (PET, HDPE, etc.)",
        example="PET"
    )
    confidence: float = Field(
        ...,
        description="Detection confidence score (0-1)",
        ge=0,
        le=1,
        example=0.95
    )
    bbox: List[float] = Field(
        ...,
        description="Bounding box coordinates [x1, y1, x2, y2]",
        min_items=4,
        max_items=4,
        example=[100, 100, 200, 200]
    )
    contamination_level: Optional[float] = Field(
        None,
        description="Estimated contamination level (0-1)",
        ge=0,
        le=1,
        example=0.1
    )


class ProcessBatchRequest(BaseModel):
    """Request model for batch processing."""

    image_data: str = Field(
        ...,
        description="Base64 encoded image data",
        example="data:image/jpeg;base64,/9j/4AAQSkZJRg..."
    )
    facility_id: str = Field(
        ...,
        description="Unique identifier for the processing facility",
        example="facility_001"
    )
    batch_id: Optional[str] = Field(
        None,
        description="Optional batch identifier",
        example="batch_001"
    )


class ProcessBatchResponse(BaseModel):
    """Response model for batch processing."""

    message: str = Field(
        ...,
        description="Processing status message",
        example="Processing 5 plastic items"
    )
    batch_id: str = Field(
        ...,
        description="Unique batch identifier",
        example="batch_001"
    )
    detections: List[PlasticDetection] = Field(
        ...,
        description="List of plastic detections"
    )
    timestamp: datetime = Field(
        ...,
        description="Processing timestamp"
    )
    facility_id: str = Field(
        ...,
        description="Processing facility identifier",
        example="facility_001"
    )


class FacilityCreate(BaseModel):
    """Schema for creating a new facility."""

    name: str = Field(
        ...,
        description="Facility name",
        example="Recycling Center North"
    )
    location: str = Field(
        ...,
        description="Facility location",
        example="123 Green Street, Eco City"
    )
    capacity: float = Field(
        ...,
        description="Processing capacity in tons per day",
        gt=0,
        example=100.0
    )


class FacilityResponse(FacilityCreate):
    """Schema for facility response."""

    id: int = Field(..., description="Facility ID")
    created_at: datetime = Field(..., description="Creation timestamp")


class ProcessingMetricsCreate(BaseModel):
    """Schema for creating processing metrics."""

    facility_id: int = Field(
        ...,
        description="Facility ID",
        example=1
    )
    throughput: float = Field(
        ...,
        description="Items processed per minute",
        ge=0,
        example=100.0
    )
    accuracy: float = Field(
        ...,
        description="Detection accuracy (0-1)",
        ge=0,
        le=1,
        example=0.95
    )
    uptime: float = Field(
        ...,
        description="System uptime percentage (0-1)",
        ge=0,
        le=1,
        example=0.99
    )
    energy_consumption: float = Field(
        ...,
        description="Energy consumption in kWh",
        ge=0,
        example=50.5
    )
    maintenance_status: str = Field(
        ...,
        description="System maintenance status",
        example="operational"
    )


class ProcessingMetricsResponse(ProcessingMetricsCreate):
    """Schema for processing metrics response."""

    id: int = Field(..., description="Metrics record ID")
    timestamp: datetime = Field(..., description="Recording timestamp")


class ErrorResponse(BaseModel):
    """Schema for error responses."""

    detail: str = Field(
        ...,
        description="Error message",
        example="Invalid input data"
    ) 