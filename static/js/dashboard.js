document.addEventListener('DOMContentLoaded', () => {
    if (!window.CHART_DATA) return;

    const chartDefaults = {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                labels: {
                    color: '#a0a0b8',
                    font: { family: 'Inter', size: 12 },
                    padding: 16,
                },
            },
        },
    };

    const statusCtx = document.getElementById('statusChart');
    if (statusCtx) {
        const statusData = window.CHART_DATA.byStatus || {};
        const statusLabels = Object.keys(statusData).map((s) => s.charAt(0).toUpperCase() + s.slice(1));
        const statusValues = Object.values(statusData);

        new Chart(statusCtx, {
            type: 'doughnut',
            data: {
                labels: statusLabels.length ? statusLabels : ['No Data'],
                datasets: [{
                    data: statusValues.length ? statusValues : [1],
                    backgroundColor: ['#10b981', '#f59e0b', '#8b5cf6', '#6366f1'],
                    borderColor: 'rgba(255, 255, 255, 0.05)',
                    borderWidth: 2,
                }],
            },
            options: {
                ...chartDefaults,
                cutout: '65%',
                plugins: {
                    ...chartDefaults.plugins,
                    legend: { position: 'bottom', labels: chartDefaults.plugins.legend.labels },
                },
            },
        });
    }

    const serviceCtx = document.getElementById('serviceChart');
    if (serviceCtx) {
        const serviceData = window.CHART_DATA.byService || {};
        const serviceLabels = Object.keys(serviceData);
        const serviceValues = Object.values(serviceData);

        new Chart(serviceCtx, {
            type: 'bar',
            data: {
                labels: serviceLabels.length ? serviceLabels : ['No Data'],
                datasets: [{
                    label: 'Leads',
                    data: serviceValues.length ? serviceValues : [0],
                    backgroundColor: 'rgba(99, 102, 241, 0.6)',
                    borderColor: '#6366f1',
                    borderWidth: 1,
                    borderRadius: 6,
                }],
            },
            options: {
                ...chartDefaults,
                scales: {
                    x: {
                        ticks: {
                            color: '#6b6b80',
                            font: { size: 10 },
                            maxRotation: 45,
                            minRotation: 45,
                        },
                        grid: { color: 'rgba(255, 255, 255, 0.03)' },
                    },
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: '#6b6b80',
                            stepSize: 1,
                        },
                        grid: { color: 'rgba(255, 255, 255, 0.03)' },
                    },
                },
                plugins: {
                    legend: { display: false },
                },
            },
        });
    }
});
