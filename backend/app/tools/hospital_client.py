"""
MediAssistant - tools/hospital_client.py
Hospital MCP client for nearby hospital lookup.
"""

from __future__ import annotations

import httpx

from app.core.config import HOSPITAL_MCP_SERVER_URL
from app.core.logging_config import logger


class HospitalClient:
    def __init__(self, server_url: str | None = None):
        self.server_url = (server_url or HOSPITAL_MCP_SERVER_URL).rstrip('/')

    def search_nearby_hospitals(
        self,
        latitude: float,
        longitude: float,
        radius_meters: int,
        limit: int,
    ) -> list[dict]:
        response = httpx.post(
            f'{self.server_url}/tools/search_nearby_hospitals',
            json={
                'latitude': latitude,
                'longitude': longitude,
                'radius_meters': radius_meters,
                'limit': limit,
            },
            timeout=20.0,
            trust_env=False,
        )
        response.raise_for_status()
        payload = response.json()
        if not payload.get('success'):
            raise RuntimeError('Hospital MCP request failed')
        return payload.get('results', [])


_hospital_client = None


def get_hospital_client() -> HospitalClient:
    global _hospital_client
    if _hospital_client is None:
        _hospital_client = HospitalClient(server_url=HOSPITAL_MCP_SERVER_URL)
        logger.info('Hospital MCP client initialized')
    return _hospital_client
