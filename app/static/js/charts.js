var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: [], // Dates
        datasets: [{
            label: 'Calories',
            data: [], // Data
            backgroundColor: [], // Colors for each segment
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
