import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.hospital_client import HospitalClient  # noqa: E402


class MockResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError('http error')


def test_hospital_client_calls_mcp_server_and_returns_results():
    client = HospitalClient(server_url='http://127.0.0.1:8090')

    with patch('app.tools.hospital_client.httpx.post') as mock_post:
        mock_post.return_value = MockResponse(
            {
                'success': True,
                'results': [
                    {
                        'id': 'B001',
                        'name': '上海交通大学医学院附属瑞金医院',
                        'type': '医疗保健服务;综合医院',
                        'distance_meters': 680,
                        'address': '上海市黄浦区瑞金二路197号',
                        'phone': '021-64370045',
                        'latitude': 31.2143,
                        'longitude': 121.4681,
                        'navigation_url': 'https://uri.amap.com/navigation?...',
                    }
                ],
            }
        )

        results = client.search_nearby_hospitals(31.2304, 121.4737, 5000, 5)

    _, kwargs = mock_post.call_args
    assert kwargs.get('trust_env') is False
    assert len(results) == 1
    assert results[0]['name'] == '上海交通大学医学院附属瑞金医院'
    assert results[0]['distance_meters'] == 680
    assert '黄浦区' in results[0]['address']
    assert results[0]['phone'] == '021-64370045'


def test_hospital_client_respects_result_limit():
    client = HospitalClient(server_url='http://127.0.0.1:8090')

    with patch('app.tools.hospital_client.httpx.post') as mock_post:
        mock_post.return_value = MockResponse(
            {
                'success': True,
                'results': [
                    {'id': 'B001', 'name': '医院1', 'distance_meters': 200},
                ],
            }
        )

        results = client.search_nearby_hospitals(31.2304, 121.4737, 5000, 1)

    assert len(results) == 1


def test_hospital_client_raises_when_mcp_server_fails():
    client = HospitalClient(server_url='http://127.0.0.1:8090')

    with patch('app.tools.hospital_client.httpx.post') as mock_post:
        mock_post.return_value = MockResponse({'success': False}, status_code=200)

        try:
            client.search_nearby_hospitals(31.2304, 121.4737, 5000, 5)
        except RuntimeError as exc:
            assert 'MCP' in str(exc)
        else:
            raise AssertionError('Expected RuntimeError to be raised')
