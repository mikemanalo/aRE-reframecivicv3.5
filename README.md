# Reframe: Civic Infrastructure V3.5 - Prototype Documentation

## Project Vision: Atelier-re

**Atelier-re** is a research initiative rethinking city planning through data-driven placemaking. Rather than accepting traditional transportation metrics (ridership, on-time performance, vehicle counts), Atelier-re asks: **"What if we measured cities by how well they serve human needs?"**

This prototype demonstrates a fundamental shift in urban analytics—from infrastructure-centric to **people-centric** metrics. By reframing transit data through the lens of healthcare access, student safety, shift worker mobility, and neighborhood vitality, we reveal what truly matters: **how infrastructure shapes daily life**.

## Overview

**Reframe: Civic Infrastructure V3.5** is an interactive data visualization dashboard that transforms California transit speed data into community-centric placemaking metrics. The prototype demonstrates how existing public datasets can be reinterpreted to measure civic infrastructure quality rather than mere operational efficiency.

## Purpose & Vision

This prototype demonstrates a paradigm shift from traditional transit metrics (on-time performance, ridership) to **human-centered placemaking indicators** that measure how transit infrastructure serves community needs:

- **Healthcare Accessibility** - How quickly can seniors and patients reach medical facilities?
- **Safe Passage** - How reliable is transit for students commuting to school?
- **24-Hour Connection** - Does transit serve shift workers and late-night activities?
- **Neighborhood Circulation** - How well do local routes connect residents to nearby amenities?

## Theoretical Foundations

### From Mobility to Accessibility

This work builds on the **mobility-to-accessibility paradigm shift** in transportation planning. Traditional planning prioritizes vehicle movement (mobility), while contemporary approaches focus on reaching destinations (accessibility).

**Key Influences**:
- **Jan Gehl** - *Cities for People* (2010): Human-scale urban design prioritizing pedestrian and transit experiences
- **Jeff Speck** - *Walkable City* (2012): The importance of transit quality in creating livable neighborhoods
- **Project for Public Spaces** - Placemaking methodology emphasizing community-centered design

### Placemaking Metrics

Traditional transportation metrics measure **system performance**:
- Vehicle throughput
- Travel time reliability
- Cost efficiency

Atelier-re's metrics measure **place quality**:
- Can vulnerable populations access healthcare?
- Do students have reliable school transit?
- Does transit support diverse work schedules?
- Can residents access local amenities car-free?

This shift aligns with the **New Urbanism** and **Complete Streets** movements, which advocate for infrastructure that serves human needs rather than vehicular efficiency.

### Data Justice & Equity

By highlighting healthcare access and educational reliability, these metrics center **equity** in infrastructure evaluation. Communities with poor healthcare accessibility scores or unreliable school transit face structural disadvantages that traditional metrics obscure.

This approach draws from:
- **Data feminism** (D'Ignazio & Klein, 2020): Making visible what is typically invisible in data
- **Transportation equity** research: Examining who benefits from infrastructure investments
- **Environmental justice**: Recognizing that infrastructure quality varies by community demographics

---

## Technical Architecture

### Frontend Stack

- **HTML5** - Semantic structure with accessibility considerations
- **CSS3** - Custom design system with CSS variables
- **Vanilla JavaScript** - No framework dependencies for maximum performance
- **Leaflet.js** - Interactive mapping library for route visualization

### Design System

#### Typography
- **Headings**: Playfair Display (serif) - elegant, editorial aesthetic
- **Body**: DM Sans (sans-serif) - clean, highly legible

#### Color Palette
```css
--bg-color: #051b2c           /* Deep navy background */
--text-primary: #ffffff        /* White text */
--text-secondary: #a0a0a0      /* Gray secondary text */
--accent-gold: #d4af37         /* Gold accents */
--accent-cyan: #00ced1 → #4682b4  /* Cyan gradient */
--accent-red: #ff6347 → #cd5c5c   /* Red gradient */
```

#### Visual Elements
- **Grid Background**: Subtle 100px grid overlay for architectural feel
- **Glassmorphism Cards**: Semi-transparent cards with blur effects
- **Decorative Shapes**: Gradient circles, arches, and organic shapes
- **Micro-animations**: Hover effects, card lifts, route highlights

### Data Architecture

#### Data Sources
1. **`kpi_data_all_districts.js`** - Aggregated KPI metrics for all 12 California districts
2. **`district_index.js`** - Maps district names to route data file paths
3. **`data/districts/*.js`** - Individual district GeoJSON route data (dynamically loaded)

#### Data Flow
```
User selects district
    ↓
Load KPI data from ALL_DISTRICT_DATA
    ↓
Update 4 widget cards with metrics
    ↓
Dynamically load district route GeoJSON
    ↓
Render color-coded routes on map
    ↓
Enable interactive popups
```

## Key Features

### 1. District Selector
- Dropdown menu with all 12 California Caltrans districts
- Default selection: "07 - Los Angeles"
- Synchronized updates across widgets and map

### 2. Four KPI Widgets (2×2 Grid)

#### Healthcare Accessibility Velocity
- **Metric**: Average speed (MPH) of healthcare-serving routes during off-peak hours
- **Route Keywords**: Medical, Hospital, Health, Senior, Clinic
- **Visual**: Cyan gradient decoration
- **Extra Data**: Top 3 fastest healthcare routes

#### Safe Passage Reliability
- **Metric**: Standard deviation of speeds on school routes during peak hours
- **Route Keywords**: School, University, College, Campus
- **Visual**: Gold flower-shaped decoration
- **Extra Data**: Average speed of school routes

#### 24-Hour Connection Rate
- **Metric**: Percentage of routes with <5 MPH speed difference between peak/off-peak
- **Indicates**: All-day service consistency
- **Visual**: Gold solid circle decoration
- **Extra Data**: Average speed difference

#### The "Petunia" Index
- **Metric**: Average speed of short-distance local routes (<0.15° length ≈ 10 miles)
- **Purpose**: Measures neighborhood-scale circulation quality
- **Visual**: Red arch-shaped decoration
- **Extra Data**: Distance threshold in meters

### 3. Interactive Map

#### Map Features
- **Base Layer**: CartoDB Dark Matter tileset (dark aesthetic)
- **Default View**: Los Angeles (34.0522°N, 118.2437°W) at zoom level 10
- **Scale Control**: Imperial units (miles/feet) in bottom-right
- **Auto-fit**: Automatically zooms to selected district's route bounds

#### Route Visualization
- **Color Coding**:
  - 🟢 **Green (#00ff88)**: Fast routes (>15 mph)
  - 🟡 **Gold (#ffd700)**: Medium routes (10-15 mph)
  - 🔴 **Red (#ff6b6b)**: Slow routes (<10 mph)
- **Line Weight**: 1.5px (0.5pt) for clean, uncluttered display
- **Opacity**: 80% for layered route visibility

#### Interactive Popups
Click any route to view:
- Route name
- Transit agency
- Average speed (MPH)
- Time period (Peak/Off-Peak)

#### Route Highlighting
- Clicked routes temporarily increase to 3px weight and 100% opacity
- Auto-reset after 2 seconds

### 4. Metric Explanations Section

Full-width card below the dashboard containing:
- Detailed calculation methodology for each KPI
- "Why it matters" context for community impact
- Data source attribution (Caltrans)
- Data references with update frequency

## File Structure

```
dashboard/
├── placemaking_v35.html       # Main HTML structure
├── placemaking_v35.css        # Complete design system
├── placemaking_v35.js         # Application logic
├── data/
│   ├── kpi_data_all_districts.js    # All district KPI metrics
│   ├── districts/
│   │   ├── district_index.js        # Route file index
│   │   ├── district_01_routes.js    # District 01 routes
│   │   ├── district_02_routes.js    # District 02 routes
│   │   └── ...                      # Districts 03-12
```

## Performance Optimizations

### Dynamic Route Loading
- **Problem**: Loading all district routes at once (12 files × ~1-5MB each) causes performance issues
- **Solution**: Dynamically load only the selected district's route data
- **Implementation**:
  1. Remove previous district script from DOM
  2. Clear `window.CURRENT_DISTRICT_ROUTES`
  3. Inject new `<script>` tag with district-specific route file
  4. Render routes on `onload` callback

### Benefits
- ✅ Reduced initial page load time
- ✅ Lower memory footprint
- ✅ No CORS issues (all data served from same origin)
- ✅ Instant district switching

## Responsive Design

### Breakpoints

#### Desktop (>1200px)
- Dashboard: 50% widgets (2×2 grid) | 50% map
- Map height: 600px

#### Tablet (768px - 1200px)
- Dashboard: Stacked layout (widgets above map)
- Map height: 500px

#### Mobile (<768px)
- Widgets: Single column grid
- Reduced padding and font sizes
- Map height: 500px

## User Interactions

### Hover Effects
- Cards lift 5px on hover
- Border color brightens from 10% to 30% opacity
- Smooth 0.3s transitions

### Click Interactions
- District dropdown triggers full data refresh
- Route clicks show popup and temporary highlight
- All interactions provide visual feedback

## Research Methodology & Data Sources

### Primary Data Source

**California Department of Transportation (Caltrans)**  
*Average Transit Speeds by Route Dataset*

- **Publisher**: California Department of Transportation (Caltrans)
- **Access**: California Open Data Portal (data.ca.gov)
- **Dataset URL**: https://data.ca.gov/dataset/average-transit-speeds-by-route
- **Format**: GeoJSON (215.9 MB), CSV, KML, Shapefile
- **Created**: November 19, 2025
- **Last Updated**: December 22, 2025
- **Coverage**: All 12 Caltrans districts across California
- **License**: Public Domain (California Open Data)

**Dataset Description**:  
The dataset provides average transit speeds and trip counts for specific routes and directions across California's public transit systems. Each feature includes:
- Route name and ID
- Transit agency
- District name and number
- Average speed (MPH)
- Time period (Peak/Off-Peak)
- Geographic route geometry (LineString)
- Route length (Shape_Length in degrees)

**Citation**:  
California Department of Transportation. (2025). *Average Transit Speeds by Route* [Dataset]. California Open Data Portal. https://data.ca.gov/dataset/average-transit-speeds-by-route

### Research Approach

#### 1. Conceptual Framework Development

The research began with a fundamental question: **How can we measure the civic value of transportation infrastructure?**

Traditional transit metrics focus on operational efficiency:
- On-time performance
- Ridership numbers
- Cost per passenger mile
- Vehicle utilization rates

Atelier-re's approach inverts this framework by asking: **"What human needs does transit serve?"** This led to four conceptual domains:

1. **Healthcare Access** - Can vulnerable populations (seniors, patients) reach medical care efficiently?
2. **Educational Equity** - Do students have reliable, predictable transit to schools?
3. **Economic Mobility** - Does transit serve shift workers and non-traditional schedules?
4. **Neighborhood Vitality** - Can residents access local amenities without cars?

#### 2. Metric Development Process

Each metric was developed through an iterative process:

**Step 1: Domain Identification**  
Identified key community needs that transit should serve (healthcare, education, employment, local circulation).

**Step 2: Proxy Selection**  
Determined which data attributes could serve as proxies for these needs:
- Route names containing keywords (e.g., "Hospital", "School")
- Time period variations (peak vs. off-peak)
- Route geometry (length as proxy for local vs. regional service)

**Step 3: Statistical Methodology**  
Selected appropriate statistical measures:
- **Mean** for central tendency (Healthcare, Petunia)
- **Standard deviation** for reliability/consistency (Safe Passage)
- **Percentage** for coverage metrics (24-Hour Connection)

**Step 4: Validation**  
Cross-referenced results against known transit patterns and district characteristics.

#### 3. Analytical Methods

**Data Processing Pipeline**:
```
Raw GeoJSON (215.9 MB)
    ↓
Filter by District (12 districts)
    ↓
Apply Keyword Filters (route names)
    ↓
Apply Time Period Filters (peak/off-peak)
    ↓
Apply Geometric Filters (route length)
    ↓
Calculate Statistical Aggregates
    ↓
Generate KPI Values + Supporting Data
```

**Tools Used**:
- **Python 3.x** - Data processing and analysis
- **JSON module** - GeoJSON parsing
- **Statistics module** - Statistical calculations (mean, stdev)
- **Custom scripts** - KPI calculation logic

### KPI Calculation Methodologies

#### Healthcare Accessibility Velocity

**Rationale**: Healthcare access is critical for aging populations and those with chronic conditions. Off-peak speeds matter because medical appointments often occur outside rush hours.

**Calculation**:
```python
keywords = ["Medical", "Hospital", "Health", "Senior", "Clinic"]
Filter routes: route_name contains ANY keyword
Filter time: time_period == "offpeak"
Calculate: MEAN(speed_mph)
Return: Top 5 fastest routes
```

**Assumptions**:
- Route names accurately reflect service destinations
- Off-peak hours represent typical medical appointment times
- Speed is a reasonable proxy for accessibility

**Limitations**:
- Does not account for route frequency
- Cannot distinguish between different types of medical facilities
- Keyword matching may miss routes without explicit healthcare naming

#### Safe Passage Reliability

**Rationale**: Students need predictable transit to arrive on time for classes. High variability in speeds suggests unreliable service that can impact educational outcomes.

**Calculation**:
```python
keywords = ["School", "University", "College", "Campus"]
Filter routes: route_name contains ANY keyword
Filter time: time_period contains "peak"
Calculate: STDEV(speed_mph)
Return: Standard deviation + average speed
```

**Assumptions**:
- Peak hours align with school commute times
- Lower variability indicates more reliable service
- School-named routes primarily serve students

**Limitations**:
- Does not account for school start/end time variations
- Cannot distinguish K-12 from higher education routes
- Variability may reflect route diversity rather than unreliability

#### 24-Hour Connection Rate

**Rationale**: Shift workers, healthcare workers, and service industry employees need consistent transit throughout the day. High peak/off-peak speed differences indicate car-dependent design.

**Calculation**:
```python
For each route_id:
    peak_speed = speed where time_period contains "peak"
    offpeak_speed = speed where time_period == "offpeak"
    speed_diff = ABS(peak_speed - offpeak_speed)
    
Count routes where speed_diff < 5 MPH
Calculate: (consistent_routes / total_routes) × 100
Return: Percentage + average speed difference
```

**Assumptions**:
- <5 MPH difference indicates consistent service
- Routes with consistent speeds serve all-day needs
- Peak/off-peak comparison captures service equity

**Limitations**:
- Does not account for frequency differences
- 5 MPH threshold is somewhat arbitrary
- Cannot distinguish intentional express service from congestion

#### The "Petunia" Index

**Rationale**: Named for neighborhood-scale circulation, this metric measures the quality of local "loop" routes that connect residents to nearby parks, shops, and community centers. Short routes indicate local service rather than regional commuting.

**Calculation**:
```python
THRESHOLD = 0.15  # degrees (~10 miles)
Filter routes: Shape_Length < THRESHOLD
Calculate: MEAN(speed_mph)
Return: Average speed + threshold distance
```

**Assumptions**:
- Route length correlates with local vs. regional service
- 0.15 degrees (~10 miles) is appropriate threshold for "local"
- Speed on short routes indicates circulation quality

**Limitations**:
- Length alone doesn't guarantee local service character
- Does not account for route circuitousness
- May include short regional connectors

### Data Quality Considerations

**Strengths**:
- ✅ Official government data source (Caltrans)
- ✅ Comprehensive statewide coverage
- ✅ Standardized measurement methodology
- ✅ Regular updates (most recent: December 2025)
- ✅ Multiple time periods (peak/off-peak)

**Limitations**:
- ⚠️ Route name keywords may not capture all relevant routes
- ⚠️ Speed alone doesn't capture frequency or reliability
- ⚠️ No demographic or ridership data linkage
- ⚠️ Cannot distinguish between different causes of slow speeds
- ⚠️ Time periods may not align perfectly with community needs

### Validation & Cross-Referencing

**District-Level Validation**:
- Los Angeles (District 07) shows expected patterns: high healthcare speeds, moderate school reliability
- Rural districts show different patterns: fewer healthcare routes, higher connection rates
- Results align with known transit system characteristics

**Comparative Analysis**:
- Metrics vary significantly across districts, suggesting real differences in transit quality
- Urban districts generally show more healthcare routes but lower connection rates
- Rural districts show higher speed consistency but fewer specialized routes

### Future Research Directions

**Potential Enhancements**:
1. **Demographic Integration**: Link metrics to census data for equity analysis
2. **Temporal Analysis**: Track metric changes over time
3. **Frequency Weighting**: Incorporate service frequency into calculations
4. **Destination Validation**: Ground-truth route names against actual destinations
5. **Comparative Metrics**: Benchmark against other states/regions
6. **Community Validation**: Survey residents to validate metric relevance

**Alternative Data Sources**:
- **General Transit Feed Specification (GTFS)** - For frequency and schedule data
- **Census Transportation Planning Products (CTPP)** - For demographic analysis
- **California Health Interview Survey (CHIS)** - For healthcare access patterns
- **School district data** - For student commute patterns

---

## Data Methodology (Technical Implementation)

### KPI Calculations

#### Healthcare Accessibility
```
Filter routes by healthcare keywords
→ Filter for off-peak time periods
→ Calculate average speed
→ Return top 3 fastest routes
```

#### Safe Passage Reliability
```
Filter routes by school keywords
→ Filter for peak time periods
→ Calculate standard deviation of speeds
→ Return average speed
```

#### 24-Hour Connection
```
For each route:
  Calculate |peak_speed - off_peak_speed|
→ Count routes with difference < 5 MPH
→ Return percentage
```

#### Petunia Index
```
Filter routes by Shape_Length < 0.15 degrees
→ Calculate average speed
→ Return threshold distance in meters
```

## Design Philosophy

### Architectural Minimalism
- Clean grid system inspired by architectural blueprints
- Generous white space for breathing room
- Subtle decorative elements that don't distract

### Editorial Aesthetic
- Serif headings evoke magazine/journal quality
- Italicized "Civic" creates emphasis
- Lowercase "atelier-re" logo suggests design studio

### Data Transparency
- Every metric includes full explanation
- Calculation methodology documented
- Data sources clearly attributed
- No "black box" analytics

## Future Enhancements

### Potential Features
- [ ] Time-series charts showing metric trends
- [ ] Comparative district analysis
- [ ] Export functionality for reports
- [ ] Custom route filtering by agency
- [ ] Heatmap overlay for speed density
- [ ] Mobile app version
- [ ] Real-time data integration

### Technical Improvements
- [ ] Service worker for offline functionality
- [ ] Progressive Web App (PWA) capabilities
- [ ] Accessibility audit (WCAG 2.1 AA compliance)
- [ ] Performance monitoring
- [ ] Error boundary handling

## Browser Compatibility

### Tested & Supported
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### Required Features
- CSS Grid
- CSS Custom Properties (variables)
- ES6 JavaScript (arrow functions, template literals)
- Fetch API (for potential future enhancements)

## Accessibility Considerations

### Current Implementation
- Semantic HTML5 elements (`<header>`, `<main>`, `<section>`)
- Descriptive labels for form controls
- Sufficient color contrast ratios
- Keyboard-navigable dropdown

### Recommended Additions
- ARIA labels for interactive map elements
- Focus indicators for keyboard navigation
- Screen reader announcements for data updates
- Alt text for decorative elements

## Credits & Attribution

### Data Source
**California Department of Transportation (Caltrans)**  
Average Transit Speeds by Route dataset

### Design & Development
**atelier-re**  
Research and experimentation in civic data visualization

### Open Source Libraries
- **Leaflet.js** - BSD 2-Clause License
- **CartoDB Basemaps** - CC BY 3.0
- **Google Fonts** - Open Font License

---

## Quick Start Guide

### Running Locally

1. **Clone or download** the repository
2. **Navigate** to the dashboard directory
3. **Open** `placemaking_v35.html` in a modern web browser
4. **Select** a district from the dropdown
5. **Explore** the metrics and interactive map

### No Build Process Required
This is a static HTML/CSS/JS application with no dependencies beyond CDN-hosted libraries.

### Recommended Local Server (Optional)
For best performance and to avoid potential CORS issues:

```bash
# Using Python 3
python3 -m http.server 8000

# Using Node.js
npx http-server

# Using PHP
php -S localhost:8000
```

Then visit: `http://localhost:8000/placemaking_v35.html`

---

## Version History

### V3.5 (Current)
- ✨ Dynamic district route loading for performance
- ✨ Refined design system with decorative elements
- ✨ Interactive map with color-coded routes
- ✨ Comprehensive metric explanations
- ✨ Responsive layout optimizations

### V3.0
- Initial implementation of 4-KPI dashboard
- Static route loading (performance issues)
- Basic map integration

### V2.0
- Prototype with 3 metrics
- No map visualization

### V1.0
- Concept demonstration
- Single district only

---

## References & Bibliography

### Primary Data Source

California Department of Transportation. (2025). *Average Transit Speeds by Route* [Dataset]. California Open Data Portal. Retrieved December 24, 2024, from https://data.ca.gov/dataset/average-transit-speeds-by-route

### Urban Planning & Placemaking Theory

D'Ignazio, C., & Klein, L. F. (2020). *Data Feminism*. MIT Press.

Gehl, J. (2010). *Cities for People*. Island Press.

Project for Public Spaces. (n.d.). *What is Placemaking?* Retrieved from https://www.pps.org/article/what-is-placemaking

Speck, J. (2012). *Walkable City: How Downtown Can Save America, One Step at a Time*. North Point Press.

### Transportation Equity & Accessibility

Karner, A., & Niemeier, D. (2013). Civil rights guidance and equity analysis methods for regional transportation plans: A critical review of literature and practice. *Journal of Transport Geography*, 33, 126-134.

Litman, T. (2022). *Evaluating Transportation Equity: Guidance for Incorporating Distributional Impacts in Transport Planning*. Victoria Transport Policy Institute.

Pereira, R. H., Schwanen, T., & Banister, D. (2017). Distributive justice and equity in transportation. *Transport Reviews*, 37(2), 170-191.

### Data Visualization & Civic Technology

Few, S. (2012). *Show Me the Numbers: Designing Tables and Graphs to Enlighten* (2nd ed.). Analytics Press.

Tufte, E. R. (2001). *The Visual Display of Quantitative Information* (2nd ed.). Graphics Press.

### Related California Open Data Resources

California Department of Transportation. (2025). *Average Transit Speeds by Stop* [Dataset]. California Open Data Portal. https://data.ca.gov/dataset/average-transit-speeds-by-stop

California Department of Transportation. (2025). *California Transit Routes* [Dataset]. California Open Data Portal. https://data.ca.gov/dataset/california-transit-routes

California Department of Transportation. (2025). *California Transit Stops* [Dataset]. California Open Data Portal. https://data.ca.gov/dataset/california-transit-stops

### Technical Documentation

Leaflet Contributors. (2024). *Leaflet: An open-source JavaScript library for mobile-friendly interactive maps*. Retrieved from https://leafletjs.com/

CartoDB. (2024). *CARTO Basemaps*. Retrieved from https://carto.com/basemaps/

---

**Last Updated**: December 24, 2024  
**Prototype Version**: 3.5  
**Status**: Active Development

