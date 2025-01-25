<template>
  <div class="chart">
    <h3>Popular Times</h3>
    <Bar 
      :data="chartData"
      :options="chartOptions"
    />
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

export default {
  name: 'PopularTimesChart',
  components: { Bar },
  props: {
    data: Array
  },
  computed: {
    chartData() {
      return {
        labels: this.data.map(d => d.hour), // FIXED
        datasets: [{
          label: 'Visits',
          data: this.data.map(d => d.visits), // FIXED
          backgroundColor: '#e2e8f0',
          borderRadius: 4,
          hoverBackgroundColor: '#9333ea',
          barThickness: 20
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
            grid: {
              display: true
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
.chart {
  height: 300px;
}
</style>
