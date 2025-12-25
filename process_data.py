import json
import os
import shutil
import pandas as pd

# Paths
INPUT_GEOJSON = "CALProcure/Average_Transit_Speeds_by_Route.geojson"
INPUT_CSV = "CALProcure/Average_Transit_Speeds_by_Route_Time_of_Day.csv"
OUTPUT_DIR = "dashboard/data"
DISTRICTS_DIR = os.path.join(OUTPUT_DIR, "districts")

def process_data():
    # Ensure output directories exist
    os.makedirs(DISTRICTS_DIR, exist_ok=True)

    # 1. Copy CSV file
    print(f"Copying CSV from {INPUT_CSV} to {OUTPUT_DIR}...")
    shutil.copy(INPUT_CSV, os.path.join(OUTPUT_DIR, "transit_data.csv"))

    # 2. Process GeoJSON
    print(f"Loading GeoJSON from {INPUT_GEOJSON}...")
    with open(INPUT_GEOJSON, 'r') as f:
        data = json.load(f)

    print(f"Found {len(data['features'])} features. Splitting by district...")
    
    districts = {}
    
    for feature in data['features']:
        # Extract district name, handle potential missing values
        props = feature.get('properties', {})
        district = props.get('district_name', 'Unknown')
        
        # Clean district name for filename (remove special chars)
        safe_district = "".join([c for c in district if c.isalnum() or c in (' ', '-', '_')]).strip()
        if not safe_district:
            safe_district = "Unknown"
            
        if safe_district not in districts:
            districts[safe_district] = []
        
        districts[safe_district].append(feature)

    # Save each district to a separate file
    for district_name, features in districts.items():
        output_path = os.path.join(DISTRICTS_DIR, f"{district_name}.geojson")
        
        district_collection = {
            "type": "FeatureCollection",
            "name": f"Transit Routes - {district_name}",
            "crs": data.get('crs'),
            "features": features
        }
        
        print(f"Saving {len(features)} features to {output_path}...")
        with open(output_path, 'w') as f:
            json.dump(district_collection, f)

    print("Data processing complete!")

if __name__ == "__main__":
    process_data()
