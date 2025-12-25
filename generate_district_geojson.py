import json
import os

# Configuration
INPUT_GEOJSON = '/Users/homegrown/Documents/_v1AREresearch/CALProcure/Average_Transit_Speeds_by_Route.geojson'
OUTPUT_DIR = '/Users/homegrown/Documents/_v1AREresearch/dashboard/data/districts'

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

def generate_district_geojson_files():
    data = load_geojson(INPUT_GEOJSON)
    if not data:
        return

    all_features = data['features']
    print(f"Total features: {len(all_features)}")
    
    districts = get_all_districts(all_features)
    print(f"Found {len(districts)} districts")
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Generate a GeoJSON file for each district
    for district in districts:
        print(f"Processing {district}...")
        filtered_features = filter_by_district(all_features, district)
        
        # Create a safe filename
        safe_name = district.replace(' - ', '_').replace(' ', '_').lower()
        output_file = os.path.join(OUTPUT_DIR, f"{safe_name}.geojson")
        
        district_geojson = {
            "type": "FeatureCollection",
            "features": filtered_features
        }
        
        with open(output_file, 'w') as f:
            json.dump(district_geojson, f)
        
        print(f"  Saved {len(filtered_features)} features to {safe_name}.geojson")
    
    # Also create a district index file for easy loading
    district_index = {}
    for district in districts:
        safe_name = district.replace(' - ', '_').replace(' ', '_').lower()
        district_index[district] = f"data/districts/{safe_name}.geojson"
    
    index_file = os.path.join(OUTPUT_DIR, 'district_index.json')
    with open(index_file, 'w') as f:
        json.dump(district_index, f, indent=2)
    
    print(f"\nCreated district index at {index_file}")
    print("Done.")

if __name__ == "__main__":
    generate_district_geojson_files()
