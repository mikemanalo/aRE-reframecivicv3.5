import json

INPUT_GEOJSON = '/Users/homegrown/Documents/_v1AREresearch/CALProcure/Average_Transit_Speeds_by_Route.geojson'

def list_districts():
    print(f"Loading GeoJSON from {INPUT_GEOJSON}...")
    with open(INPUT_GEOJSON, 'r') as f:
        data = json.load(f)
    
    districts = set()
    for feature in data['features']:
        district = feature.get('properties', {}).get('district_name', '')
        if district:
            districts.add(district)
    
    sorted_districts = sorted(districts)
    print(f"\nFound {len(sorted_districts)} districts:\n")
    for d in sorted_districts:
        print(f"  - {d}")
    
    return sorted_districts

if __name__ == "__main__":
    list_districts()
