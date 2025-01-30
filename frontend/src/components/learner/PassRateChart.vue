<template>
  <div class="pass-rate-container">
    <h3>Pass Rate</h3>
    <apexchart 
      type="pie" 
      :options="chartOptions" 
      :series="chartData" 
      height="350" 
    />
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

export default {
  name: "PassRate",
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      chartData: [0, 0, 0], // [Failed, Open, Passed]
      chartOptions: {
        chart: {
          type: 'pie',
        },
        labels: ['Not Passed', 'Open', 'Passed'],
        colors: ['#c40d1e', '#888888', '#49cb40'],
        legend: {
          position: 'bottom',
        },
      },
    };
  },
  methods: {
    getCookie(name) {
      const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
      return match ? match[2] : null;
    },
    async fetchPassRate() {
  const token = this.getCookie("auth_token");

  if (!token) {
    console.error("No authentication token found.");
    return;
  }

  try {
    const response = await fetch("http://localhost:8000/passRate/learner", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    console.log("API Response:", data);

    // Extract passed, failed, and open values directly from the response
    const passed = data.passed || 0;
    const failed = data.failed || 0;
    const open = data.open || 0;

    // Update chart data
    this.chartData = [failed, open, passed];

  } catch (error) {
    console.error("Error fetching pass rate data:", error);
  }
},
  },
  mounted() {
    this.fetchPassRate();
  },
};
</script>

<style scoped>
h3 {
  text-align: left;
  font-size: 15px;
  color: black;
}
</style>