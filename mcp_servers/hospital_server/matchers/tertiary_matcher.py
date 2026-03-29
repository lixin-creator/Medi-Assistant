"""Static tertiary-A hospital matcher."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / 'data' / 'tertiary_hospitals.json'


def _normalize_text(value: str | None) -> str:
    if not value:
        return ''
    normalized = value.strip().lower()
    normalized = re.sub(r'[（）()\s]', '', normalized)
    normalized = re.sub(r'(东院区|西院区|南院区|北院区|东院|西院|南院|北院)$', '', normalized)
    return normalized


def _normalize_city(value: str | None) -> str:
    city = _normalize_text(value)
    for suffix in ('市', '特别行政区'):
        if city.endswith(suffix):
            city = city[: -len(suffix)]
    return city


@lru_cache(maxsize=1)
def load_tertiary_hospitals() -> list[dict]:
    with DATA_FILE.open('r', encoding='utf-8') as file:
        return json.load(file)


def match_tertiary_a_hospital(name: str, city: str | None, address: str | None) -> dict | None:
    normalized_name = _normalize_text(name)
    normalized_city = _normalize_city(city)
    normalized_address = _normalize_text(address)

    for item in load_tertiary_hospitals():
        if _normalize_city(item.get('city')) != normalized_city:
            continue

        candidate_names = [_normalize_text(item.get('canonical_name'))]
        candidate_names.extend(_normalize_text(alias) for alias in item.get('aliases', []))

        if normalized_name not in candidate_names:
            continue

        address_keywords = [_normalize_text(keyword) for keyword in item.get('address_keywords', [])]
        if address_keywords and normalized_address:
            if not any(keyword and keyword in normalized_address for keyword in address_keywords):
                continue

        return item

    return None


def annotate_tertiary_labels(hospitals: list[dict]) -> list[dict]:
    annotated = []
    for hospital in hospitals:
        matched_item = match_tertiary_a_hospital(
            hospital.get('name', ''),
            hospital.get('city'),
            hospital.get('address'),
        )
        is_tertiary_a = bool(matched_item and matched_item.get('is_tertiary_a'))
        enriched = dict(hospital)
        enriched['is_tertiary_a'] = is_tertiary_a
        enriched['tertiary_label'] = '三甲医院' if is_tertiary_a else ''
        annotated.append(enriched)
    return annotated
