window.KPI_DATA = {
    "healthcare_accessibility": {
        "title": "Healthcare Accessibility Velocity",
        "value": 14.58,
        "unit": "MPH (Off-Peak)",
        "description": "Average speed of routes serving healthcare and senior centers during off-peak hours.",
        "top_routes": [
            {
                "route_name": "Puente Hills Mall ? Whittier Hospital ? La Habra",
                "agency": "City of Duarte",
                "speed_mph": 17.27259119
            },
            {
                "route_name": "Puente Hills Mall ? Whittier Hospital ? La Habra",
                "agency": "Foothill Transit",
                "speed_mph": 17.27259119
            },
            {
                "route_name": "Puente Hills Mall ? Whittier Hospital ? La Habra",
                "agency": "City of Duarte",
                "speed_mph": 16.96234462
            },
            {
                "route_name": "Puente Hills Mall ? Whittier Hospital ? La Habra",
                "agency": "Foothill Transit",
                "speed_mph": 16.96234462
            },
            {
                "route_name": "Santa Paula B Route (SP Hospital)",
                "agency": "City of Ojai",
                "speed_mph": 14.55144491
            }
        ]
    },
    "safe_passage": {
        "title": "Safe Passage Reliability",
        "value": 2.91,
        "unit": "MPH Variability",
        "description": "Standard deviation of speeds on school routes during peak hours.",
        "avg_speed": 12.25
    },
    "community_connection": {
        "title": "24-Hour Connection Rate",
        "value": 91.2,
        "unit": "%",
        "description": "Percentage of routes with consistent speeds (<5 MPH difference) between peak and all-day service.",
        "avg_diff": 1.8
    },
    "petunia_index": {
        "title": "The \"Petunia\" Index",
        "value": 11.59,
        "unit": "MPH (Local Loops)",
        "description": "Average speed of short-distance local circulator routes.",
        "threshold_meters": 16000
    }
};
