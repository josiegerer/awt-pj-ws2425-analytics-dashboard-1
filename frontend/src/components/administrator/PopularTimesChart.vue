<template>
  <!-- Bar chart of popular hours of the current day-->
  <h3 class="chart-header">Popular Times</h3>
  <div class="chart-container" style="width: 100%; height: 400px;">
    <canvas ref="chartRef"></canvas>
  </div>
</template>
 
<script setup>
import { ref, onMounted } from "vue";
import { Chart, BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip } from "chart.js";

// Register Chart.js components
Chart.register(BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip);

const chartRef = ref(null);
const chartInstance = ref(null);
const chartData = ref({
  labels: [],
  datasets: [
    {
      label: "Active Users by Hour",
      data: [],
      backgroundColor: "rgba(96, 96, 96, 0.7)",
      borderWidth: 1,
    },
  ],
});

// Fetch data from API
const fetchData = async () => {
  try {
    const response = await fetch("http://localhost:8000/popularTimes");
    const data = await response.json();
    const activeUsers = data.activeUsersByHour;

    // Map active users to hours
    chartData.value.labels = Object.keys(activeUsers).map((hour) => `${hour}:00`);
    chartData.value.datasets[0].data = Object.values(activeUsers);

    renderChart();
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

// Function to render the chart
const renderChart = () => {
  if (chartInstance.value) {
    chartInstance.value.destroy(); 
  }
  chartInstance.value = new Chart(chartRef.value, {
    type: "bar",
    data: chartData.value,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          title: { display: true, text: "Hour of the Day" },
        },
        y: {
          title: { display: true, text: "Number of Active Users" },
          beginAtZero: true,
          ticks: {
            precision: 0, 
          },
        },
      },
    },
  });
};

// Fetch data when the component is mounted
onMounted(fetchData);
</script>

<style scoped>
.chart-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: 500px; 
  overflow: hidden; 
}

.chart-header {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 10px; 
}
</style>

