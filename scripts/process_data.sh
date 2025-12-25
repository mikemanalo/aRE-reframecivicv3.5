#!/bin/bash

# Define paths
INPUT_GEOJSON="CALProcure/Average_Transit_Speeds_by_Route.geojson"
INPUT_CSV="CALProcure/Average_Transit_Speeds_by_Route_Time_of_Day.csv"
OUTPUT_DIR="dashboard/data"
DISTRICTS_DIR="$OUTPUT_DIR/districts"

# Create directories
mkdir -p "$DISTRICTS_DIR"

# Copy CSV
echo "Copying CSV..."
cp "$INPUT_CSV" "$OUTPUT_DIR/transit_data.csv"

# Define districts
districts=(
    "01 - Eureka"
    "02 - Redding"
    "03 - Marysville"
    "04 - Oakland"
    "05 - San Luis Obispo"
    "06 - Fresno"
    "07 - Los Angeles"
    "08 - San Bernardino"
    "09 - Bishop"
    "10 - Stockton"
    "11 - San Diego"
    "12 - Irvine"
)

# Process each district
echo "Processing GeoJSON..."

for district in "${districts[@]}"; do
    # Create safe filename (replace spaces and dashes with underscores)
    safe_name=$(echo "$district" | tr ' -' '__')
    output_file="$DISTRICTS_DIR/${safe_name}.js"
    
    echo "Processing $district -> $output_file"
    
    # Write header
    echo 'window.loadGeoJson({ "type": "FeatureCollection", "name": "Transit Routes - '"$district"'", "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } }, "features": [' > "$output_file"
    
    # Grep features and append to file
    # We use a temporary file to handle the comma separation
    grep "$district" "$INPUT_GEOJSON" > "${output_file}.tmp"
    
    # Check if we found any lines
    if [ -s "${output_file}.tmp" ]; then
        # Append lines to output file, adding a comma to the end of each line except the last one
        # Actually, since each line is a full JSON object, we just need to join them with commas.
        # A simple way is to paste with delimiter ,
        # But the lines might be long.
        # Let's try sed to add comma to all lines, then remove the last comma.
        sed 's/$/,/' "${output_file}.tmp" | sed '$ s/,$//' >> "$output_file"
    fi
    
    # Write footer
    echo ']})' >> "$output_file"
    
    # Clean up temp file
    rm "${output_file}.tmp"
done

echo "Data processing complete!"
