"""Schemas for the hospital MCP server."""

from pydantic import BaseModel, Field


class NearbyHospitalToolRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    radius_meters: int = Field(default=5000, gt=0)
    limit: int = Field(default=10, gt=0, le=20)


class NearbyHospitalToolResponse(BaseModel):
    success: bool
    results: list[dict]
