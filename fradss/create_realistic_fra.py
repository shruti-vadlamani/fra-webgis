import json
import random
import math

def create_realistic_fra_parcels():
    """Create realistic FRA parcels that don't overlap and are properly constrained to forest areas"""
    
    # Define specific forest coordinates in Telangana (based on dense forest areas)
    forest_regions = [
        # Northern Telangana forests (Adilabad/Komaram Bheem districts)
        {'center': [19.16, 79.11], 'name': 'Adilabad Forest Block', 'size': 'large'},
        {'center': [19.05, 79.25], 'name': 'Asifabad Forest Block', 'size': 'large'},
        {'center': [18.95, 79.35], 'name': 'Kagaznagar Forest Block', 'size': 'medium'},
        
        # Central-Eastern forests (Warangal region)
        {'center': [18.0, 79.8], 'name': 'Warangal Forest Block', 'size': 'medium'},
        {'center': [18.15, 79.95], 'name': 'Pakhal Forest Block', 'size': 'medium'},
        
        # Eastern forests (Khammam district)
        {'center': [17.95, 80.45], 'name': 'Khammam Forest Block', 'size': 'large'},
        {'center': [17.75, 80.25], 'name': 'Bhadrachalam Forest Block', 'size': 'large'},
        
        # Western forests (Medak region)
        {'center': [18.2, 78.8], 'name': 'Medak Forest Block', 'size': 'small'},
        {'center': [17.85, 78.65], 'name': 'Vikarabad Forest Block', 'size': 'medium'},
        
        # Southern forests (Mahbubnagar region)  
        {'center': [16.45, 78.85], 'name': 'Mahbubnagar Forest Block', 'size': 'small'},
        {'center': [16.25, 78.95], 'name': 'Nagarjuna Sagar Forest Block', 'size': 'small'}
    ]
    
    # Define tribal communities and their characteristics
    tribal_communities = [
        {'name': 'Gond', 'population_range': (50, 200), 'forest_dependence': 'high'},
        {'name': 'Koya', 'population_range': (30, 150), 'forest_dependence': 'high'},
        {'name': 'Chenchu', 'population_range': (20, 80), 'forest_dependence': 'very_high'},
        {'name': 'Lambada', 'population_range': (40, 180), 'forest_dependence': 'medium'},
        {'name': 'Yerukula', 'population_range': (25, 100), 'forest_dependence': 'high'},
        {'name': 'Kolam', 'population_range': (15, 70), 'forest_dependence': 'high'},
        {'name': 'Pradhan', 'population_range': (20, 90), 'forest_dependence': 'medium'}
    ]
    
    features = []
    used_areas = []  # Track used coordinates to prevent overlaps
    
    def is_area_free(center_lat, center_lon, radius):
        """Check if an area is free from existing parcels"""
        for used in used_areas:
            distance = math.sqrt((center_lat - used['lat'])**2 + (center_lon - used['lon'])**2)
            # Much smaller buffer for tiny IFR parcels
            if radius < 0.001:  # Very small IFR parcels
                buffer_multiplier = 1.1
            elif radius < 0.003:  # Small IFR parcels  
                buffer_multiplier = 1.3
            else:  # CFR and CR parcels
                buffer_multiplier = 2.0
            
            if distance < (radius + used['radius']) * buffer_multiplier:
                return False
        return True
    
    def reserve_area(center_lat, center_lon, radius):
        """Reserve an area to prevent future overlaps"""
        used_areas.append({'lat': center_lat, 'lon': center_lon, 'radius': radius})
    
    # Generate CFR parcels (larger community forest areas)
    cfr_count = 0
    for region in forest_regions:
        center_lat, center_lon = region['center']
        region_size = region['size']
        
        # Determine number of CFR parcels per region (fewer to leave space)
        if region_size == 'large':
            num_cfr = random.randint(1, 2)  # Reduced from 2-4
        elif region_size == 'medium':
            num_cfr = random.randint(0, 1)  # Reduced from 1-2
        else:
            num_cfr = random.randint(0, 1)  # Keep same
        
        for i in range(num_cfr):
            # Find a non-overlapping location within the forest region
            attempts = 0
            while attempts < 50:  # Max attempts to find free space
                offset_lat = random.uniform(-0.15, 0.15)
                offset_lon = random.uniform(-0.15, 0.15)
                cfr_lat = center_lat + offset_lat
                cfr_lon = center_lon + offset_lon
                
                # CFR size based on community and forest density
                if region_size == 'large':
                    cfr_size = random.uniform(0.02, 0.06)  # 50-150 hectares
                elif region_size == 'medium':
                    cfr_size = random.uniform(0.015, 0.04)  # 30-100 hectares
                else:
                    cfr_size = random.uniform(0.01, 0.025)  # 20-60 hectares
                
                if is_area_free(cfr_lat, cfr_lon, cfr_size):
                    reserve_area(cfr_lat, cfr_lon, cfr_size)
                    
                    # Select a tribal community
                    community = random.choice(tribal_communities)
                    community_size = random.randint(*community['population_range'])
                    
                    # Create CFR polygon
                    cfr_coords = []
                    num_vertices = random.randint(6, 9)
                    for j in range(num_vertices):
                        angle = (j / num_vertices) * 2 * math.pi
                        radius_var = cfr_size * random.uniform(0.7, 1.3)
                        point_lat = cfr_lat + radius_var * math.cos(angle)
                        point_lon = cfr_lon + radius_var * math.sin(angle)
                        cfr_coords.append([point_lon, point_lat])
                    cfr_coords.append(cfr_coords[0])  # Close polygon
                    
                    cfr_feature = {
                        'type': 'Feature',
                        'properties': {
                            'claim_type': 'CFR',
                            'claim_id': f'CFR_{cfr_count:03d}',
                            'tribal_community': community['name'],
                            'village': f"{region['name'].replace(' Forest Block', '')} Village {i+1}",
                            'district': get_district_from_coordinates(cfr_lat, cfr_lon),
                            'claim_area_ha': round((cfr_size * 111000) ** 2 / 10000, 2),
                            'community_size': community_size,
                            'status': random.choice(['Approved', 'Pending', 'Under Review']),
                            'forest_dependence': community['forest_dependence'],
                            'year_claimed': random.randint(2008, 2023)
                        },
                        'geometry': {
                            'type': 'Polygon',
                            'coordinates': [cfr_coords]
                        }
                    }
                    features.append(cfr_feature)
                    cfr_count += 1
                    break
                
                attempts += 1
    
    print(f"Generated {cfr_count} CFR parcels")
    
    # Generate IFR parcels (individual/family parcels within or near CFR areas)
    ifr_count = 0
    cfr_features = [f for f in features if f['properties']['claim_type'] == 'CFR']
    
    for cfr_feature in cfr_features:
        cfr_coords = cfr_feature['geometry']['coordinates'][0]
        # Calculate CFR centroid
        cfr_center_lat = sum([coord[1] for coord in cfr_coords[:-1]]) / (len(cfr_coords) - 1)
        cfr_center_lon = sum([coord[0] for coord in cfr_coords[:-1]]) / (len(cfr_coords) - 1)
        
        # Generate 3-8 IFR parcels around each CFR
        num_ifr = random.randint(3, 8)
        
        for i in range(num_ifr):
            attempts = 0
            while attempts < 30:
                # Place IFR within or near CFR boundary
                offset_lat = random.uniform(-0.02, 0.02)
                offset_lon = random.uniform(-0.02, 0.02)
                ifr_lat = cfr_center_lat + offset_lat
                ifr_lon = cfr_center_lon + offset_lon
                
                # IFR size (individual/family plots - MUCH smaller)
                ifr_size = random.uniform(0.0002, 0.001)  # 0.05-0.25 hectares (very small!)
                
                if is_area_free(ifr_lat, ifr_lon, ifr_size):
                    reserve_area(ifr_lat, ifr_lon, ifr_size)
                    
                    # Create IFR polygon (simpler shape)
                    ifr_coords = []
                    num_vertices = 4  # Rectangular-ish plots
                    for j in range(num_vertices):
                        angle = (j / num_vertices) * 2 * math.pi
                        radius_var = ifr_size * random.uniform(0.8, 1.2)
                        point_lat = ifr_lat + radius_var * math.cos(angle)
                        point_lon = ifr_lon + radius_var * math.sin(angle)
                        ifr_coords.append([point_lon, point_lat])
                    ifr_coords.append(ifr_coords[0])
                    
                    ifr_feature = {
                        'type': 'Feature',
                        'properties': {
                            'claim_type': 'IFR',
                            'claim_id': f'IFR_{ifr_count:03d}',
                            'tribal_community': cfr_feature['properties']['tribal_community'],
                            'village': cfr_feature['properties']['village'],
                            'district': cfr_feature['properties']['district'],
                            'claim_area_ha': round((ifr_size * 111000) ** 2 / 10000, 2),
                            'family_head': f"Family_{i+1}",
                            'family_size': random.randint(3, 12),
                            'status': random.choice(['Approved', 'Pending', 'Under Review']),
                            'land_use': random.choice(['Cultivation', 'Homestead', 'Mixed']),
                            'year_claimed': random.randint(2008, 2023)
                        },
                        'geometry': {
                            'type': 'Polygon',
                            'coordinates': [ifr_coords]
                        }
                    }
                    features.append(ifr_feature)
                    ifr_count += 1
                    break
                
                attempts += 1
    
    # Generate standalone IFR parcels (individual/family rights) across forest regions
    for region in forest_regions:
        center_lat, center_lon = region['center']
        
        # 2-5 standalone IFR parcels per region
        num_ifr = random.randint(2, 5)
        
        for i in range(num_ifr):
            attempts = 0
            while attempts < 40:
                # Random location within region
                offset_lat = random.uniform(-0.15, 0.15)
                offset_lon = random.uniform(-0.15, 0.15)
                ifr_lat = center_lat + offset_lat
                ifr_lon = center_lon + offset_lon
                
                # Very small IFR size (individual/family plots)
                ifr_size = random.uniform(0.0001, 0.0008)  # 0.01-0.8 hectares
                
                if is_area_free(ifr_lat, ifr_lon, ifr_size):
                    reserve_area(ifr_lat, ifr_lon, ifr_size)
                    
                    # Create tiny IFR polygon
                    ifr_coords = []
                    for j in range(4):
                        angle = (j / 4) * 2 * math.pi
                        point_lat = ifr_lat + ifr_size * math.cos(angle)
                        point_lon = ifr_lon + ifr_size * math.sin(angle)
                        ifr_coords.append([point_lon, point_lat])
                    ifr_coords.append(ifr_coords[0])
                    
                    ifr_feature = {
                        'type': 'Feature',
                        'properties': {
                            'claim_type': 'IFR',
                            'claim_id': f'IFR_{ifr_count:03d}',
                            'tribal_community': random.choice([t['name'] for t in tribal_communities]),
                            'village': f"{region['name'].replace(' Forest Block', '')} Village",
                            'district': get_district_from_coordinates(ifr_lat, ifr_lon),
                            'claim_area_ha': round((ifr_size * 111000) ** 2 / 10000, 3),
                            'family_head': f"Family_{ifr_count+1}",
                            'family_size': random.randint(3, 8),
                            'status': random.choice(['Approved', 'Pending', 'Under Review']),
                            'land_use': random.choice(['Cultivation', 'Homestead', 'Collection']),
                            'year_claimed': random.randint(2008, 2023)
                        },
                        'geometry': {
                            'type': 'Polygon',
                            'coordinates': [ifr_coords]
                        }
                    }
                    features.append(ifr_feature)
                    ifr_count += 1
                    break
                
                attempts += 1
    
    # Generate CR parcels (community resources - grazing, water bodies, etc.)
    cr_count = 0
    for region in forest_regions:
        center_lat, center_lon = region['center']
        
        # 1-3 CR parcels per region
        num_cr = random.randint(1, 3)
        
        for i in range(num_cr):
            attempts = 0
            while attempts < 40:
                offset_lat = random.uniform(-0.1, 0.1)
                offset_lon = random.uniform(-0.1, 0.1)
                cr_lat = center_lat + offset_lat
                cr_lon = center_lon + offset_lon
                
                # CR size (community resources)
                cr_size = random.uniform(0.005, 0.015)  # 5-15 hectares
                
                if is_area_free(cr_lat, cr_lon, cr_size):
                    reserve_area(cr_lat, cr_lon, cr_size)
                    
                    # Create CR polygon
                    cr_coords = []
                    num_vertices = random.randint(5, 7)
                    for j in range(num_vertices):
                        angle = (j / num_vertices) * 2 * math.pi
                        radius_var = cr_size * random.uniform(0.7, 1.3)
                        point_lat = cr_lat + radius_var * math.cos(angle)
                        point_lon = cr_lon + radius_var * math.sin(angle)
                        cr_coords.append([point_lon, point_lat])
                    cr_coords.append(cr_coords[0])
                    
                    cr_resource_type = random.choice(['Grazing Land', 'Water Body', 'Sacred Grove', 'Collection Area', 'Burial Ground'])
                    
                    cr_feature = {
                        'type': 'Feature',
                        'properties': {
                            'claim_type': 'CR',
                            'claim_id': f'CR_{cr_count:03d}',
                            'tribal_community': random.choice([t['name'] for t in tribal_communities]),
                            'village': f"{region['name'].replace(' Forest Block', '')} Village",
                            'district': get_district_from_coordinates(cr_lat, cr_lon),
                            'claim_area_ha': round((cr_size * 111000) ** 2 / 10000, 2),
                            'resource_type': cr_resource_type,
                            'status': random.choice(['Approved', 'Pending', 'Under Review']),
                            'community_users': random.randint(20, 150),
                            'year_claimed': random.randint(2008, 2023)
                        },
                        'geometry': {
                            'type': 'Polygon',
                            'coordinates': [cr_coords]
                        }
                    }
                    features.append(cr_feature)
                    cr_count += 1
                    break
                
                attempts += 1
    
    # Create GeoJSON
    geojson_data = {
        'type': 'FeatureCollection',
        'features': features
    }
    
    # Save to file
    with open('output/telangana_fra_realistic.geojson', 'w') as f:
        json.dump(geojson_data, f, indent=2)
    
    print(f"Created realistic FRA data with {len(features)} parcels:")
    print(f"- CFR: {len([f for f in features if f['properties']['claim_type'] == 'CFR'])}")
    print(f"- IFR: {len([f for f in features if f['properties']['claim_type'] == 'IFR'])}")
    print(f"- CR: {len([f for f in features if f['properties']['claim_type'] == 'CR'])}")

def get_district_from_coordinates(lat, lon):
    """Map coordinates to approximate Telangana districts"""
    if lat > 18.5:
        if lon > 79.5:
            return "Komaram Bheem Asifabad"
        elif lon > 78.8:
            return "Adilabad"
        else:
            return "Nirmal"
    elif lat > 17.5:
        if lon > 80.0:
            return "Khammam"
        elif lon > 79.5:
            return "Warangal"
        elif lon > 79.0:
            return "Karimnagar"
        else:
            return "Medak"
    else:
        if lon > 79.5:
            return "Nalgonda"
        elif lon > 78.5:
            return "Mahbubnagar"
        else:
            return "Vikarabad"

if __name__ == "__main__":
    create_realistic_fra_parcels()