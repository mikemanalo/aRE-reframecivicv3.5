import csv
import json
import os
import math
import statistics

# Define paths
INPUT_CSV = '/Users/homegrown/Documents/_v1AREresearch/CALProcure/Average_Transit_Speeds_by_Route_Time_of_Day.csv'
OUTPUT_JSON = '/Users/homegrown/Documents/_v1AREresearch/dashboard/data/kpi_data.json'

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)

def calculate_kpis():
    print("Loading data...")
    try:
        with open(INPUT_CSV, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            all_data = list(reader)
    except FileNotFoundError:
        print(f"Error: File not found at {INPUT_CSV}")
        return

    # Filter for Los Angeles District
    data = [row for row in all_data if "Los Angeles" in row.get('district_name', '')]
    print(f"Filtered to {len(data)} rows for Los Angeles district.")

    kpis = {}

    # Helper to parse float safely
    def safe_float(val):
        try:
            return float(val)
        except (ValueError, TypeError):
            return 0.0

    # --- KPI 1: Healthcare Accessibility Velocity (Senior Communities) ---
    healthcare_keywords = ['Hospital', 'Medical', 'Senior', 'Center', 'Clinic', 'Health']
    healthcare_speeds = []
    healthcare_routes = []

    for row in data:
        route_name = row.get('route_name', '')
        time_period = row.get('time_period', '')
        speed = safe_float(row.get('speed_mph', 0))
        
        if any(keyword.lower() in route_name.lower() for keyword in healthcare_keywords):
            if time_period == 'offpeak':
                healthcare_speeds.append(speed)
                healthcare_routes.append({
                    'route_name': route_name,
                    'agency': row.get('agency', ''),
                    'speed_mph': speed
                })

    avg_healthcare_speed = statistics.mean(healthcare_speeds) if healthcare_speeds else 0
    top_healthcare_routes = sorted(healthcare_routes, key=lambda x: x['speed_mph'], reverse=True)[:5]

    kpis['healthcare_accessibility'] = {
        'title': 'Healthcare Accessibility Velocity',
        'value': round(avg_healthcare_speed, 2),
        'unit': 'MPH (Off-Peak)',
        'description': 'Average speed of routes serving healthcare and senior centers during off-peak hours.',
        'top_routes': top_healthcare_routes
    }

    # --- KPI 2: Safe Passage Reliability Score (Children & Youth) ---
    school_keywords = ['School', 'College', 'University', 'Campus', 'Student']
    school_speeds = []

    for row in data:
        route_name = row.get('route_name', '')
        time_period = row.get('time_period', '')
        speed = safe_float(row.get('speed_mph', 0))
        
        if any(keyword.lower() in route_name.lower() for keyword in school_keywords):
            if time_period == 'peak':
                school_speeds.append(speed)

    if len(school_speeds) > 1:
        speed_std = statistics.stdev(school_speeds)
        avg_school_speed = statistics.mean(school_speeds)
    else:
        speed_std = 0
        avg_school_speed = 0

    kpis['safe_passage'] = {
        'title': 'Safe Passage Reliability',
        'value': round(speed_std, 2),
        'unit': 'MPH Variability',
        'description': 'Standard deviation of speeds on school routes during peak hours. Lower means more consistent service.',
        'avg_speed': round(avg_school_speed, 2)
    }

    # --- KPI 3: 24-Hour Community Connection Rate (Car-free) ---
    # We need to group by route_id/direction/agency to compare peak vs all_day
    route_groups = {}
    
    for row in data:
        # Create a unique key for the route
        key = (row.get('route_id'), row.get('direction_id'), row.get('agency'))
        time_period = row.get('time_period')
        speed = safe_float(row.get('speed_mph', 0))
        
        if key not in route_groups:
            route_groups[key] = {}
        
        route_groups[key][time_period] = speed

    connection_diffs = []
    good_connection_count = 0
    total_routes_with_data = 0

    for key, periods in route_groups.items():
        if 'peak' in periods and 'all_day' in periods:
            diff = abs(periods['peak'] - periods['all_day'])
            connection_diffs.append(diff)
            total_routes_with_data += 1
            if diff < 5:
                good_connection_count += 1

    avg_connection_diff = statistics.mean(connection_diffs) if connection_diffs else 0
    connection_rate = (good_connection_count / total_routes_with_data * 100) if total_routes_with_data > 0 else 0

    kpis['community_connection'] = {
        'title': '24-Hour Connection Rate',
        'value': round(connection_rate, 1),
        'unit': '%',
        'description': 'Percentage of routes with consistent speeds (<5 MPH difference) between peak and all-day service.',
        'avg_diff': round(avg_connection_diff, 2)
    }

    # --- KPI 4: The 'Petunia' Index (Short-Trip Efficiency) ---
    # First, collect all lengths to find the threshold
    all_lengths = []
    for row in data:
        length = safe_float(row.get('Shape_Length', 0))
        if length > 0:
            all_lengths.append(length)
    
    if all_lengths:
        all_lengths.sort()
        # 25th percentile
        idx = int(len(all_lengths) * 0.25)
        length_threshold = all_lengths[idx]
    else:
        length_threshold = 0

    petunia_speeds = []
    for row in data:
        length = safe_float(row.get('Shape_Length', 0))
        speed = safe_float(row.get('speed_mph', 0))
        
        if length > 0 and length < length_threshold:
            petunia_speeds.append(speed)

    avg_petunia_speed = statistics.mean(petunia_speeds) if petunia_speeds else 0

    kpis['petunia_index'] = {
        'title': 'The "Petunia" Index',
        'value': round(avg_petunia_speed, 2),
        'unit': 'MPH (Local Loops)',
        'description': 'Average speed of short-distance local circulator routes.',
        'threshold_meters': round(length_threshold, 2)
    }

    # --- Save to JSON ---
    print("Saving KPIs to JSON...")
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(kpis, f, indent=4)
    print(f"Done. Output saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    calculate_kpis()
