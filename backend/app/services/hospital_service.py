"""Hospital lookup service with output normalization helpers."""

from app.core.logging_config import logger


def normalize_hospital_level(raw_level: str | None) -> str:
    return raw_level.strip() if raw_level else '未标注'


def format_distance(distance_meters: int | float | None) -> str:
    if distance_meters is None:
        return '未知距离'
    if distance_meters < 1000:
        return f'{int(distance_meters)} m'
    return f'{distance_meters / 1000:.1f} km'


class HospitalService:
    def __init__(self, client=None):
        self.client = client

    def search_nearby(self, latitude: float, longitude: float, radius_meters: int, limit: int) -> list[dict]:
        if self.client is None:
            logger.warning('HospitalService: no hospital client configured')
            return []

        hospitals = self.client.search_nearby_hospitals(
            latitude=latitude,
            longitude=longitude,
            radius_meters=radius_meters,
            limit=limit,
        )

        normalized_items = []
        for item in hospitals:
            distance_meters = item.get('distance_meters')
            tertiary_label = item.get('tertiary_label', '')
            normalized_items.append(
                {
                    'id': item.get('id', ''),
                    'name': item.get('name', '未命名医院'),
                    'level': tertiary_label,
                    'is_tertiary_a': bool(item.get('is_tertiary_a', False)),
                    'distance_meters': int(distance_meters) if distance_meters is not None else 0,
                    'distance_text': format_distance(distance_meters),
                    'address': item.get('address', '未提供'),
                    'phone': item.get('phone'),
                    'latitude': item.get('latitude', latitude),
                    'longitude': item.get('longitude', longitude),
                    'navigation_url': item.get('navigation_url'),
                }
            )

        return normalized_items
