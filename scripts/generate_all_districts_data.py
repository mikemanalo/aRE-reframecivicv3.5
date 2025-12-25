import json
import os
import statistics

# Configuration
INPUT_GEOJSON = '/Users/homegrown/Documents/_v1AREresearch/CALProcure/Average_Transit_Speeds_by_Route.geojson'
OUTPUT_JS = '/Users/homegrown/Documents/_v1AREresearch/dashboard/data/kpi_data_all_districts.js'

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

def calculate_healthcare_kpi(features):
    keywords = ["Medical", "Hospital", "Health", "Senior", "Clinic"]
    relevant_routes = []
    
    for f in features:
        props = f.get('properties', {})
        name = props.get('route_name', '')
        time_period = props.get('time_period', '').lower()
        
        if time_period == 'offpeak' and any(k.lower() in name.lower() for k in keywords):
            relevant_routes.append({
                "route_name": name,
                "agency": props.get('agency', 'Unknown'),
                "speed_mph": props.get('speed_mph', 0)
            })
            
    if not relevant_routes:
        return {"value": 0, "unit": "MPH (Off-Peak)", "description": "No healthcare routes found.", "top_routes": []}
        
    avg_speed = statistics.mean([r['speed_mph'] for r in relevant_routes])
    relevant_routes.sort(key=lambda x: x['speed_mph'], reverse=True)
    
    return {
        "title": "Healthcare Accessibility Velocity",
        "value": round(avg_speed, 2),
        "unit": "MPH (Off-Peak)",
        "description": "Average speed of routes serving healthcare and senior centers during off-peak hours.",
        "top_routes": relevant_routes[:5]
    }

def calculate_safe_passage_kpi(features):
    keywords = ["School", "University", "College", "Campus"]
    speeds = []
    
    for f in features:
        props = f.get('properties', {})
        name = props.get('route_name', '')
        time_period = props.get('time_period', '').lower()
        
        if "peak" in time_period and any(k.lower() in name.lower() for k in keywords):
             speeds.append(props.get('speed_mph', 0))
             
    if len(speeds) < 2:
        return {"value": 0, "unit": "MPH Variability", "description": "Insufficient school route data.", "avg_speed": 0}
        
    std_dev = statistics.stdev(speeds)
    avg_speed = statistics.mean(speeds)
    
    return {
        "title": "Safe Passage Reliability",
        "value": round(std_dev, 2),
        "unit": "MPH Variability",
        "description": "Standard deviation of speeds on school routes during peak hours.",
        "avg_speed": round(avg_speed, 2)
    }

def calculate_connection_kpi(features):
    routes = {}
    for f in features:
        props = f.get('properties', {})
        rid = props.get('route_id')
        tp = props.get('time_period', '').lower()
        speed = props.get('speed_mph', 0)
        
        if rid not in routes:
            routes[rid] = {}
        routes[rid][tp] = speed
        
    consistent_count = 0
    total_comparable = 0
    diffs = []
    
    for rid, data in routes.items():
        peak_speed = data.get('peak') or data.get('am_peak') or data.get('pm_peak')
        offpeak_speed = data.get('offpeak')
        
        if peak_speed and offpeak_speed:
            diff = abs(peak_speed - offpeak_speed)
            diffs.append(diff)
            total_comparable += 1
            if diff < 5:
                consistent_count += 1
                
    if total_comparable == 0:
        return {"value": 0, "unit": "%", "description": "No comparable peak/off-peak data.", "avg_diff": 0}
        
    percentage = (consistent_count / total_comparable) * 100
    avg_diff = statistics.mean(diffs)
    
    return {
        "title": "24-Hour Connection Rate",
        "value": round(percentage, 1),
        "unit": "%",
        "description": "Percentage of routes with consistent speeds (<5 MPH difference) between peak and all-day service.",
        "avg_diff": round(avg_diff, 2)
    }

def calculate_petunia_kpi(features):
    THRESHOLD = 0.15
    short_route_speeds = []
    
    for f in features:
        props = f.get('properties', {})
        length = props.get('Shape_Length', 0)
        speed = props.get('speed_mph', 0)
        
        if length < THRESHOLD and speed > 0:
            short_route_speeds.append(speed)
            
    if not short_route_speeds:
        return {"value": 0, "unit": "MPH (Local Loops)", "description": "No local loop routes found.", "threshold_meters": 0}
        
    avg_speed = statistics.mean(short_route_speeds)
    
    return {
        "title": "The \"Petunia\" Index",
        "value": round(avg_speed, 2),
        "unit": "MPH (Local Loops)",
        "description": "Average speed of short-distance local circulator routes.",
        "threshold_meters": 16000
    }

def generate_all_districts_data():
    data = load_geojson(INPUT_GEOJSON)
    if not data:
        return

    all_features = data['features']
    print(f"Total features: {len(all_features)}")
    
    districts = get_all_districts(all_features)
    print(f"Found {len(districts)} districts")
    
    all_district_data = {}
    
    for district in districts:
        print(f"Processing {district}...")
        filtered_features = filter_by_district(all_features, district)
        
        all_district_data[district] = {
            "healthcare_accessibility": calculate_healthcare_kpi(filtered_features),
            "safe_passage": calculate_safe_passage_kpi(filtered_features),
            "community_connection": calculate_connection_kpi(filtered_features),
            "petunia_index": calculate_petunia_kpi(filtered_features)
        }
    
    os.makedirs(os.path.dirname(OUTPUT_JS), exist_ok=True)
    
    print(f"\nSaving all district data to {OUTPUT_JS}...")
    with open(OUTPUT_JS, 'w') as f:
        json_str = json.dumps(all_district_data, indent=4)
        js_content = f"window.ALL_DISTRICT_DATA = {json_str};\n"
        f.write(js_content)
    print("Done.")

if __name__ == "__main__":
    generate_all_districts_data()
