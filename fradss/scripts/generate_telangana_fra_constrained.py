#!/usr/bin/env python3
"""
Generate Telangana FRA data (IFR, CFR, CR) restricted to forest areas
Based on existing Telangana land-use data (Tree cover areas)
"""

import json
import random
import math
from datetime import datetime, timedelta
import os

def generate_telangana_landuse_data():
    """Generate realistic dummy land-use data for Telangana state"""
    
    # ESA WorldCover categories with colors and realistic distribution
    landuse_categories = {
        'Tree cover': {
            'color': '#006400',
            'code': 10,
            'description': 'Dense forest areas, mainly in eastern districts',
            'percentage': 25
        },
        'Shrubland': {
            'color': '#FFBB22', 
            'code': 20,
            'description': 'Sparse vegetation and scrubland',
            'percentage': 15
        },
        'Grassland': {
            'color': '#FFFF4C',
            'code': 30,
            'description': 'Natural grasslands and grazing areas',
            'percentage': 10
        },
        'Cropland': {
            'color': '#F096FF',
            'code': 40,
            'description': 'Agricultural areas - rice, cotton, maize',
            'percentage': 35
        },
        'Built-up': {
            'color': '#FA0000',
            'code': 50,
            'description': 'Urban areas including Hyderabad metro',
            'percentage': 8
        },
        'Bare/sparse vegetation': {
            'color': '#B4B4B4',
            'code': 60,
            'description': 'Rocky outcrops and sparse vegetation',
            'percentage': 5
        },
        'Permanent water bodies': {
            'color': '#0064C8',
            'code': 80,
            'description': 'Rivers, lakes, and reservoirs',
            'percentage': 2
        }
    }
    
    # Telangana approximate bounds
    telangana_bounds = {
        'min_lat': 15.8,
        'max_lat': 19.9,
        'min_lon': 77.3,
        'max_lon': 81.1
    }
    
    # District-wise realistic land-use patterns
    district_patterns = {
        'Hyderabad': {'Built-up': 60, 'Cropland': 25, 'Tree cover': 10, 'Permanent water bodies': 5},
        'Adilabad': {'Tree cover': 55, 'Cropland': 30, 'Grassland': 10, 'Shrubland': 5},
        'Warangal': {'Cropland': 50, 'Tree cover': 25, 'Grassland': 15, 'Built-up': 10},
        'Khammam': {'Tree cover': 45, 'Cropland': 35, 'Permanent water bodies': 10, 'Grassland': 10},
        'Nizamabad': {'Cropland': 60, 'Tree cover': 20, 'Grassland': 15, 'Built-up': 5},
        'Karimnagar': {'Cropland': 55, 'Tree cover': 25, 'Grassland': 15, 'Built-up': 5},
        'Medak': {'Cropland': 50, 'Grassland': 25, 'Tree cover': 20, 'Built-up': 5},
        'Rangareddy': {'Built-up': 35, 'Cropland': 40, 'Tree cover': 20, 'Permanent water bodies': 5},
        'Mahbubnagar': {'Cropland': 45, 'Bare/sparse vegetation': 25, 'Tree cover': 20, 'Grassland': 10},
        'Nalgonda': {'Cropland': 50, 'Tree cover': 25, 'Grassland': 20, 'Permanent water bodies': 5}
    }
    
    features = []
    feature_id = 1
    
    # Generate polygons for each district pattern
    for district, pattern in district_patterns.items():
        # Get district center coordinates (approximate)
        district_centers = {
            'Hyderabad': [78.4867, 17.3850],
            'Adilabad': [78.5311, 19.6700],
            'Warangal': [79.5941, 17.9689],
            'Khammam': [80.1514, 17.2473],
            'Nizamabad': [78.0937, 18.6725],
            'Karimnagar': [79.1288, 18.4386],
            'Medak': [78.2747, 18.0387],
            'Rangareddy': [78.2466, 17.4065],
            'Mahbubnagar': [77.9974, 16.7460],
            'Nalgonda': [79.2673, 17.0542]
        }
        
        center_lon, center_lat = district_centers.get(district, [78.9629, 17.9689])
        
        # Generate 2-3 polygons per district
        for i in range(random.randint(2, 4)):
            # Select land-use type based on district pattern
            landuse_type = np.random.choice(
                list(pattern.keys()), 
                p=[pattern[k]/100 for k in pattern.keys()]
            )
            
            # Generate polygon around district center with some randomness
            polygon_coords = generate_realistic_polygon(
                center_lat, center_lon, 
                size_km=random.uniform(5, 25),
                irregularity=0.3
            )
            
            # Calculate area (approximate)
            area_km2 = calculate_polygon_area(polygon_coords)
            
            feature = {
                "type": "Feature",
                "properties": {
                    "id": f"TG_LU_{feature_id:03d}",
                    "landuse_type": landuse_type,
                    "landuse_code": landuse_categories[landuse_type]['code'],
                    "color": landuse_categories[landuse_type]['color'],
                    "description": landuse_categories[landuse_type]['description'],
                    "district": district,
                    "area_km2": round(area_km2, 2),
                    "area_hectares": round(area_km2 * 100, 2),
                    "confidence": round(random.uniform(0.85, 0.98), 2),
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
            "name": "Telangana Land-use Classification",
            "description": "Dummy ESA WorldCover-style land-use data for Telangana",
            "total_features": len(features),
            "categories": len(landuse_categories),
            "generated_at": datetime.now().isoformat(),
            "bounds": telangana_bounds,
            "projection": "EPSG:4326",
            "data_source": "Generated for Vanachitra.AI prototype"
        },
        "features": features
    }
    
    return geojson_data, landuse_categories

def generate_realistic_polygon(center_lat, center_lon, size_km=10, irregularity=0.2):
    """Generate a realistic polygon around a center point"""
    
    # Convert km to approximate degrees (rough conversion)
    size_deg = size_km / 111.0  # 1 degree ≈ 111 km
    
    # Generate points around a circle with irregularity
    num_points = random.randint(6, 12)
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
    # Simple approximation using shoelace formula
    n = len(coords) - 1  # Exclude closing point
    area = 0.0
    
    for i in range(n):
        j = (i + 1) % n
        area += coords[i][0] * coords[j][1]
        area -= coords[j][0] * coords[i][1]
    
    area = abs(area) / 2.0
    
    # Convert from degrees² to km² (rough approximation)
    # 1 degree² ≈ 12321 km² at equator, adjust for latitude
    avg_lat = sum(coord[1] for coord in coords[:-1]) / n
    lat_correction = np.cos(np.radians(avg_lat))
    area_km2 = area * 12321 * lat_correction
    
    return area_km2

def main():
    """Generate and save Telangana land-use data"""
    print("Generating Telangana land-use data...")
    
    # Generate data
    geojson_data, categories = generate_telangana_landuse_data()
    
    # Save to file
    output_file = 'output/telangana_landuse_dummy.geojson'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, indent=2, ensure_ascii=False)
    
    # Save categories for legend
    categories_file = 'output/telangana_landuse_categories.json'
    with open(categories_file, 'w', encoding='utf-8') as f:
        json.dump(categories, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated {len(geojson_data['features'])} land-use polygons")
    print(f"📁 Saved to: {output_file}")
    print(f"📊 Categories saved to: {categories_file}")
    
    # Print summary
    print("\n📈 Land-use Summary:")
    landuse_counts = {}
    total_area = 0
    
    for feature in geojson_data['features']:
        landuse = feature['properties']['landuse_type']
        area = feature['properties']['area_km2']
        
        if landuse not in landuse_counts:
            landuse_counts[landuse] = {'count': 0, 'area': 0}
        
        landuse_counts[landuse]['count'] += 1
        landuse_counts[landuse]['area'] += area
        total_area += area
    
    for landuse, data in landuse_counts.items():
        percentage = (data['area'] / total_area) * 100
        print(f"  {landuse}: {data['count']} polygons, {data['area']:.1f} km² ({percentage:.1f}%)")
    
    print(f"\n🗺️  Total area covered: {total_area:.1f} km²")
    print(f"💾 File size: ~{len(json.dumps(geojson_data))/1024:.1f} KB")

if __name__ == "__main__":
    main()
