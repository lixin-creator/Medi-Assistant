import os
import sys

import pytest
from pydantic import ValidationError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.schemas.hospital import (  # noqa: E402
    HospitalItem,
    NearbyHospitalRequest,
    NearbyHospitalResponse,
)


def test_nearby_hospital_request_accepts_valid_values():
    request = NearbyHospitalRequest(
        latitude=31.2304,
        longitude=121.4737,
        radius_meters=5000,
        limit=10,
    )

    assert request.latitude == 31.2304
    assert request.longitude == 121.4737
    assert request.radius_meters == 5000
    assert request.limit == 10


@pytest.mark.parametrize(
    ('field_name', 'value'),
    [
        ('latitude', 91),
        ('latitude', -91),
        ('longitude', 181),
        ('longitude', -181),
    ],
)
def test_nearby_hospital_request_rejects_invalid_coordinates(field_name, value):
    payload = {
        'latitude': 31.2304,
        'longitude': 121.4737,
        'radius_meters': 5000,
        'limit': 10,
    }
    payload[field_name] = value

    with pytest.raises(ValidationError):
        NearbyHospitalRequest(**payload)


def test_nearby_hospital_response_serializes_hospital_items():
    response = NearbyHospitalResponse(
        success=True,
        hospitals=[
            HospitalItem(
                id='hospital_001',
                name='复旦大学附属中山医院',
                level='三级甲等',
                distance_meters=1200,
                distance_text='1.2 km',
                address='上海市徐汇区枫林路180号',
                phone='021-12345678',
                latitude=31.2,
                longitude=121.4,
                navigation_url='https://example.com/nav',
            )
        ],
    )

    data = response.model_dump()

    assert data['success'] is True
    assert len(data['hospitals']) == 1
    assert data['hospitals'][0]['level'] == '三级甲等'
    assert data['hospitals'][0]['distance_text'] == '1.2 km'
