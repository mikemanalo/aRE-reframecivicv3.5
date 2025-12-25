document.addEventListener('DOMContentLoaded', () => {
    // Initialize Map
    const map = L.map('map').setView([37.7749, -122.4194], 6); // California view

    // Dark Matter Tile Layer (CartoDB)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    // Get district selector
    const districtSelect = document.getElementById('district-select');

    // Load Data from Global Variable
    if (window.ALL_DISTRICT_DATA) {
        // Populate dropdown with districts
        const districts = Object.keys(window.ALL_DISTRICT_DATA).sort();
        districtSelect.innerHTML = '';

        districts.forEach(district => {
            const option = document.createElement('option');
            option.value = district;
            option.textContent = district;
            districtSelect.appendChild(option);
        });

        // Set default to Los Angeles
        const defaultDistrict = '07 - Los Angeles';
        if (districts.includes(defaultDistrict)) {
            districtSelect.value = defaultDistrict;
        } else {
            districtSelect.value = districts[0];
        }

        // Load initial data
        updateWidgets(window.ALL_DISTRICT_DATA[districtSelect.value]);

        // Add change event listener
        districtSelect.addEventListener('change', (e) => {
            const selectedDistrict = e.target.value;
            updateWidgets(window.ALL_DISTRICT_DATA[selectedDistrict]);
        });
    } else {
        console.error('District data not found. Ensure data/kpi_data_all_districts.js is loaded.');
        districtSelect.innerHTML = '<option value="">Error loading data</option>';
    }

    function updateWidgets(data) {
        // KPI 1: Healthcare
        if (data.healthcare_accessibility) {
            document.getElementById('healthcare-value').textContent = data.healthcare_accessibility.value;
            document.getElementById('healthcare-unit').textContent = data.healthcare_accessibility.unit;
            document.getElementById('healthcare-desc').textContent = data.healthcare_accessibility.description;

            const topRoutes = data.healthcare_accessibility.top_routes || [];
            if (topRoutes.length > 0) {
                let html = '<div style="margin-bottom:0.5rem; font-weight:bold; color:var(--accent-cyan-start)">Top Routes:</div><ul>';
                topRoutes.slice(0, 3).forEach(route => {
                    html += `<li><span class="label" style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:150px;" title="${route.route_name}">${route.route_name}</span> <span class="val">${Math.round(route.speed_mph)} mph</span></li>`;
                });
                html += '</ul>';
                document.getElementById('healthcare-extra').innerHTML = html;
            } else {
                document.getElementById('healthcare-extra').innerHTML = '<p style="font-size:0.85rem; color:var(--text-secondary);">No healthcare routes found.</p>';
            }
        }

        // KPI 2: Safe Passage
        if (data.safe_passage) {
            document.getElementById('safe-passage-value').textContent = data.safe_passage.value;
            document.getElementById('safe-passage-unit').textContent = data.safe_passage.unit;
            document.getElementById('safe-passage-desc').textContent = data.safe_passage.description;

            if (data.safe_passage.avg_speed > 0) {
                document.getElementById('safe-passage-extra').innerHTML = `
                    <ul>
                        <li><span class="label">Avg Speed:</span> <span class="val">${data.safe_passage.avg_speed} mph</span></li>
                    </ul>
                `;
            } else {
                document.getElementById('safe-passage-extra').innerHTML = '<p style="font-size:0.85rem; color:var(--text-secondary);">No school routes found.</p>';
            }
        }

        // KPI 3: Connection
        if (data.community_connection) {
            document.getElementById('connection-value').textContent = data.community_connection.value;
            document.getElementById('connection-unit').textContent = data.community_connection.unit;
            document.getElementById('connection-desc').textContent = data.community_connection.description;

            if (data.community_connection.avg_diff > 0) {
                document.getElementById('connection-extra').innerHTML = `
                    <ul>
                        <li><span class="label">Avg Speed Diff:</span> <span class="val">${data.community_connection.avg_diff} mph</span></li>
                    </ul>
                `;
            } else {
                document.getElementById('connection-extra').innerHTML = '<p style="font-size:0.85rem; color:var(--text-secondary);">Insufficient data.</p>';
            }
        }

        // KPI 4: Petunia
        if (data.petunia_index) {
            document.getElementById('petunia-value').textContent = data.petunia_index.value;
            document.getElementById('petunia-unit').textContent = data.petunia_index.unit;
            document.getElementById('petunia-desc').textContent = data.petunia_index.description;

            if (data.petunia_index.value > 0) {
                document.getElementById('petunia-extra').innerHTML = `
                    <ul>
                        <li><span class="label">Distance Threshold:</span> <span class="val">${Math.round(data.petunia_index.threshold_meters)} m</span></li>
                    </ul>
                `;
            } else {
                document.getElementById('petunia-extra').innerHTML = '<p style="font-size:0.85rem; color:var(--text-secondary);">No local loops found.</p>';
            }
        }
    }
});
