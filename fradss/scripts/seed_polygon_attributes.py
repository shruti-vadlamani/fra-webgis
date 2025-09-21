#!/usr/bin/env python3
"""
Seed synthetic polygon attributes for FRA polygons into PostgreSQL and JSON fallback.

Requirements:
- Env var DATABASE_URL=postgresql://user:pass@host:port/dbname (optional)
- Input GeoJSON: output/vanachitra_fra_data.geojson

Outputs:
- PostgreSQL table polygon_attributes (if DATABASE_URL provided)
- JSON cache at output/polygon_attributes.json (always written)
"""

import json
import os
import random
from datetime import datetime
from typing import Dict, Any, List

DB_URL = os.getenv('DATABASE_URL')

try:
    import psycopg2  # type: ignore
    from psycopg2.extras import execute_values  # type: ignore
except Exception:
    psycopg2 = None
    execute_values = None

INPUT_GEOJSON = os.path.join('output', 'vanachitra_fra_data.geojson')
JSON_CACHE = os.path.join('output', 'polygon_attributes.json')

TARGET_STATES = {"Madhya Pradesh", "Odisha", "Telangana", "Tripura"}


def ensure_table(conn) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS polygon_attributes (
                polygon_id TEXT PRIMARY KEY,
                water_level INTEGER,
                groundwater_index REAL,
                soil_quality TEXT,
                crop_yield REAL,
                forest_cover_percentage REAL,
                poverty_index REAL,
                infra_index REAL
            );
            """
        )
        conn.commit()


def soil_quality_for_type(fra_type: str) -> str:
    mapping = {
        'Community Forest Resource Rights': ['Good', 'Excellent', 'Moderate'],
        'Individual Forest Rights': ['Moderate', 'Good', 'Poor'],
        'Community Rights': ['Moderate', 'Good'],
        'Agriculture': ['Poor', 'Moderate', 'Good'],
        'Water Body': ['Moderate', 'Good']
    }
    choices = mapping.get(fra_type, ['Moderate', 'Good'])
    return random.choice(choices)


def generate_attributes(feature: Dict[str, Any]) -> Dict[str, Any]:
    props = feature.get('properties', {})
    fra_type = props.get('fra_type') or props.get('feature_type')
    claim_type = props.get('claim_type')
    if claim_type == 'CFR':
        fra_type = 'Community Forest Resource Rights'
    elif claim_type == 'IFR':
        fra_type = 'Individual Forest Rights'
    elif claim_type == 'CR':
        fra_type = 'Community Rights'

    # Base ranges by type
    if fra_type == 'Water Body':
        water_level = random.randint(120, 250)
        groundwater_index = round(random.uniform(0.5, 0.9), 2)
        crop_yield = round(random.uniform(5, 15), 1)
        forest_cover = round(random.uniform(10, 40), 1)
    elif fra_type == 'Agriculture':
        water_level = random.randint(40, 140)
        groundwater_index = round(random.uniform(0.2, 0.7), 2)
        crop_yield = round(random.uniform(10, 35), 1)
        forest_cover = round(random.uniform(0, 20), 1)
    elif fra_type == 'Community Forest Resource Rights':
        water_level = random.randint(60, 160)
        groundwater_index = round(random.uniform(0.3, 0.8), 2)
        crop_yield = round(random.uniform(8, 25), 1)
        forest_cover = round(random.uniform(50, 90), 1)
    elif fra_type == 'Community Rights':
        water_level = random.randint(50, 150)
        groundwater_index = round(random.uniform(0.3, 0.7), 2)
        crop_yield = round(random.uniform(8, 22), 1)
        forest_cover = round(random.uniform(30, 70), 1)
    else:  # IFR or unknown
        water_level = random.randint(50, 150)
        groundwater_index = round(random.uniform(0.2, 0.7), 2)
        crop_yield = round(random.uniform(10, 28), 1)
        forest_cover = round(random.uniform(10, 50), 1)

    poverty_index = round(random.uniform(0.3, 0.9), 2)
    infra_index = round(random.uniform(0.2, 0.9), 2)
    soil_quality = soil_quality_for_type(fra_type or 'Unknown')

    return {
        'water_level': water_level,
        'groundwater_index': groundwater_index,
        'soil_quality': soil_quality,
        'crop_yield': crop_yield,
        'forest_cover_percentage': forest_cover,
        'poverty_index': poverty_index,
        'infra_index': infra_index,
    }


def load_features() -> List[Dict[str, Any]]:
    with open(INPUT_GEOJSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    features = data.get('features', [])
    selected = []
    for feat in features:
        props = feat.get('properties', {})
        state = props.get('state')
        if state in TARGET_STATES:
            selected.append(feat)
    return selected


def determine_polygon_id(props: Dict[str, Any]) -> str:
    return props.get('claim_id') or props.get('feature_id') or props.get('fra_id') or props.get('id')


def main() -> None:
    if not os.path.exists('output'):
        os.makedirs('output')

    features = load_features()
    records = []
    json_cache: Dict[str, Any] = {
        'generated_at': datetime.utcnow().isoformat(),
        'count': 0,
        'items': {}
    }

    for feat in features:
        props = feat.get('properties', {})
        polygon_id = determine_polygon_id(props)
        if not polygon_id:
            continue
        attrs = generate_attributes(feat)
        records.append((
            polygon_id,
            attrs['water_level'],
            attrs['groundwater_index'],
            attrs['soil_quality'],
            attrs['crop_yield'],
            attrs['forest_cover_percentage'],
            attrs['poverty_index'],
            attrs['infra_index'],
        ))
        json_cache['items'][polygon_id] = attrs

    json_cache['count'] = len(json_cache['items'])

    # Always write JSON cache
    with open(JSON_CACHE, 'w', encoding='utf-8') as f:
        json.dump(json_cache, f, indent=2)
    print(f"Wrote JSON cache with {json_cache['count']} items to {JSON_CACHE}")

    # Optionally write to PostgreSQL
    if DB_URL and psycopg2 is not None:
        try:
            conn = psycopg2.connect(DB_URL)
            ensure_table(conn)
            with conn.cursor() as cur:
                execute_values(
                    cur,
                    """
                    INSERT INTO polygon_attributes (
                        polygon_id, water_level, groundwater_index, soil_quality,
                        crop_yield, forest_cover_percentage, poverty_index, infra_index
                    ) VALUES %s
                    ON CONFLICT (polygon_id) DO UPDATE SET
                        water_level = EXCLUDED.water_level,
                        groundwater_index = EXCLUDED.groundwater_index,
                        soil_quality = EXCLUDED.soil_quality,
                        crop_yield = EXCLUDED.crop_yield,
                        forest_cover_percentage = EXCLUDED.forest_cover_percentage,
                        poverty_index = EXCLUDED.poverty_index,
                        infra_index = EXCLUDED.infra_index;
                    """,
                    records
                )
            conn.commit()
            conn.close()
            print(f"Upserted {len(records)} rows into PostgreSQL polygon_attributes table.")
        except Exception as e:
            print(f"Warning: Failed to write to PostgreSQL: {e}")


if __name__ == '__main__':
    main()


