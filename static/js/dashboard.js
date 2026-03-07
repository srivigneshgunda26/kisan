// Dashboard JavaScript

let categoryPieChart = null;
let cropBarChart = null;

// Load dashboard data on page load
document.addEventListener('DOMContentLoaded', function() {
    loadDashboardData();
    
    // Refresh every 30 seconds
    setInterval(loadDashboardData, 30000);
});

// Load dashboard statistics
async function loadDashboardData() {
    try {
        const response = await fetch('/api/statistics');
        const data = await response.json();
        
        if (data.success) {
            updateStatistics(data);
            updateCharts(data);
            updateRecentQueries(data.recent_queries);
        }
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

// Update statistics cards
function updateStatistics(data) {
    document.getElementById('totalEntries').textContent = data.total_entries.toLocaleString();
    document.getElementById('totalQueries').textContent = data.total_queries.toLocaleString();
    document.getElementById('totalCategories').textContent = Object.keys(data.categories).length;
    document.getElementById('totalCrops').textContent = Object.keys(data.crops).length;
}

// Update charts
function updateCharts(data) {
    // Category Pie Chart
    const categoryCtx = document.getElementById('categoryPieChart').getContext('2d');
    
    if (categoryPieChart) {
        categoryPieChart.destroy();
    }
    
    const categoryLabels = Object.keys(data.categories);
    const categoryData = Object.values(data.categories);
    
    categoryPieChart = new Chart(categoryCtx, {
        type: 'pie',
        data: {
            labels: categoryLabels,
            datasets: [{
                data: categoryData,
                backgroundColor: [
                    '#4CAF50',
                    '#2196F3',
                    '#FF9800',
                    '#F44336',
                    '#9C27B0',
                    '#00BCD4',
                    '#FFEB3B',
                    '#795548'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'right'
                },
                title: {
                    display: true,
                    text: 'Distribution by Category'
                }
            }
        }
    });
    
    // Crop Bar Chart - Top 10
    const cropCtx = document.getElementById('cropBarChart').getContext('2d');
    
    if (cropBarChart) {
        cropBarChart.destroy();
    }
    
    // Sort crops by count and take top 10
    const sortedCrops = Object.entries(data.crops)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);
    
    const cropLabels = sortedCrops.map(item => item[0]);
    const cropData = sortedCrops.map(item => item[1]);
    
    cropBarChart = new Chart(cropCtx, {
        type: 'bar',
        data: {
            labels: cropLabels,
            datasets: [{
                label: 'Number of Entries',
                data: cropData,
                backgroundColor: '#4CAF50',
                borderColor: '#2E7D32',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Top 10 Crops by Entries'
                }
            }
        }
    });
}

// Update recent queries table
function updateRecentQueries(queries) {
    const tbody = document.getElementById('recentQueriesTable');
    
    if (!queries || queries.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No queries yet</td></tr>';
        return;
    }
    
    tbody.innerHTML = '';
    
    queries.reverse().forEach(query => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><small>${query.timestamp}</small></td>
            <td>${query.query}</td>
            <td><span class="badge bg-primary">${query.results_count}</span></td>
            <td>
                ${query.categories.map(cat => `<span class="badge bg-success me-1">${cat}</span>`).join('')}
            </td>
            <td>
                ${query.crops.map(crop => `<span class="badge bg-info me-1">${crop}</span>`).join('')}
            </td>
        `;
        tbody.appendChild(row);
    });
}
