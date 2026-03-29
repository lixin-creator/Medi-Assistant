"""
MediAssistant - schemas/hospital.py
Pydantic schemas for nearby hospital search.
"""

from typing import Optional

from pydantic import BaseModel, Field


class NearbyHospitalRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    radius_meters: int = Field(default=5000, gt=0)
    limit: int = Field(default=10, gt=0, le=20)


class HospitalItem(BaseModel):
    id: str
    name: str
    level: str
    is_tertiary_a: bool = False
    distance_meters: int
    distance_text: str
    address: str
    phone: Optional[str] = None
    latitude: float
    longitude: float
    navigation_url: Optional[str] = None


class NearbyHospitalResponse(BaseModel):
    success: bool
    hospitals: list[HospitalItem]
