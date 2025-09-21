#!/usr/bin/env python3
"""
Generate dummy land-use data for multiple states (Telangana, Odisha, MP, Tripura)
to support the multi-state WebGIS interface
"""

import json
import random
import numpy as np
from datetime import datetime
import os

def generate_state_landuse_data(state_name, state_bounds, districts_info):
    """Generate realistic dummy land-use data for a specific state"""
    
    # ESA WorldCover categories with colors
    landuse_categories = {
        'Tree cover': {'color': '#006400', 'code': 10},
        'Shrubland': {'color': '#FFBB22', 'code': 20},
        'Grassland': {'color': '#FFFF4C', 'code': 30},
        'Cropland': {'color': '#F096FF', 'code': 40},
        'Built-up': {'color': '#FA0000', 'code': 50},
        'Bare/sparse vegetation': {'color': '#B4B4B4', 'code': 60},
        'Permanent water bodies': {'color': '#0064C8', 'code': 80}
    }
    
    features = []
    feature_id = 1
    
    # Generate polygons for each district
    for district_name, pattern in districts_info.items():
        center_lat = random.uniform(state_bounds['min_lat'], state_bounds['max_lat'])
        center_lon = random.uniform(state_bounds['min_lon'], state_bounds['max_lon'])
        
        # Generate 2-4 polygons per district
        for i in range(random.randint(2, 4)):
            # Select land-use type based on district pattern
            landuse_type = np.random.choice(
                list(pattern.keys()), 
                p=[pattern[k]/100 for k in pattern.keys()]
            )
            
            # Generate polygon coordinates
            polygon_coords = generate_realistic_polygon(
                center_lat, center_lon, 
                size_km=random.uniform(8, 30),
                irregularity=0.3
            )
            
            # Calculate area (approximate)
            area_km2 = calculate_polygon_area(polygon_coords)
            
            feature = {
                "type": "Feature",
                "properties": {
                    "id": f"{state_name.upper()[:2]}_LU_{feature_id:03d}",
                    "landuse_type": landuse_type,
                    "landuse_code": landuse_categories[landuse_type]['code'],
                    "color": landuse_categories[landuse_type]['color'],
                    "description": f"{landuse_type} in {district_name}, {state_name}",
                    "district": district_name,
                    "state": state_name,
                    "area_km2": round(area_km2, 2),
                    "area_hectares": round(area_km2 * 100, 2),
                    "confidence": round(random.uniform(0.82, 0.96), 2),
                    "last_updated": "2024-01-15",
                    "data_source": "ESA WorldCover 2021 (Simulated)",
                    "resolution": "10m"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [polygon_coords]
                }
            }
            
            features.append(feature)
            feature_id += 1
    
    # Create GeoJSON structure
    geojson_data = {
        "type": "FeatureCollection",
        "properties": {
            "name": f"{state_name} Land-use Classification",
            "description": f"Dummy ESA WorldCover-style land-use data for {state_name}",
            "total_features": len(features),
            "generated_at": datetime.now().isoformat(),
            "bounds": state_bounds,
            "projection": "EPSG:4326",
            "data_source": "Generated for Vanachitra.AI prototype"
        },
        "features": features
    }
    
    return geojson_data

def generate_realistic_polygon(center_lat, center_lon, size_km=10, irregularity=0.2):
    """Generate a realistic polygon around a center point"""
    
    # Convert km to approximate degrees
    size_deg = size_km / 111.0
    
    # Generate points around a circle with irregularity
    num_points = random.randint(6, 10)
    angles = np.linspace(0, 2*np.pi, num_points, endpoint=False)
    
    coords = []
    for angle in angles:
        # Add irregularity to radius
        radius = size_deg * (1 + random.uniform(-irregularity, irregularity))
        
        # Calculate point
        lat = center_lat + radius * np.cos(angle)
        lon = center_lon + radius * np.sin(angle) / np.cos(np.radians(center_lat))
        
        coords.append([lon, lat])
    
    # Close the polygon
    coords.append(coords[0])
    
    return coords

def calculate_polygon_area(coords):
    """Calculate approximate area of polygon in km²"""
    n = len(coords) - 1
    area = 0.0
    
    for i in range(n):
        j = (i + 1) % n
        area += coords[i][0] * coords[j][1]
        area -= coords[j][0] * coords[i][1]
    
    area = abs(area) / 2.0
    
    # Convert to km² (rough approximation)
    avg_lat = sum(coord[1] for coord in coords[:-1]) / n
    lat_correction = np.cos(np.radians(avg_lat))
    area_km2 = area * 12321 * lat_correction
    
    return area_km2

def main():
    """Generate land-use data for all target states"""
    
    # State configurations
    states_config = {
        'Odisha': {
            'bounds': {'min_lat': 17.78, 'max_lat': 22.57, 'min_lon': 81.37, 'max_lon': 87.53},
            'districts': {
                'Mayurbhanj': {'Tree cover': 45, 'Cropland': 35, 'Grassland': 15, 'Built-up': 5},
                'Koraput': {'Tree cover': 55, 'Cropland': 25, 'Grassland': 15, 'Built-up': 5},
                'Bhubaneswar': {'Built-up': 40, 'Cropland': 35, 'Tree cover': 20, 'Permanent water bodies': 5},
                'Cuttack': {'Cropland': 50, 'Tree cover': 25, 'Built-up': 15, 'Permanent water bodies': 10},
                'Sambalpur': {'Tree cover': 40, 'Cropland': 40, 'Grassland': 15, 'Built-up': 5}
            }
        },
        'Madhya Pradesh': {
            'bounds': {'min_lat': 21.07, 'max_lat': 26.87, 'min_lon': 74.02, 'max_lon': 82.75},
            'districts': {
                'Bhopal': {'Built-up': 45, 'Cropland': 30, 'Tree cover': 20, 'Grassland': 5},
                'Indore': {'Built-up': 40, 'Cropland': 35, 'Tree cover': 20, 'Grassland': 5},
                'Jabalpur': {'Cropland': 45, 'Tree cover': 30, 'Built-up': 15, 'Grassland': 10},
                'Balaghat': {'Tree cover': 60, 'Cropland': 25, 'Grassland': 10, 'Built-up': 5},
                'Jhabua': {'Tree cover': 50, 'Cropland': 30, 'Grassland': 15, 'Built-up': 5}
            }
        },
        'Tripura': {
            'bounds': {'min_lat': 22.94, 'max_lat': 24.53, 'min_lon': 91.09, 'max_lon': 92.20},
            'districts': {
                'Agartala': {'Built-up': 35, 'Cropland': 35, 'Tree cover': 25, 'Permanent water bodies': 5},
                'Dharmanagar': {'Tree cover': 50, 'Cropland': 30, 'Grassland': 15, 'Built-up': 5},
                'Kailashahar': {'Tree cover': 45, 'Cropland': 35, 'Grassland': 15, 'Built-up': 5},
                'Udaipur': {'Cropland': 45, 'Tree cover': 35, 'Grassland': 15, 'Built-up': 5}
            }
        }
    }
    
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Generate data for each state
    for state_name, config in states_config.items():
        print(f"Generating land-use data for {state_name}...")
        
        geojson_data = generate_state_landuse_data(
            state_name, 
            config['bounds'], 
            config['districts']
        )
        
        # Save to file
        filename = f"output/{state_name.lower().replace(' ', '_')}_landuse_dummy.geojson"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(geojson_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Generated {len(geojson_data['features'])} polygons for {state_name}")
        print(f"📁 Saved to: {filename}")
        
        # Calculate summary
        total_area = sum(f['properties']['area_km2'] for f in geojson_data['features'])
        print(f"🗺️  Total area: {total_area:.1f} km²")
        print(f"💾 File size: ~{len(json.dumps(geojson_data))/1024:.1f} KB\n")

if __name__ == "__main__":
    main()
