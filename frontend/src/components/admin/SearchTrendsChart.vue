<template>
    <div class="search-trends">
      <div class="search-header">
        <div class="search-title">
          <h3>Searches conducted</h3>
          <div class="search-count">254</div>
          <div class="search-change">+30 Searches in the last 30 days</div>
        </div>
      </div>
      <div class="chart">
        <Line
          :data="chartData"
          :options="chartOptions"
        />
      </div>
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
    Tooltip
  } from 'chart.js'
  
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip
  )
  
  export default {
    name: 'SearchTrendsChart',
    components: { Line },
    props: {
      data: Array
    },
    computed: {
      chartData() {
        return {
          labels: this.data.map(d => d.date),
          datasets: [{
            label: 'Searches',
            data: this.data.map(d => d.searches),
            borderColor: '#3b82f6',
            tension: 0.4,
            borderWidth: 2,
            pointRadius: 0
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
              beginAtZero: true,
              max: 200,
              ticks: {
                stepSize: 50
              },
              grid: {
                color: '#f0f0f0'
              }
            },
            x: {
              grid: {
                display: false
              }
            }
          }
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .search-trends {
    height: 100%;
  }
  
  .search-header {
    margin-bottom: 20px;
  }
  
  .search-title {
    margin-bottom: 10px;
  }
  
  .search-count {
    font-size: 2em;
    font-weight: bold;
    display: inline-flex;
    align-items: baseline;
  }
  

  .search-change {
    color: #22bb33;
    font-size: 0.9em;
    margin-top: 5px;
  }
  
  .chart {
    height: 200px;
  }
  </style>