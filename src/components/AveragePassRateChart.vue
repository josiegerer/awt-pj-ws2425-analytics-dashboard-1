<template>
  <div>
    <h3>Average Pass Rate</h3>
    <Bar :data="passRateData" :options="chartOptions" />
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

// Register required components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default {
  name: 'AveragePassRateChart',
  components: {
    Bar
  },
  data() {
    return {
      // Example data for average pass rate
      passRateData: {
        labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'], // Example time period (e.g., weeks)
        datasets: [
          {
            label: 'Pass Rate (%)',
            data: [75, 80, 85, 90], // Example pass rates
            backgroundColor: '#66BB6A',
            borderColor: '#388E3C',
            borderWidth: 1,
          },
        ],
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false, // Allow chart to resize, but we'll fix height
        plugins: {
          title: {
            display: true,
            text: 'Average Pass Rate Over Time',
          },
          tooltip: {
            mode: 'nearest',
            intersect: false,
          },
        },
        scales: {
          x: {
            title: {
              display: true,
              text: 'Weeks',
            },
          },
          y: {
            title: {
              display: true,
              text: 'Pass Rate (%)',
            },
            beginAtZero: true, // Ensures the Y-axis starts at 0
            min: 0,  // Ensures Y-axis doesn't go below 0
            max: 100, // Set a static max value for the Y-axis
            stepSize: 10, // Set the step size for ticks (interval between ticks)
          },
        },
      },
    };
  },
};
</script>

<style scoped>
/* Ensure the chart has a fixed height and width to maintain static size */
div {
  height: 400px; /* Fixed height */
  width: 100%; /* Full width */
}

h3 {
  text-align: center;
}
</style>
