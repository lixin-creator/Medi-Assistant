"""
MediAssistant - api/v1/endpoints/hospital.py
Nearby hospital search endpoint.
"""

from fastapi import APIRouter, HTTPException

from app.schemas.hospital import NearbyHospitalRequest, NearbyHospitalResponse
from app.services.hospital_service import HospitalService
from app.tools.hospital_client import get_hospital_client

router = APIRouter(tags=['Hospital'])

hospital_service = HospitalService(client=get_hospital_client())


@router.post('/hospitals/nearby', response_model=NearbyHospitalResponse)
async def nearby_hospital_endpoint(request: NearbyHospitalRequest):
    try:
        hospitals = hospital_service.search_nearby(
            request.latitude,
            request.longitude,
            request.radius_meters,
            request.limit,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail='Hospital search service unavailable',
        ) from exc

    return NearbyHospitalResponse(success=True, hospitals=hospitals)
