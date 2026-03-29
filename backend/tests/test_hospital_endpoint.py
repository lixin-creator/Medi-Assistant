from unittest.mock import patch


def test_nearby_hospital_endpoint_returns_results(test_client):
    with patch('app.api.v1.endpoints.hospital.hospital_service') as mock_service:
        mock_service.search_nearby.return_value = [
            {
                'id': 'hospital_001',
                'name': '上海交通大学医学院附属瑞金医院',
                'level': '三级甲等',
                'distance_meters': 600,
                'distance_text': '600 m',
                'address': '上海市黄浦区瑞金二路197号',
                'phone': '021-12345678',
                'latitude': 31.2,
                'longitude': 121.4,
                'navigation_url': 'https://example.com/nav',
            }
        ]

        response = test_client.post(
            '/api/v1/hospitals/nearby',
            json={
                'latitude': 31.2304,
                'longitude': 121.4737,
                'radius_meters': 5000,
                'limit': 10,
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['hospitals']) == 1
    assert data['hospitals'][0]['level'] == '三级甲等'


def test_nearby_hospital_endpoint_rejects_invalid_coordinates(test_client):
    response = test_client.post(
        '/api/v1/hospitals/nearby',
        json={
            'latitude': 131.2304,
            'longitude': 121.4737,
            'radius_meters': 5000,
            'limit': 10,
        },
    )

    assert response.status_code == 422


def test_nearby_hospital_endpoint_handles_service_failure(test_client):
    with patch('app.api.v1.endpoints.hospital.hospital_service') as mock_service:
        mock_service.search_nearby.side_effect = RuntimeError('provider unavailable')

        response = test_client.post(
            '/api/v1/hospitals/nearby',
            json={
                'latitude': 31.2304,
                'longitude': 121.4737,
                'radius_meters': 5000,
                'limit': 10,
            },
        )

    assert response.status_code == 503
    assert response.json()['detail'] == 'Hospital search service unavailable'
