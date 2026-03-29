import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from mcp_servers.hospital_server.matchers.tertiary_matcher import (  # noqa: E402
    match_tertiary_a_hospital,
)
from mcp_servers.hospital_server.providers.amap_provider import AMapHospitalProvider  # noqa: E402


class MockResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError('http error')


def test_amap_provider_returns_hospital_results():
    provider = AMapHospitalProvider(api_key='test-key')

    with patch('mcp_servers.hospital_server.providers.amap_provider.httpx.get') as mock_get:
        mock_get.side_effect = [
            MockResponse({'status': '1', 'locations': '121.4737,31.2304'}),
            MockResponse(
                {
                    'status': '1',
                    'pois': [
                        {
                            'id': 'B001',
                            'name': '上海市第一人民医院',
                            'type': '医疗保健服务;综合医院',
                            'address': '武进路85号',
                            'cityname': '上海市',
                            'adname': '虹口区',
                            'distance': '530',
                            'location': '121.4900,31.2500',
                            'business': {'tel': '021-63240090'},
                        }
                    ],
                }
            ),
        ]

        results = provider.search_nearby_hospitals(31.2304, 121.4737, 5000, 5)

    assert len(results) == 1
    assert results[0]['name'] == '上海市第一人民医院'
    assert results[0]['distance_meters'] == 530
    assert '虹口区' in results[0]['address']


def test_amap_provider_marks_tertiary_a_hospital():
    provider = AMapHospitalProvider(api_key='test-key')

    with patch('mcp_servers.hospital_server.providers.amap_provider.httpx.get') as mock_get:
        mock_get.side_effect = [
            MockResponse({'status': '1', 'locations': '121.4737,31.2304'}),
            MockResponse(
                {
                    'status': '1',
                    'pois': [
                        {
                            'id': 'B002',
                            'name': '复旦大学附属中山医院',
                            'type': '医疗保健服务;综合医院',
                            'address': '枫林路180号',
                            'cityname': '上海市',
                            'adname': '徐汇区',
                            'distance': '1200',
                            'location': '121.4368,31.2050',
                            'business': {'tel': '021-64041990'},
                        }
                    ],
                }
            ),
        ]

        results = provider.search_nearby_hospitals(31.2304, 121.4737, 5000, 5)

    assert results[0]['is_tertiary_a'] is True
    assert results[0]['tertiary_label'] == '三甲医院'


def test_tertiary_matcher_supports_new_major_city_hospital():
    matched_item = match_tertiary_a_hospital(
        '北京大学深圳医院',
        '深圳市',
        '广东省深圳市福田区莲花路1120号',
    )

    assert matched_item is not None
    assert matched_item['canonical_name'] == '北京大学深圳医院'
    assert matched_item['is_tertiary_a'] is True


def test_tertiary_matcher_supports_chongqing_main_urban_hospital():
    matched_item = match_tertiary_a_hospital(
        '重庆大学附属肿瘤医院',
        '重庆市',
        '重庆市沙坪坝区汉渝路181号',
    )

    assert matched_item is not None
    assert matched_item['canonical_name'] == '重庆大学附属肿瘤医院'
    assert matched_item['is_tertiary_a'] is True
