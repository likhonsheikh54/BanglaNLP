document.addEventListener('DOMContentLoaded', function() {
    // Dataset Growth Chart
    const growthCtx = document.getElementById('dataset-growth');
    if (growthCtx) {
        new Chart(growthCtx, {
            type: 'line',
            data: {
                labels: ['Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
                datasets: [{
                    label: 'Total Sentence Pairs',
                    data: [20000, 45000, 75000, 95000, 110000, 120000],
                    borderColor: '#4299e1',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Dataset Growth Over Time'
                    }
                }
            }
        });
    }

    // Source Distribution Chart
    const sourceCtx = document.getElementById('source-distribution');
    if (sourceCtx) {
        new Chart(sourceCtx, {
            type: 'doughnut',
            data: {
                labels: ['Prothom Alo', 'Ittefaq', 'Bangla Tribune', 'BD Pratidin', 'Janakantha', 'Jai Jaidin'],
                datasets: [{
                    data: [30000, 25000, 20000, 15000, 15000, 15000],
                    backgroundColor: [
                        '#4299e1',
                        '#48bb78',
                        '#ed64a6',
                        '#ecc94b',
                        '#9f7aea',
                        '#f687b3'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Distribution by Source'
                    }
                }
            }
        });
    }
});

// Add source distribution chart
function createSourceChart() {
    const ctx = document.getElementById('source-chart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Prothom Alo', 'Ittefaq', 'Bangla Tribune', 'BD Pratidin', 'Janakantha', 'Jai Jaidin'],
            datasets: [{
                data: [30, 25, 20, 15, 15, 15],
                backgroundColor: [
                    '#4299e1',
                    '#48bb78',
                    '#ed64a6',
                    '#ecc94b',
                    '#9f7aea',
                    '#f687b3'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                title: {
                    display: true,
                    text: 'Distribution by Source (%)'
                }
            }
        }
    });
}

// Add quality metrics chart
function createMetricsChart() {
    const ctx = document.getElementById('quality-metrics');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: [
                'Language Detection',
                'Alignment Score',
                'Content Quality',
                'Translation Accuracy',
                'Topic Coverage'
            ],
            datasets: [{
                label: 'Current Version',
                data: [99, 92, 95, 90, 85],
                backgroundColor: 'rgba(66, 153, 225, 0.2)',
                borderColor: '#4299e1',
                pointBackgroundColor: '#4299e1'
            }]
        },
        options: {
            responsive: true,
            scales: {
                r: {
                    min: 0,
                    max: 100,
                    ticks: {
                        stepSize: 20
                    }
                }
            }
        }
    });
}

// Initialize all charts
document.addEventListener('DOMContentLoaded', () => {
    createDatasetGrowthChart();
    createSourceChart();
    createMetricsChart();
    createQualityMetricsChart();
});
