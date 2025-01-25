<template>
  <div class="search-trends">
    <div class="search-header">
      <div class="search-title">
        <h3>Top Search Trends</h3>
        <div class="search-count">{{ totalSearches }}</div>
        <div class="search-change">+{{ searchChange }} in the last 30 days</div>
      </div>
    </div>
    <div class="chart">
      <Bar
        :data="chartData"
        :options="chartOptions"
      />
    </div>
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
  name: 'SearchTrendsChart',
  components: { Bar },
  props: {
    data: Array
  },
  computed: {
    totalSearches() {
      return this.data.reduce((sum, d) => sum + d.count, 0) // Sum of all searches
    },
    searchChange() {
      return Math.floor(this.totalSearches * 0.12) // Mock increase (+12%)
    },
    chartData() {
      return {
        labels: this.data.map(d => d.query), // Words on X-axis
        datasets: [{
          label: 'Search Volume',
          data: this.data.map(d => d.count), // Counts on Y-axis
          backgroundColor: '#3b82f6', // Bar color
          borderRadius: 4,
          hoverBackgroundColor: '#9333ea',
          barThickness: 30
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
  height: 300px;
}
</style>
