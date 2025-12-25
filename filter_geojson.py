import json
import os

INPUT_GEOJSON = '/Users/homegrown/Documents/_v1AREresearch/CALProcure/Average_Transit_Speeds_by_Route.geojson'
OUTPUT_GEOJSON = '/Users/homegrown/Documents/_v1AREresearch/dashboard/data/la_routes.geojson'

def filter_geojson():
    print(f"Loading GeoJSON from {INPUT_GEOJSON}...")
    try:
        with open(INPUT_GEOJSON, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {INPUT_GEOJSON}")
        return

    print(f"Total features: {len(data['features'])}")
    
    # Inspect first feature properties
    if data['features']:
        print("First feature properties:", json.dumps(data['features'][0]['properties'], indent=2))

    # Filter for Los Angeles District
    # Matching the logic used in the CSV filter: "Los Angeles" in district_name
    filtered_features = []
    for feature in data['features']:
        props = feature.get('properties', {})
        district = props.get('district_name', '')
        if district and "Los Angeles" in district:
            filtered_features.append(feature)
            
    data['features'] = filtered_features
    print(f"Filtered to {len(filtered_features)} features for Los Angeles district.")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_GEOJSON), exist_ok=True)
    
    print(f"Saving filtered GeoJSON to {OUTPUT_GEOJSON}...")
    with open(OUTPUT_GEOJSON, 'w') as f:
        json.dump(data, f)
    print("Done.")

if __name__ == "__main__":
    filter_geojson()
