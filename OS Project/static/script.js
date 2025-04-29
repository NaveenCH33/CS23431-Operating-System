document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded');
    const form = document.getElementById('simulationForm');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        console.log('Form submitted');
        
        const pages = document.getElementById('pages').value;
        const frames = document.getElementById('frames').value;
        console.log('Input values:', { pages, frames });
        
        try {
            const response = await fetch('/simulate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    pages: pages,
                    frames: frames
                })
            });
            
            const data = await response.json();
            console.log('Received data:', data);
            displayResults(data);
        } catch (error) {
            console.error('Error:', error);
        }
    });
});

function displayResults(data) {
    console.log('Displaying results');
    const results = document.getElementById('results');
    results.style.display = 'block';
    
    // Clear previous results
    document.getElementById('fifoTable').querySelector('tbody').innerHTML = '';
    document.getElementById('lruTable').querySelector('tbody').innerHTML = '';
    document.getElementById('optimalTable').querySelector('tbody').innerHTML = '';
    
    // Display steps for each algorithm
    displayAlgorithmSteps('fifoTable', data.algorithms.fifo.steps);
    displayAlgorithmSteps('lruTable', data.algorithms.lru.steps);
    displayAlgorithmSteps('optimalTable', data.algorithms.optimal.steps);
    
    // Create performance graphs
    createPageFaultsChart(data);
    createMemorySizeChart(data);
    createHitRateChart(data);
}

function displayAlgorithmSteps(tableId, steps) {
    const tbody = document.getElementById(tableId).querySelector('tbody');
    
    steps.forEach(step => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${step.step}</td>
            <td>${step.page}</td>
            <td><span class="memory-state">${step.memory_state.join(' ')}</span></td>
            <td><span class="${step.is_hit ? 'page-hit' : 'page-fault'}">${step.is_hit ? 'HIT' : 'MISS'}</span></td>
        `;
        tbody.appendChild(row);
    });
}

function createPageFaultsChart(data) {
    const ctx = document.getElementById('pageFaultsChart');
    if (!ctx) {
        console.error('Could not find pageFaultsChart canvas');
        return;
    }

    const steps = data.algorithms.fifo.steps.map(step => step.step);
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: steps,
            datasets: [
                {
                    label: 'FIFO',
                    data: data.algorithms.fifo.steps.map(step => step.page_faults),
                    borderColor: '#FF6384',
                    backgroundColor: '#FF6384',
                    tension: 0.1
                },
                {
                    label: 'LRU',
                    data: data.algorithms.lru.steps.map(step => step.page_faults),
                    borderColor: '#36A2EB',
                    backgroundColor: '#36A2EB',
                    tension: 0.1
                },
                {
                    label: 'Optimal',
                    data: data.algorithms.optimal.steps.map(step => step.page_faults),
                    borderColor: '#4BC0C0',
                    backgroundColor: '#4BC0C0',
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Page Faults Over Time'
                }
            }
        }
    });
}

function createMemorySizeChart(data) {
    const ctx = document.getElementById('memorySizeChart');
    if (!ctx) {
        console.error('Could not find memorySizeChart canvas');
        return;
    }

    const steps = data.algorithms.fifo.steps.map(step => step.step);
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: steps,
            datasets: [
                {
                    label: 'FIFO',
                    data: data.algorithms.fifo.steps.map(step => step.memory_state.length),
                    borderColor: '#FF6384',
                    backgroundColor: '#FF6384',
                    tension: 0.1
                },
                {
                    label: 'LRU',
                    data: data.algorithms.lru.steps.map(step => step.memory_state.length),
                    borderColor: '#36A2EB',
                    backgroundColor: '#36A2EB',
                    tension: 0.1
                },
                {
                    label: 'Optimal',
                    data: data.algorithms.optimal.steps.map(step => step.memory_state.length),
                    borderColor: '#4BC0C0',
                    backgroundColor: '#4BC0C0',
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Memory State Size'
                }
            }
        }
    });
}

function createHitRateChart(data) {
    const ctx = document.getElementById('hitRateChart');
    if (!ctx) {
        console.error('Could not find hitRateChart canvas');
        return;
    }

    const algorithms = ['FIFO', 'LRU', 'Optimal'];
    const hitRates = [
        data.algorithms.fifo.hit_rate,
        data.algorithms.lru.hit_rate,
        data.algorithms.optimal.hit_rate
    ];

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: algorithms,
            datasets: [{
                label: 'Hit Rate (%)',
                data: hitRates,
                backgroundColor: ['#FF6384', '#36A2EB', '#4BC0C0']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Hit Rate Comparison'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}
