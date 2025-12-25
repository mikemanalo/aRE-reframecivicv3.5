document.addEventListener('DOMContentLoaded', () => {
    // Initialize Map
    const map = L.map('map').setView([37.7749, -122.4194], 7); // Default to Bay Area/NorCal view

    // Dark Matter Tile Layer (CartoDB)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    // Load Data from Global Variable
    if (window.KPI_DATA) {
        updateWidgets(window.KPI_DATA);
    } else {
        console.error('KPI Data not found. Ensure data/kpi_data.js is loaded.');
    }

    function updateWidgets(data) {
        // Helper to animate numbers
        const animateValue = (id, start, end, duration) => {
            const obj = document.getElementById(id);
            let startTimestamp = null;
            const step = (timestamp) => {
                if (!startTimestamp) startTimestamp = timestamp;
                const progress = Math.min((timestamp - startTimestamp) / duration, 1);
                obj.innerHTML = Math.floor(progress * (end - start) + start);
                if (progress < 1) {
                    window.requestAnimationFrame(step);
                } else {
                    obj.innerHTML = end; // Ensure final value is exact
                }
            };
            window.requestAnimationFrame(step);
        };

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
            }
        }

        // KPI 2: Safe Passage
        if (data.safe_passage) {
            document.getElementById('safe-passage-value').textContent = data.safe_passage.value;
            document.getElementById('safe-passage-unit').textContent = data.safe_passage.unit;
            document.getElementById('safe-passage-desc').textContent = data.safe_passage.description;

            document.getElementById('safe-passage-extra').innerHTML = `
                <ul>
                    <li><span class="label">Avg Speed:</span> <span class="val">${data.safe_passage.avg_speed} mph</span></li>
                </ul>
            `;
        }

        // KPI 3: Connection
        if (data.community_connection) {
            document.getElementById('connection-value').textContent = data.community_connection.value;
            document.getElementById('connection-unit').textContent = data.community_connection.unit;
            document.getElementById('connection-desc').textContent = data.community_connection.description;

            document.getElementById('connection-extra').innerHTML = `
                <ul>
                    <li><span class="label">Avg Speed Diff:</span> <span class="val">${data.community_connection.avg_diff} mph</span></li>
                </ul>
            `;
        }

        // KPI 4: Petunia
        if (data.petunia_index) {
            document.getElementById('petunia-value').textContent = data.petunia_index.value;
            document.getElementById('petunia-unit').textContent = data.petunia_index.unit;
            document.getElementById('petunia-desc').textContent = data.petunia_index.description;

            document.getElementById('petunia-extra').innerHTML = `
                <ul>
                    <li><span class="label">Distance Threshold:</span> <span class="val">${Math.round(data.petunia_index.threshold_meters)} m</span></li>
                </ul>
            `;
        }
    }
});
