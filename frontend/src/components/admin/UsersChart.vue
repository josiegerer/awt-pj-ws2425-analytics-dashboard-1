<template>
    <div class="chart">
      <Line
        :data="chartData"
        :options="chartOptions"
      />
    </div>
  </template>
  
  <script>
  import { Line } from 'vue-chartjs'
  import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Filler
  } from 'chart.js'
  
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Filler
  )
  
  export default {
    components: { Line },
    props: {
      data: Array
    },
    computed: {
      chartData() {
        return {
          labels: this.data.map(d => d.date),
          datasets: [{
            label: 'Users',
            data: this.data.map(d => d.users),
            fill: true,
            backgroundColor: 'rgba(200, 200, 200, 0.2)',
            borderColor: 'rgb(150, 150, 150)',
            tension: 0.4
          }]
        }
      },
      chartOptions() {
        return {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .chart {
    height: 300px;
  }
  </style>