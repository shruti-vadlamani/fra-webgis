import json
import random
import math

def generate_realistic_fra_parcels():
    """Generate realistic FRA parcels with proper sizing and placement"""
    
    # Forest coordinates in Telangana based on dense forest areas
    forest_centers = [
        {'lat': 19.16, 'lon': 79.11, 'name': 'Adilabad Forest'},
        {'lat': 18.5, 'lon': 79.5, 'name': 'Karimnagar Forest'}, 
        {'lat': 17.95, 'lon': 80.45, 'name': 'Warangal Forest'},
        {'lat': 18.2, 'lon': 78.8, 'name': 'Medak Forest'},
        {'lat': 17.5, 'lon': 79.2, 'name': 'Nalgonda Forest'},
        {'lat': 18.8, 'lon': 78.5, 'name': 'Nizamabad Forest'}
    ]
    
    features = []
    claim_id = 1
    
    for forest in forest_centers:
        center_lat = forest['lat']
        center_lon = forest['lon']
        forest_name = forest['name']
        
        # Generate 3-5 community clusters around each forest area
        num_clusters = random.randint(3, 5)
        
        for cluster in range(num_clusters):
            # Place cluster within 0.1-0.3 degrees of forest center
            cluster_offset_lat = random.uniform(-0.3, 0.3)
            cluster_offset_lon = random.uniform(-0.3, 0.3)
            cluster_lat = center_lat + cluster_offset_lat
            cluster_lon = center_lon + cluster_offset_lon
            
            village_name = f"Village_{cluster + 1}_{forest_name.split()[0]}"
            
            # Decide if this cluster has CFR (60% chance)
            has_cfr = random.random() < 0.6
            
            if has_cfr:
                # Create CFR - Large community forest area (100-800 hectares)
                cfr_area_hectares = random.uniform(100, 800)
                cfr_size_degrees = math.sqrt(cfr_area_hectares / 11100)  # Rough conversion
                
                cfr_coords = create_polygon_coordinates(
                    cluster_lat, cluster_lon, cfr_size_degrees, 6
                )
                
                cfr_feature = {
                    'type': 'Feature',
                    'properties': {
                        'claim_type': 'CFR',
                        'claim_id': f'CFR_{claim_id:03d}',
                        'village': village_name,
                        'community': f'Tribal Community {cluster + 1}',
                        'area_hectares': round(cfr_area_hectares, 2),
                        'status': random.choice(['Approved', 'Under Review', 'Pending']),
                        'claim_year': random.randint(2010, 2024),
                        'forest_area': forest_name
                    },
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [cfr_coords]
                    }
                }
                features.append(cfr_feature)
                claim_id += 1
            
            # Generate 8-15 IFR parcels around this cluster
            num_ifr = random.randint(8, 15)
            for ifr in range(num_ifr):
                # IFR - Small individual plots (0.2-3 hectares)
                ifr_area_hectares = random.uniform(0.2, 3.0)
                ifr_size_degrees = math.sqrt(ifr_area_hectares / 11100) * 0.8
                
                # Place within 0.05 degrees of cluster center
                ifr_lat = cluster_lat + random.uniform(-0.05, 0.05)
                ifr_lon = cluster_lon + random.uniform(-0.05, 0.05)
                
                ifr_coords = create_polygon_coordinates(
                    ifr_lat, ifr_lon, ifr_size_degrees, 4
                )
                
                ifr_feature = {
                    'type': 'Feature',
                    'properties': {
                        'claim_type': 'IFR',
                        'claim_id': f'IFR_{claim_id:03d}',
                        'village': village_name,
                        'family_name': f'Family_{ifr + 1}',
                        'area_hectares': round(ifr_area_hectares, 2),
                        'status': random.choice(['Approved', 'Under Review', 'Pending']),
                        'claim_year': random.randint(2008, 2024),
                        'forest_area': forest_name,
                        'cultivation_type': random.choice(['Agriculture', 'Habitation', 'Mixed'])
                    },
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [ifr_coords]
                    }
                }
                features.append(ifr_feature)
                claim_id += 1
            
            # Generate 2-4 CR parcels (community resources)
            num_cr = random.randint(2, 4)
            for cr in range(num_cr):
                # CR - Medium community resources (2-25 hectares)
                cr_area_hectares = random.uniform(2, 25)
                cr_size_degrees = math.sqrt(cr_area_hectares / 11100) * 0.9
                
                # Place within 0.08 degrees of cluster center
                cr_lat = cluster_lat + random.uniform(-0.08, 0.08)
                cr_lon = cluster_lon + random.uniform(-0.08, 0.08)
                
                cr_coords = create_polygon_coordinates(
                    cr_lat, cr_lon, cr_size_degrees, 5
                )
                
                cr_feature = {
                    'type': 'Feature',
                    'properties': {
                        'claim_type': 'CR',
                        'claim_id': f'CR_{claim_id:03d}',
                        'village': village_name,
                        'community': f'Tribal Community {cluster + 1}',
                        'area_hectares': round(cr_area_hectares, 2),
                        'status': random.choice(['Approved', 'Under Review', 'Pending']),
                        'claim_year': random.randint(2009, 2024),
                        'forest_area': forest_name,
                        'resource_type': random.choice(['Grazing Land', 'Water Body', 'NTFP Collection', 'Sacred Grove'])
                    },
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [cr_coords]
                    }
                }
                features.append(cr_feature)
                claim_id += 1
    
    # Create GeoJSON
    geojson = {
        'type': 'FeatureCollection',
        'features': features
    }
    
    # Save to file
    with open('output/telangana_fra_realistic.geojson', 'w') as f:
        json.dump(geojson, f, indent=2)
    
    print(f"Generated {len(features)} realistic FRA parcels:")
    cfr_count = len([f for f in features if f['properties']['claim_type'] == 'CFR'])
    ifr_count = len([f for f in features if f['properties']['claim_type'] == 'IFR'])
    cr_count = len([f for f in features if f['properties']['claim_type'] == 'CR'])
    print(f"  CFR: {cfr_count} parcels")
    print(f"  IFR: {ifr_count} parcels")
    print(f"  CR: {cr_count} parcels")
    
    return geojson

def create_polygon_coordinates(center_lat, center_lon, size, num_points):
    """Create polygon coordinates around a center point"""
    coords = []
    for i in range(num_points):
        angle = (2 * math.pi * i) / num_points
        # Add some randomness to make irregular shapes
        radius = size * (0.7 + 0.6 * random.random())
        lat_offset = radius * math.cos(angle)
        lon_offset = radius * math.sin(angle)
        
        lat = center_lat + lat_offset
        lon = center_lon + lon_offset
        coords.append([lon, lat])
    
    # Close the polygon
    coords.append(coords[0])
    return coords

if __name__ == "__main__":
    generate_realistic_fra_parcels()