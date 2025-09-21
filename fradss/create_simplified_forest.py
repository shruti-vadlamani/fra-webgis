import json
import random

def create_simplified_forest():
    """Create a simplified version of the forest data for testing"""
    
    # Load original data
    print("Loading original forest data...")
    with open('Telangana_Forest.geojson', 'r') as f:
        original_data = json.load(f)
    
    print(f"Original data has {len(original_data['features'])} features")
    
    # Sample every 100th feature to reduce from 245k to ~2.5k features
    sampled_features = []
    for i, feature in enumerate(original_data['features']):
        if i % 100 == 0:  # Take every 100th feature
            sampled_features.append(feature)
    
    # Create simplified GeoJSON
    simplified_data = {
        'type': 'FeatureCollection',
        'features': sampled_features
    }
    
    print(f"Simplified data has {len(simplified_data['features'])} features")
    
    # Save simplified version
    with open('Telangana_Forest_Simplified.geojson', 'w') as f:
        json.dump(simplified_data, f)
    
    print("Saved simplified forest data to Telangana_Forest_Simplified.geojson")

if __name__ == "__main__":
    create_simplified_forest()