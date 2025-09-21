#!/usr/bin/env python3
"""
Generate Telangana FRA data at specific forest coordinates provided by user
Places CFR, IFR, and CR polygons around exact coordinate locations
"""

import json
import random
import math
from datetime import datetime, timedelta
import os

class CoordinateBasedFRAGenerator:
    def __init__(self):
        # Specific forest coordinates provided by user (from coordinate images)
        self.forest_coordinates = [
            {'lat': 17.95, 'lon': 80.45, 'name': 'Eastern_Forest', 'district': 'Khammam'},
            {'lat': 19.16, 'lon': 79.11, 'name': 'Northern_Forest', 'district': 'Adilabad'}, 
            {'lat': 16.15, 'lon': 78.72, 'name': 'Southern_Forest', 'district': 'Mahbubnagar'}
        ]
        
        # Telangana forest districts
        self.forest_districts = ['Adilabad', 'Kumuram Bheem', 'Khammam', 'Mahbubnagar', 'Warangal', 'Mancherial']
        
        # Tribal communities in Telangana
        self.tribal_communities = ['Gond', 'Koya', 'Lambada', 'Yerukala', 'Chenchu']
        
        # Village patterns for Telangana
        self.village_patterns = ['palli', 'guda', 'nagar', 'puram']
        
    def generate_realistic_village_name(self):
        """Generate realistic village names for Telangana"""
        prefixes = ['Raja', 'Krishna', 'Rama', 'Sita', 'Ganga', 'Venkate', 'Lakshmi', 'Bhima', 'Koti', 'Meka']
        suffix = random.choice(self.village_patterns)
        prefix = random.choice(prefixes)
        return f"{prefix}{suffix}"
    
    def generate_point_near_coordinate(self, base_lat, base_lon, radius_km=3.0):
        """Generate a random point within radius_km of the base coordinate"""
        # Convert km to approximate degrees (1 degree ≈ 111 km)
        radius_deg = radius_km / 111.0
        
        # Random angle and distance
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0.1, radius_deg)  # Min 0.1 km away
        
        # Calculate new coordinates
        lat = base_lat + distance * math.cos(angle)
        lon = base_lon + distance * math.sin(angle)
        
        return lat, lon
    
    def generate_polygon(self, center_lat, center_lon, area_hectares, shape='irregular'):
        """Generate polygon with specified area around center point"""
        # Convert hectares to approximate degrees (rough approximation)
        area_deg_sq = area_hectares * 0.0001
        radius_deg = math.sqrt(area_deg_sq / math.pi)
        
        if shape == 'rectangular':
            # Rectangular plot (typical for agricultural IFR)
            width = radius_deg * random.uniform(1.2, 2.5)
            height = area_deg_sq / width
            
            # Add slight rotation
            rotation = random.uniform(-math.pi/8, math.pi/8)
            
            corners = [
                [-width/2, -height/2],
                [width/2, -height/2], 
                [width/2, height/2],
                [-width/2, height/2]
            ]
            
            points = []
            for corner in corners:
                x_rot = corner[0] * math.cos(rotation) - corner[1] * math.sin(rotation)
                y_rot = corner[0] * math.sin(rotation) + corner[1] * math.cos(rotation)
                points.append([center_lon + x_rot, center_lat + y_rot])
            
        else:
            # Irregular polygon
            num_points = random.randint(6, 10)
            points = []
            
            for i in range(num_points):
                angle = 2 * math.pi * i / num_points
                r = radius_deg * random.uniform(0.7, 1.3)
                
                lat = center_lat + r * math.cos(angle)
                lon = center_lon + r * math.sin(angle)
                points.append([lon, lat])
        
        # Close the polygon
        points.append(points[0])
        return points
    
    def point_in_polygon(self, point, polygon_coords):
        """Check if a point is inside a polygon using ray casting algorithm"""
        x, y = point
        n = len(polygon_coords)
        inside = False
        
        p1x, p1y = polygon_coords[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon_coords[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside
    
    def generate_cfr_at_location(self, forest_loc, village_name, tribal_community):
        """Generate a CFR polygon at a specific forest location"""
        # Generate CFR around the forest coordinate with some variation
        center_lat, center_lon = self.generate_point_near_coordinate(
            forest_loc['lat'], forest_loc['lon'], radius_km=2.0
        )
        
        # CFR should be substantial - 200-600 hectares
        area_hectares = random.uniform(200, 600)
        
        polygon_coords = self.generate_polygon(
            center_lat, center_lon, area_hectares, 'irregular'
        )
        
        cfr_data = {
            'coordinates': [polygon_coords],
            'center': [center_lat, center_lon],
            'area_hectares': area_hectares,
            'district': forest_loc['district'],
            'location_name': forest_loc['name'],
            'bounds': {
                'min_lat': min(coord[1] for coord in polygon_coords),
                'max_lat': max(coord[1] for coord in polygon_coords),
                'min_lon': min(coord[0] for coord in polygon_coords),
                'max_lon': max(coord[0] for coord in polygon_coords)
            }
        }
        
        cfr_feature = {
            'type': 'Feature',
            'properties': {
                'claim_id': f'CFR_TG_{forest_loc["district"][:3].upper()}_{forest_loc["name"][:3].upper()}',
                'claim_type': 'CFR',
                'fra_type': 'Community Forest Resource Rights',
                'village': village_name,
                'district': forest_loc['district'],
                'state': 'Telangana',
                'area_claimed': round(area_hectares, 2),
                'area_unit': 'hectares',
                'status': random.choice(['Approved', 'Pending', 'Under Review']),
                'tribal_community': tribal_community,
                'gram_sabha': f'{village_name} Gram Sabha',
                'total_households': random.randint(50, 150),
                'forest_committee_formed': random.choice([True, False]),
                'management_plan': random.choice(['Prepared', 'Under Preparation', 'Not Started']),
                'submission_date': (datetime.now() - timedelta(days=random.randint(60, 900))).strftime('%Y-%m-%d'),
                'forest_type': random.choice(['Dry Deciduous', 'Moist Deciduous', 'Scrub Forest']),
                'forest_location': forest_loc['name'],
                'base_coordinates': f"{forest_loc['lat']}, {forest_loc['lon']}"
            },
            'geometry': {
                'type': 'Polygon',
                'coordinates': [polygon_coords]
            }
        }
        
        return cfr_data, cfr_feature
    
    def generate_point_inside_cfr(self, cfr_data):
        """Generate a random point inside the CFR polygon"""
        bounds = cfr_data['bounds']
        max_attempts = 150
        
        for _ in range(max_attempts):
            lon = random.uniform(bounds['min_lon'], bounds['max_lon'])
            lat = random.uniform(bounds['min_lat'], bounds['max_lat'])
            
            if self.point_in_polygon([lon, lat], cfr_data['coordinates'][0]):
                return lat, lon
        
        # Fallback to CFR center
        return cfr_data['center'][0], cfr_data['center'][1]
    
    def generate_ifr_polygons(self, cfr_data, village_name, tribal_community, num_ifrs=25):
        """Generate IFR polygons inside CFR - individual property sizes (0.1-1.2 hectares)"""
        ifr_features = []
        district = cfr_data['district']
        
        for i in range(num_ifrs):
            # Generate point inside CFR
            center_lat, center_lon = self.generate_point_inside_cfr(cfr_data)
            
            # IFR should be very small - individual household land (0.1 to 1.2 hectares)
            area_hectares = random.uniform(0.1, 1.2)
            
            # Generate small rectangular plot (typical for individual holdings)
            polygon_coords = self.generate_polygon(
                center_lat, center_lon, area_hectares, 'rectangular'
            )
            
            # Generate household head name
            household_heads = [
                'Ramesh Kumar', 'Sita Devi', 'Lakshman Singh', 'Ganga Bai', 
                'Ravi Rao', 'Kamala Devi', 'Suresh Kumar', 'Radha Bai',
                'Gopal Singh', 'Anita Devi', 'Kiran Kumar', 'Pushpa Bai'
            ]
            household_head = random.choice(household_heads)
            
            ifr_feature = {
                'type': 'Feature',
                'properties': {
                    'claim_id': f'IFR_TG_{district[:3].upper()}_{i+1:03d}',
                    'claim_type': 'IFR',
                    'fra_type': 'Individual Forest Rights',
                    'village': village_name,
                    'district': district,
                    'state': 'Telangana',
                    'area_claimed': round(area_hectares, 2),
                    'area_unit': 'hectares',
                    'status': random.choice(['Approved', 'Pending', 'Under Review']),
                    'tribal_community': tribal_community,
                    'household_head': household_head,
                    'family_members': random.randint(3, 8),
                    'livelihood': random.choice(['Agriculture', 'NTFP Collection', 'Animal Husbandry', 'Mixed']),
                    'submission_date': (datetime.now() - timedelta(days=random.randint(30, 730))).strftime('%Y-%m-%d'),
                    'survey_number': f'SY_{random.randint(100, 999)}',
                    'patta_issued': random.choice([True, False]),
                    'cultivation_type': random.choice(['Paddy', 'Cotton', 'Maize', 'Vegetables', 'Mixed Crops']),
                    'forest_location': cfr_data['location_name']
                },
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': [polygon_coords]
                }
            }
            
            ifr_features.append(ifr_feature)
        
        return ifr_features
    
    def generate_cr_features(self, cfr_data, village_name, tribal_community, num_crs=4):
        """Generate CR features inside CFR - only as polygons, no point markers"""
        cr_features = []
        district = cfr_data['district']
        
        cr_types = ['Grazing Ground', 'NTFP Collection Area', 'Sacred Grove', 'Community Water Source']
        
        for i in range(num_crs):
            cr_type = random.choice(cr_types)
            
            # Generate point inside CFR
            center_lat, center_lon = self.generate_point_inside_cfr(cfr_data)
            
            # All CR features as polygons - small to medium areas (1-15 hectares)
            area_hectares = random.uniform(1.0, 15.0)
            
            polygon_coords = self.generate_polygon(
                center_lat, center_lon, area_hectares, 'irregular'
            )
            
            cr_feature = {
                'type': 'Feature',
                'properties': {
                    'claim_id': f'CR_TG_{district[:3].upper()}_{i+1:03d}',
                    'claim_type': 'CR',
                    'fra_type': 'Community Rights',
                    'resource_type': cr_type,
                    'village': village_name,
                    'district': district,
                    'state': 'Telangana',
                    'area_claimed': round(area_hectares, 2),
                    'area_unit': 'hectares',
                    'status': random.choice(['Approved', 'Pending']),
                    'tribal_community': tribal_community,
                    'beneficiary_households': random.randint(20, 80),
                    'usage_pattern': random.choice(['Seasonal', 'Year-round', 'Occasional']),
                    'traditional_use': random.choice([True, False]),
                    'community_management': True,
                    'forest_location': cfr_data['location_name']
                },
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': [polygon_coords]
                }
            }
            
            cr_features.append(cr_feature)
        
        return cr_features
    
    def generate_telangana_fra_data(self):
        """Generate complete FRA data for the 3 specific forest locations"""
        all_features = []
        
        print(f"Generating FRA data for {len(self.forest_coordinates)} forest locations...")
        
        for idx, forest_loc in enumerate(self.forest_coordinates):
            print(f"Processing {forest_loc['name']} at {forest_loc['lat']}, {forest_loc['lon']}")
            
            village_name = self.generate_realistic_village_name()
            tribal_community = random.choice(self.tribal_communities)
            
            # Generate CFR at this forest location
            cfr_data, cfr_feature = self.generate_cfr_at_location(forest_loc, village_name, tribal_community)
            all_features.append(cfr_feature)
            
            # Generate IFR features inside CFR
            ifr_features = self.generate_ifr_polygons(
                cfr_data, village_name, tribal_community, 
                num_ifrs=random.randint(15, 25)  # Fewer IFRs per location
            )
            all_features.extend(ifr_features)
            
            # Generate CR features inside CFR
            cr_features = self.generate_cr_features(
                cfr_data, village_name, tribal_community, 
                num_crs=random.randint(3, 5)
            )
            all_features.extend(cr_features)
        
        # Create GeoJSON structure
        fra_geojson = {
            'type': 'FeatureCollection',
            'properties': {
                'title': 'Telangana Forest Rights Act Spatial Data (Coordinate-Based)',
                'description': 'FRA claims data placed at specific forest coordinates provided by user',
                'created_date': datetime.now().isoformat(),
                'total_features': len(all_features),
                'state': 'Telangana',
                'spatial_reference': 'EPSG:4326 (WGS84)',
                'data_quality': 'Synthetic but placed at user-specified forest locations',
                'coordinate_locations': [
                    f"{loc['name']}: {loc['lat']}, {loc['lon']}" for loc in self.forest_coordinates
                ]
            },
            'features': all_features
        }
        
        return fra_geojson

def main():
    """Generate Telangana FRA data at specific coordinates"""
    print("🎯 Generating Telangana FRA Data at Specified Forest Coordinates...")
    print("=" * 70)
    
    generator = CoordinateBasedFRAGenerator()
    
    # Show coordinate locations
    print("📍 Target Forest Locations:")
    for loc in generator.forest_coordinates:
        print(f"   • {loc['name']}: {loc['lat']}°N, {loc['lon']}°E ({loc['district']})")
    
    # Generate FRA data
    fra_data = generator.generate_telangana_fra_data()
    
    # Save to file
    os.makedirs('output', exist_ok=True)
    output_file = 'output/telangana_fra_coordinates.geojson'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(fra_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Telangana FRA data generated successfully!")
    print(f"📁 Output file: {output_file}")
    print(f"📊 Total features: {len(fra_data['features'])}")
    
    # Print summary by feature type and location
    feature_counts = {}
    total_area_by_type = {}
    location_counts = {}
    
    for feature in fra_data['features']:
        ftype = feature['properties']['claim_type']
        area = feature['properties'].get('area_claimed', 0)
        location = feature['properties'].get('forest_location', 'Unknown')
        
        feature_counts[ftype] = feature_counts.get(ftype, 0) + 1
        total_area_by_type[ftype] = total_area_by_type.get(ftype, 0) + area
        location_counts[location] = location_counts.get(location, 0) + 1
    
    print("\n📈 Feature type distribution:")
    for ftype, count in feature_counts.items():
        avg_area = total_area_by_type[ftype] / count if count > 0 else 0
        print(f"   {ftype}: {count} features, Total: {total_area_by_type[ftype]:.1f} ha, Avg: {avg_area:.1f} ha")
    
    print("\n🌍 Distribution by forest location:")
    for location, count in location_counts.items():
        print(f"   {location}: {count} features")
    
    print(f"\n🎯 All FRA features placed around specified forest coordinates")
    print("✅ Realistic polygon sizes: CFR (200-600 ha), IFR (0.1-1.2 ha), CR (1-15 ha)")

if __name__ == '__main__':
    main()