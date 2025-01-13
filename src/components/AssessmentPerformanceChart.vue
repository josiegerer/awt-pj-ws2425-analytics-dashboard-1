<template>
    <div class="assessment-performance-chart">
      <h3>Assessment Performance Over Time</h3>
      <LineChart :data="chartData" :options="chartOptions" />
    </div>
  </template>
  
  <script>
  import { Line } from 'vue-chartjs';
  import { Chart as ChartJS, Title, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement } from 'chart.js';
  
  // Register required chart.js components
  ChartJS.register(Title, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement);
  
  export default {
    name: 'AssessmentPointsChart',
    components: {
      LineChart: Line
    },
    data() {
      return {
        chartData: {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], // Months
          datasets: [
            {
              label: 'Points Achieved',
              data: [10, 25, 40, 55, 60, 63, 75, 88], // Static data for points achieved each month
              borderColor: '#42A5F5', // Line color
              backgroundColor: 'rgba(66, 165, 245, 0.2)', // Fill color under the line
              fill: true, // Fill the area under the line
              tension: 0.4 // Smooth line
            }
          ]
        },
        chartOptions: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            tooltip: {
              callbacks: {
                label: function (context) {
                  return `Points: ${context.raw}`;
                }
              }
            },
            legend: {
            display: true, // Ensure the legend is displayed
            position: 'bottom', // Position legend at the bottom
            labels: {
              color: '#000', // Change legend label color
              font: {
                size: 12, // Adjust font size of legend labels
              },
            },
          },
        },
          
          scales: {
            x: {
              title: {
                display: true,
                text: 'Months'
              }
            },
            y: {
              title: {
                display: true,
                text: 'Assessment Points',
              },
              beginAtZero: true,
              min: 0,
              max: 100,
            }
          }
        }
      };
    }
  };
  </script>
  
  <style scoped>
  h3 {
    text-align: left;
    font-size: 15px;
    color: black;
    margin-bottom: 20px;
  }
  </style>
  