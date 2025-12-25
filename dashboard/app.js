// Global variables
let map;
let geoJsonLayer;
let csvData = [];
let agencyChart;
let timeChart;

// Initialize Dashboard
document.addEventListener('DOMContentLoaded', () => {
    initMap();
    loadCSV();
});

function initMap() {
    // Initialize map centered on California
    map = L.map('map').setView([37.0, -120.0], 6);

    // Add OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
}

function loadCSV() {
    // Check if data is available in global variable
    if (typeof window.transitDataCsv === 'undefined') {
        console.error('CSV data not found. Make sure transit_data.js is loaded.');
        document.getElementById('stats-content').innerHTML = '<p class="error">Error loading data.</p>';
        return;
    }

    Papa.parse(window.transitDataCsv, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
        complete: function (results) {
            csvData = results.data;
            populateDistricts();
        },
        error: function (error) {
            console.error('Error parsing CSV:', error);
            document.getElementById('stats-content').innerHTML = '<p class="error">Error parsing data.</p>';
        }
    });
}

function populateDistricts() {
    const districtSelect = document.getElementById('district-select');

    // Extract unique districts
    const districts = [...new Set(csvData.map(row => row.district_name).filter(d => d))].sort();

    // Clear loading option
    districtSelect.innerHTML = '<option value="">Select a District</option>';

    districts.forEach(district => {
        const option = document.createElement('option');
        option.value = district;
        option.textContent = district;
        districtSelect.appendChild(option);
    });

    // Add event listener
    districtSelect.addEventListener('change', (e) => {
        const selectedDistrict = e.target.value;
        if (selectedDistrict) {
            updateDashboard(selectedDistrict);
        }
    });
}

function updateDashboard(district) {
    updateStats(district);
    updateCharts(district);
    updateMap(district);
}

function updateStats(district) {
    const districtData = csvData.filter(row => row.district_name === district);
    if (districtData.length === 0) return;

    const avgSpeed = districtData.reduce((sum, row) => sum + (row.speed_mph || 0), 0) / districtData.length;
    const routeCount = new Set(districtData.map(row => row.route_id)).size;
    const agencyCount = new Set(districtData.map(row => row.agency)).size;

    const statsHtml = `
        <p><strong>District:</strong> ${district}</p>
        <p><strong>Avg Speed:</strong> ${avgSpeed.toFixed(2)} mph</p>
        <p><strong>Routes:</strong> ${routeCount}</p>
        <p><strong>Agencies:</strong> ${agencyCount}</p>
    `;

    document.getElementById('stats-content').innerHTML = statsHtml;
}

function updateCharts(district) {
    const districtData = csvData.filter(row => row.district_name === district);

    // Prepare Agency Data
    const agencySpeeds = {};
    const agencyCounts = {};

    districtData.forEach(row => {
        if (!row.agency) return;
        if (!agencySpeeds[row.agency]) {
            agencySpeeds[row.agency] = 0;
            agencyCounts[row.agency] = 0;
        }
        agencySpeeds[row.agency] += row.speed_mph || 0;
        agencyCounts[row.agency]++;
    });

    const agencyLabels = Object.keys(agencySpeeds);
    const agencyValues = agencyLabels.map(a => agencySpeeds[a] / agencyCounts[a]);

    // Prepare Time Period Data
    const timeSpeeds = {};
    const timeCounts = {};

    districtData.forEach(row => {
        if (!row.time_period) return;
        if (!timeSpeeds[row.time_period]) {
            timeSpeeds[row.time_period] = 0;
            timeCounts[row.time_period] = 0;
        }
        timeSpeeds[row.time_period] += row.speed_mph || 0;
        timeCounts[row.time_period]++;
    });

    const timeLabels = Object.keys(timeSpeeds);
    const timeValues = timeLabels.map(t => timeSpeeds[t] / timeCounts[t]);

    // Update Agency Chart
    const agencyCtx = document.getElementById('agencyChart').getContext('2d');
    if (agencyChart) agencyChart.destroy();

    agencyChart = new Chart(agencyCtx, {
        type: 'bar',
        data: {
            labels: agencyLabels,
            datasets: [{
                label: 'Avg Speed by Agency (mph)',
                data: agencyValues,
                backgroundColor: 'rgba(52, 152, 219, 0.6)',
                borderColor: 'rgba(52, 152, 219, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });

    // Update Time Chart
    const timeCtx = document.getElementById('timeChart').getContext('2d');
    if (timeChart) timeChart.destroy();

    timeChart = new Chart(timeCtx, {
        type: 'doughnut',
        data: {
            labels: timeLabels,
            datasets: [{
                label: 'Avg Speed by Time Period',
                data: timeValues,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

// Global function to be called by the loaded script
window.loadGeoJson = function (data) {
    if (geoJsonLayer) {
        map.removeLayer(geoJsonLayer);
    }

    geoJsonLayer = L.geoJSON(data, {
        style: function (feature) {
            return {
                color: getColor(feature.properties.speed_mph),
                weight: 3,
                opacity: 0.7
            };
        },
        onEachFeature: function (feature, layer) {
            const props = feature.properties;
            layer.bindPopup(`
                <strong>Route:</strong> ${props.route_name || props.route_id}<br>
                <strong>Agency:</strong> ${props.agency}<br>
                <strong>Speed:</strong> ${props.speed_mph.toFixed(1)} mph<br>
                <strong>Time:</strong> ${props.time_period}
            `);
        }
    }).addTo(map);

    // Fit map to bounds
    if (geoJsonLayer.getLayers().length > 0) {
        map.fitBounds(geoJsonLayer.getBounds());
    }
};

function updateMap(district) {
    // Construct filename from district name
    const safeName = district.replace(/[ -]/g, '_');
    const scriptPath = `data/districts/${safeName}.js`;

    // Remove existing district script if any (optional, but cleaner)
    const existingScript = document.getElementById('district-data-script');
    if (existingScript) {
        existingScript.remove();
    }

    // Load new script
    const script = document.createElement('script');
    script.src = scriptPath;
    script.id = 'district-data-script';
    script.onerror = function () {
        console.error('Error loading script:', scriptPath);
        alert('Could not load map data for this district.');
    };
    document.body.appendChild(script);
}

function getColor(speed) {
    return speed > 30 ? '#2ecc71' :
        speed > 15 ? '#f1c40f' :
            '#e74c3c';
}
