import os
import sys
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.hospital_service import (  # noqa: E402
    HospitalService,
    format_distance,
    normalize_hospital_level,
)


def test_normalize_hospital_level_maps_known_values():
    assert normalize_hospital_level('三甲医院') == '三甲医院'
    assert normalize_hospital_level('综合医院') == '综合医院'
    assert normalize_hospital_level(None) == '未标注'


def test_format_distance_returns_human_readable_text():
    assert format_distance(350) == '350 m'
    assert format_distance(1200) == '1.2 km'
    assert format_distance(None) == '未知距离'


def test_hospital_service_returns_stable_hospital_shape():
    client = MagicMock()
    client.search_nearby_hospitals.return_value = [
        {
            'id': 'hospital_001',
            'name': '上海市第一人民医院',
            'level': '',
            'is_tertiary_a': True,
            'tertiary_label': '三甲医院',
            'distance_meters': 820,
            'address': '上海市虹口区武进路85号',
            'phone': '021-12345678',
            'latitude': 31.25,
            'longitude': 121.49,
            'navigation_url': 'https://example.com/nav',
        }
    ]

    service = HospitalService(client=client)
    result = service.search_nearby(31.23, 121.47, 5000, 10)

    assert len(result) == 1
    assert result[0]['name'] == '上海市第一人民医院'
    assert result[0]['level'] == '三甲医院'
    assert result[0]['is_tertiary_a'] is True
    assert result[0]['distance_text'] == '820 m'


def test_hospital_service_handles_empty_results():
    client = MagicMock()
    client.search_nearby_hospitals.return_value = []

    service = HospitalService(client=client)

    assert service.search_nearby(31.23, 121.47, 5000, 10) == []
