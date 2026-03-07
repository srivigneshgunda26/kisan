// Main Application JavaScript

let categoryChart = null;
let cropChart = null;

// Load sample queries on page load
document.addEventListener('DOMContentLoaded', function() {
    loadSampleQueries();
    
    // Event listeners
    document.getElementById('searchBtn').addEventListener('click', handleSearch);
    document.getElementById('clearBtn').addEventListener('click', handleClear);
    document.getElementById('queryInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSearch();
        }
    });
});

// Load sample queries
async function loadSampleQueries() {
    try {
        const response = await fetch('/api/sample-queries');
        const samples = await response.json();
        
        const container = document.getElementById('sampleQueriesContainer');
        container.innerHTML = '';
        
        samples.forEach(sample => {
            const btn = document.createElement('button');
            btn.className = 'sample-query-btn';
            btn.innerHTML = `
                <span class="icon">${sample.icon}</span>
                <span class="text">${sample.query}</span>
                <span class="category">${sample.category}</span>
            `;
            btn.onclick = () => {
                document.getElementById('queryInput').value = sample.query;
                handleSearch();
            };
            container.appendChild(btn);
        });
    } catch (error) {
        console.error('Error loading sample queries:', error);
    }
}

// Handle search
async function handleSearch() {
    const query = document.getElementById('queryInput').value.trim();
    
    if (!query) {
        alert('Please enter a query');
        return;
    }
    
    const onlineMode = document.getElementById('onlineModeToggle').checked;
    
    // Show loading
    document.getElementById('loadingIndicator').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';
    
    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query,
                online_mode: onlineMode
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Search failed');
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        alert('Error: ' + error.message);
        console.error('Search error:', error);
    } finally {
        document.getElementById('loadingIndicator').style.display = 'none';
    }
}

// Display results
function displayResults(data) {
    // Show results section
    document.getElementById('resultsSection').style.display = 'block';
    
    // Update statistics cards
    document.getElementById('statResults').textContent = data.statistics.total_results;
    
    // Calculate relevance (inverse of average distance, normalized to percentage)
    const relevance = Math.max(0, Math.min(100, 100 - (data.statistics.avg_distance * 10)));
    document.getElementById('statAccuracy').textContent = Math.round(relevance) + '%';
    
    document.getElementById('statCategories').textContent = Object.keys(data.statistics.categories).length;
    document.getElementById('statCrops').textContent = Object.keys(data.statistics.crops).length;
    
    // Display offline answer
    document.getElementById('offlineAnswer').innerHTML = formatAnswer(data.offline_answer);
    
    // Display online answer
    const onlineAnswerDiv = document.getElementById('onlineAnswer');
    if (data.online_answer) {
        onlineAnswerDiv.innerHTML = formatAnswer(data.online_answer);
    } else {
        onlineAnswerDiv.innerHTML = '<p class="text-muted"><i class="fas fa-info-circle"></i> Online mode is disabled. Enable it in settings to get AI-generated answers.</p>';
    }
    
    // Display retrieved entries
    displayRetrievedEntries(data.results);
    
    // Update charts
    updateCharts(data.statistics);
    
    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Format answer text
function formatAnswer(text) {
    // Escape HTML first to prevent XSS
    const escapeHtml = (str) => {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    };
    
    // Don't escape, we want to render HTML
    // text = escapeHtml(text);
    
    // Convert bold text: **text** or * **text** *
    text = text.replace(/\*\s*\*\*([^*]+)\*\*\s*\*/g, '<strong>$1</strong>');
    text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    
    // Convert italic text: *text*
    text = text.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    
    // Convert bullet points: - item or * item
    text = text.replace(/^[\*\-]\s+(.+)$/gm, '<li>$1</li>');
    
    // Convert numbered lists: 1. item
    text = text.replace(/^(\d+)\.\s+(.+)$/gm, '<li>$2</li>');
    
    // Wrap consecutive list items in ul/ol
    text = text.replace(/(<li>.*<\/li>\s*)+/gs, function(match) {
        // Check if it's a numbered list (original text had numbers)
        return '<ul>' + match + '</ul>';
    });
    
    // Convert line breaks
    text = text.replace(/\n\n+/g, '</p><p>');
    text = text.replace(/\n/g, '<br>');
    
    // Wrap in paragraph if not already wrapped
    if (!text.startsWith('<ul>') && !text.startsWith('<ol>') && !text.startsWith('<p>')) {
        text = '<p>' + text + '</p>';
    }
    
    // Clean up empty paragraphs
    text = text.replace(/<p><\/p>/g, '');
    text = text.replace(/<p>\s*<\/p>/g, '');
    
    return text;
}

// Display retrieved entries
function displayRetrievedEntries(results) {
    const container = document.getElementById('entriesList');
    container.innerHTML = '';
    
    results.forEach((result, index) => {
        const entryDiv = document.createElement('div');
        entryDiv.className = 'entry-card';
        entryDiv.innerHTML = `
            <div class="question"><i class="fas fa-question-circle"></i> ${result.question}</div>
            <div class="answer">${result.answer}</div>
            <div class="metadata">
                <span class="badge bg-primary">${result.category || 'General'}</span>
                <span class="badge bg-success">${result.crop || 'General'}</span>
                <span class="badge bg-info">Relevance: ${(100 - result.distance * 10).toFixed(1)}%</span>
            </div>
        `;
        container.appendChild(entryDiv);
    });
}

// Update charts
function updateCharts(statistics) {
    // Category Chart
    const categoryCtx = document.getElementById('categoryChart').getContext('2d');
    
    if (categoryChart) {
        categoryChart.destroy();
    }
    
    const categoryLabels = Object.keys(statistics.categories);
    const categoryData = Object.values(statistics.categories);
    
    categoryChart = new Chart(categoryCtx, {
        type: 'doughnut',
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
                    '#00BCD4'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
    
    // Crop Chart
    const cropCtx = document.getElementById('cropChart').getContext('2d');
    
    if (cropChart) {
        cropChart.destroy();
    }
    
    const cropLabels = Object.keys(statistics.crops);
    const cropData = Object.values(statistics.crops);
    
    cropChart = new Chart(cropCtx, {
        type: 'bar',
        data: {
            labels: cropLabels,
            datasets: [{
                label: 'Occurrences',
                data: cropData,
                backgroundColor: '#4CAF50',
                borderColor: '#2E7D32',
                borderWidth: 1
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
                }
            }
        }
    });
}

// Handle clear
function handleClear() {
    document.getElementById('queryInput').value = '';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('queryInput').focus();
}
