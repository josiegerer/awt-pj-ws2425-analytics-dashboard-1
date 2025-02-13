<template>
  <!-- Pie chart of pass rates (total of all activities)-->
  <div class="assessment-marks-container">
    <h3>Assessment Pass Rate</h3>
    <p>Student Pass Rate Distribution</p>
    <apexchart
      type="pie"
      :options="chartOptions"
      :series="chartData"
      height="450"
    />
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

export default {
  name: "PassRates",
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    // create and format pie chart
    return {
      chartData: [0, 0, 0], // [Failed, Open, Passed]
      chartOptions: {
        chart: {
          type: "pie",
        },
        labels: ["Not Passed", "Open", "Passed"],
        colors: ["#c40d1e", "#888888", "#49cb40"],
        legend: {
          position: "top",
        },
        dataLabels: {
          enabled: true,
          style: {
            fontSize: '12px' 
          },
          formatter: (val) => `${Math.round(val)}%`,
        },
      },
    };
  },
  methods: {
    // get cookie
    getCookie(name) {
      const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
      return match ? match[2] : null;
    },
    async fetchPassRateData() {
      // Get the authentication token from cookie
      const token = this.getCookie("auth_token");

      if (!token) {
        console.error("No authentication token found.");
        return;
      }

      try {
        // fetch data from url endpoint
        const response = await fetch("http://localhost:8000/passRate/instructor", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("API Response:", data);

        // Extract passed, failed, and open values from the response
        const userResults = data.userResults || {};
        let passed = 0;
        let failed = 0;
        let open = 0;

        // Sum up the values for passed, failed, and open
        Object.values(userResults).forEach((user) => {
          passed += user.passed || 0;
          failed += user.failed || 0;
          open += user.open || 0;
        });

        // Round each value to 2 decimal places
        passed = parseFloat(passed.toFixed(2));
        failed = parseFloat(failed.toFixed(2));
        open = parseFloat(open.toFixed(2));

        this.chartData = [failed, open, passed];

      } catch (error) {
        console.error("Error fetching assessment data:", error);
      }
},
  },
  mounted() {
    this.fetchPassRateData();
  },
};
</script>

<style scoped>
.assessment-marks-container {
  height: 100%;
}

h3 {
  text-align: left;
  font-size: 15px;
  color: black;
  margin-bottom: 5px;
}

p {
  text-align: left;
  font-size: 12px;
  color: grey;
  margin-bottom: 15px;
}
</style>