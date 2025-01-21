<template>
  <div>
    <h2>Time Spent on Activities</h2>
    
    <!-- Dropdown to select the time period -->
    <div>
      <label for="time-period">Select Time Period: </label>
      <select v-model="timePeriod" id="time-period">
        <option value="day">Day</option>
        <option value="week">Week</option>
        <option value="month">Month</option>
        <option value="year">Year</option>
      </select>
    </div>

    <!-- Line Chart Component -->
    <LineChart :data="chartData" :options="chartOptions" />
  </div>
</template>

<script>
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement);

export default {
  components: {
    LineChart: Line,
  },
  data() {
    return {
      timePeriod: 'day', // Default to day
      chartData: {
        labels: [], // This will dynamically update based on time period
        datasets: [
          {
            label: 'User Count',
            data: [], // This will dynamically update based on time period
            borderColor: 'rgba(75,192,192,1)',
            borderWidth: 1,
            fill: false,
          },
        ],
      },
      chartOptions: {
        responsive: true,
        scales: {
          x: {
            beginAtZero: true,
          },
        },
      },
    };
  },
  watch: {
    // Watch for changes in timePeriod and update chart data accordingly
    timePeriod(newPeriod) {
      this.updateChartData(newPeriod);
    },
  },
  created() {
    // Initialize chart data for the default time period (Day)
    this.updateChartData(this.timePeriod);
  },
  methods: {
    updateChartData(period) {
      // Define different datasets for each period
      if (period === 'day') {
        this.chartData.labels = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5'];
        this.chartData.datasets[0].data = [100, 200, 150, 300, 250]; // Example data
      } else if (period === 'week') {
        this.chartData.labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
        this.chartData.datasets[0].data = [75, 85, 90, 95]; // Example data
      } else if (period === 'month') {
        this.chartData.labels = ['January', 'February', 'March', 'April'];
        this.chartData.datasets[0].data = [200, 180, 160, 220]; // Example data
      } else if (period === 'year') {
        this.chartData.labels = ['2021', '2022', '2023'];
        this.chartData.datasets[0].data = [500, 600, 700]; // Example data
      }
    },
  },
};
</script>

<style scoped>
/* Optional styles for the chart */
h2 {
  text-align: center;
}

select {
  margin-left: 10px;
  padding: 5px;
}

div {
  margin-bottom: 20px;
}
</style>
