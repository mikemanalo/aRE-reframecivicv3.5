import json
import os

# Configuration
INPUT_GEOJSON = '/Users/homegrown/Documents/_v1AREresearch/CALProcure/Average_Transit_Speeds_by_Route.geojson'
OUTPUT_JS = '/Users/homegrown/Documents/_v1AREresearch/dashboard/data/district_routes.js'

def load_geojson(path):
    print(f"Loading GeoJSON from {path}...")
    with open(path, 'r') as f:
        return json.load(f)

def get_all_districts(features):
    districts = set()
    for f in features:
        d_name = f.get('properties', {}).get('district_name', '')
        if d_name:
            districts.add(d_name)
    return sorted(districts)

def filter_by_district(features, district_name):
    return [f for f in features if f.get('properties', {}).get('district_name', '') == district_name]

def generate_combined_district_js():
    """Generate a single JS file with all district routes data"""
    data = load_geojson(INPUT_GEOJSON)
    if not data:
        return

    all_features = data['features']
    print(f"Total features: {len(all_features)}")
    
    districts = get_all_districts(all_features)
    print(f"Found {len(districts)} districts")
    
    # Create a dictionary with all district data
    all_district_routes = {}
    
    for district in districts:
        print(f"Processing {district}...")
        filtered_features = filter_by_district(all_features, district)
        
        all_district_routes[district] = {
            "type": "FeatureCollection",
            "features": filtered_features
        }
        
        print(f"  Added {len(filtered_features)} features")
    
    # Write as JavaScript file
    print(f"\nSaving all district routes to {OUTPUT_JS}...")
    with open(OUTPUT_JS, 'w') as f:
        json_str = json.dumps(all_district_routes, indent=2)
        js_content = f"window.DISTRICT_ROUTES = {json_str};\n"
        f.write(js_content)
    
    print("Done.")

if __name__ == "__main__":
    generate_combined_district_js()
