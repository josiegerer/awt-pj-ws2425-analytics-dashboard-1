<template>
  <div class="chart-container">
    <div class="chart-header">
      <h3>Active Users (Last {{ selectedDays }} Days)</h3>
      <select v-model="selectedDays" @change="fetchActiveUsersData">
        <option v-for="n in 50" :key="n" :value="n">{{ n }} Days</option>
      </select>
    </div>
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script>
import { Line } from "vue-chartjs";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default {
  components: { Line },
  data() {
    return {
      adminToken: localStorage.getItem("adminToken"), // Load token from local storage
      activeUsersData: [], // Array to store daily active users
      selectedDays: 30 // Default to last 30 days
    };
  },
  computed: {
    averageUsers() {
      const totalUsers = this.activeUsersData.reduce((sum, d) => sum + d.users, 0);
      return totalUsers / this.activeUsersData.length || 0; // Avoid division by zero
    },
    chartData() {
      return {
        labels: this.activeUsersData.map(d => d.date), // Labels are selected days
        datasets: [
          {
            label: "Active Users",
            data: this.activeUsersData.map(d => d.users),
            fill: true,
            backgroundColor: "rgba(200, 200, 200, 0.2)",
            borderColor: "rgb(150, 150, 150)",
            tension: 0.4
          },
          {
            label: "Average Users",
            data: Array(this.activeUsersData.length).fill(this.averageUsers), // Flat average line
            borderColor: "rgb(255, 99, 132)",
            borderWidth: 2,
            borderDash: [10, 5], // Dashed line
            pointRadius: 0 // Hide points on the average line
          }
        ]
      };
    },
    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true // Display legend for both datasets
          }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      };
    }
  },
  methods: {
    async fetchActiveUsersData() {
      const today = new Date();
      let promises = [];

      // Loop through the selected number of days
      for (let i = this.selectedDays - 1; i >= 0; i--) {
        const day = new Date();
        day.setDate(today.getDate() - i);
        const formattedDate = day.toISOString().split("T")[0]; // YYYY-MM-DD format

        promises.push(
          fetch(`http://localhost:8000/activeUser/${i + 1}`, {
            headers: { Authorization: `Bearer ${this.adminToken}` }
          })
            .then(response => response.json())
            .then(data => ({
              date: formattedDate,
              users: data.activeUser || 0
            }))
            .catch(error => {
              console.error(`Error fetching active users for day ${i + 1}:`, error);
              return { date: formattedDate, users: 0 };
            })
        );
      }

      // Wait for all API calls to complete
      this.activeUsersData = await Promise.all(promises);
    }
  },
  created() {
    this.fetchActiveUsersData(); // Fetch API data when component is created
  }
};
</script>

<style scoped>
.chart-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: 400px; 
  min-height: 400px;
  max-height: 500px;
  overflow: hidden; 
}

.chart-header {
  display: flex;
  justify-content: space-between;
  width: 100%;
  align-items: center;
  margin-bottom: 10px; 
}

select {
  padding: 5px;
  font-size: 14px;
  margin-left: 10px;
}

.chart {
  height: 250px; 
  width: 100%;
  max-height: 250px;
}
</style>

