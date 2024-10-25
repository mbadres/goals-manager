document.addEventListener('DOMContentLoaded', function() {
    const chartCanvas = document.getElementById('progressChart');
    if (!chartCanvas) return;

    fetch('/api/average-scores')
        .then(response => response.json())
        .then(datasets => {
            new Chart(chartCanvas, {
                type: 'line',
                data: {
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'day',
                                displayFormats: {
                                    day: 'MMM d'
                                }
                            },
                            title: {
                                display: true,
                                text: 'Date'
                            }
                        },
                        y: {
                            min: 0,
                            max: 10,
                            title: {
                                display: true,
                                text: 'Score'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            position: 'top',
                            labels: {
                                usePointStyle: true,
                                pointStyle: 'circle'
                            }
                        },
                        tooltip: {
                            callbacks: {
                                title: function(context) {
                                    const date = new Date(context[0].raw.x);
                                    return date.toLocaleDateString();
                                },
                                label: function(context) {
                                    return `${context.dataset.label}: ${context.raw.y}`;
                                }
                            }
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode: 'nearest'
                    }
                }
            });
        })
        .catch(error => console.error('Error loading chart data:', error));
});