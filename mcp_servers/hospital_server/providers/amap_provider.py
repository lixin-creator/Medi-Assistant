"""AMap provider for nearby hospital lookup."""

from __future__ import annotations

from urllib.parse import quote

import httpx

from mcp_servers.hospital_server.config import AMAP_WEB_SERVICE_KEY
from mcp_servers.hospital_server.matchers.tertiary_matcher import annotate_tertiary_labels

AMAP_COORDINATE_CONVERT_URL = 'https://restapi.amap.com/v3/assistant/coordinate/convert'
AMAP_POI_AROUND_URL = 'https://restapi.amap.com/v5/place/around'


class AMapHospitalProvider:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or AMAP_WEB_SERVICE_KEY

    def _convert_coordinates(self, latitude: float, longitude: float) -> tuple[float, float]:
        response = httpx.get(
            AMAP_COORDINATE_CONVERT_URL,
            params={
                'key': self.api_key,
                'locations': f'{longitude},{latitude}',
                'coordsys': 'gps',
            },
            timeout=20.0,
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get('status') != '1' or not payload.get('locations'):
            raise RuntimeError('AMap coordinate conversion failed')

        converted_longitude, converted_latitude = payload['locations'].split(',')
        return float(converted_latitude), float(converted_longitude)

    def _build_address(self, poi: dict) -> str:
        return ''.join(part for part in [poi.get('cityname'), poi.get('adname'), poi.get('address')] if part)

    def _build_navigation_url(self, longitude: float, latitude: float, name: str) -> str:
        return (
            'https://uri.amap.com/navigation?'
            f'to={longitude},{latitude},{quote(name)}&mode=car&coordinate=gaode&callnative=0'
        )

    def search_nearby_hospitals(
        self,
        latitude: float,
        longitude: float,
        radius_meters: int,
        limit: int,
    ) -> list[dict]:
        if not self.api_key:
            return []

        converted_latitude, converted_longitude = self._convert_coordinates(latitude, longitude)
        response = httpx.get(
            AMAP_POI_AROUND_URL,
            params={
                'key': self.api_key,
                'location': f'{converted_longitude},{converted_latitude}',
                'radius': min(radius_meters, 50000),
                'keywords': '医院',
                'types': '090100',
                'page_size': min(limit, 25),
                'sortrule': 'distance',
                'show_fields': 'business',
            },
            timeout=20.0,
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get('status') != '1':
            raise RuntimeError('AMap nearby hospital search failed')

        hospitals = []
        for poi in (payload.get('pois') or [])[:limit]:
            poi_longitude, poi_latitude = (poi.get('location') or '0,0').split(',')
            business = poi.get('business') or {}
            name = poi.get('name', '未命名医院')
            hospitals.append(
                {
                    'id': poi.get('id', ''),
                    'name': name,
                    'type': poi.get('type'),
                    'city': poi.get('cityname'),
                    'distance_meters': int(float(poi.get('distance', 0) or 0)),
                    'address': self._build_address(poi) or '未提供',
                    'phone': business.get('tel') or poi.get('tel'),
                    'latitude': float(poi_latitude),
                    'longitude': float(poi_longitude),
                    'navigation_url': self._build_navigation_url(float(poi_longitude), float(poi_latitude), name),
                }
            )

        return annotate_tertiary_labels(hospitals)
