<template>
  <div class="chart">
    <h3>Popular Times</h3>
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script>
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default {
  name: "PopularTimesChart",
  data() {
    return {
      adminToken: localStorage.getItem("adminToken"), // Load token from local storage
      popularTimesData: Array(24).fill(0) // Default values for 24 hours
    };
  },
  computed: {
    chartData() {
      return {
        labels: Array.from({ length: 24 }, (_, i) => `${i}:00`), // Hours 0-23
        datasets: [
          {
            label: "Active Users",
            data: this.popularTimesData, // Set from API response
            backgroundColor: "#e2e8f0",
            borderRadius: 4,
            hoverBackgroundColor: "#9333ea",
            barThickness: 20
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
      };
    }
  },
  methods: {
    async fetchPopularTimes() {
      try {
        const response = await fetch("http://localhost:8000/popularTimes", {
          headers: { Authorization: `Bearer ${this.adminToken}` }
        });

        if (!response.ok) {
          throw new Error("Failed to fetch popularTimes");
        }

        const data = await response.json();

        if (data.activeUsersByHour) {
          this.popularTimesData = Object.values(data.activeUsersByHour); // Extract user counts
        }
      } catch (error) {
        console.error("Error fetching popularTimes:", error);
      }
    }
  },
  created() {
    this.fetchPopularTimes(); // Fetch API data when component is created
  }
};
</script>

<style scoped>
.chart {
  height: 320px;
}
</style>