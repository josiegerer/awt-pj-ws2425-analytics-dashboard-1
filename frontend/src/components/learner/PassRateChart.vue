<template>
  <!-- Container for the pass rate pie chart -->
  <div class="pass-rate-container">
    <h3>Pass Rate</h3>
    <!-- ApexCharts component for rendering the pie chart -->
    <apexchart 
      type="pie" 
      :options="chartOptions" 
      :series="chartData" 
      height="380" 
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
  provide() {
    return {
      passRate: () => this.passRate,
    };
  },
  data() {
    return {
      // Data for the pie chart
      chartData: [0, 0, 0], // [Failed, Open, Passed]
      // Configuration options for the pie chart
      chartOptions: {
        chart: {
          type: 'pie',
          height: 380, // Increased height to accommodate legend
        },
        labels: ['Not Passed', 'Open', 'Passed'],
        colors: ['#c40d1e', '#888888', '#49cb40'],
        legend: {
          position: 'bottom',
          horizontalAlign: 'center',
          show: true,
          floating: false,
          itemMargin: {
            horizontal: 10,
            vertical: 5
          },
        },
      },
    };
  },
  methods: {
    // Function to get a cookie value by name
    getCookie(name) {
      const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
      return match ? match[2] : null;
    },
    // Function to fetch pass rate data from the server
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

        const passed = data.passed || 0;
        const failed = data.failed || 0;
        const open = data.open || 0;

        this.chartData = [failed, open, passed];

        this.passRate = failed + open > 0 ? (passed / (failed + open)).toFixed(2) : 0;

      } catch (error) {
        console.error("Error fetching pass rate data:", error);
      }
    },
  },
  // Fetch pass rate data when the component is mounted
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
