<template>
  <div class="assessment-marks-container">
    <h3>Assessment Performance Overview</h3>
    <p>Student Pass Rate Distribution</p>
    <apexchart
      type="pie"
      :options="chartOptions"
      :series="chartSeries"
      height="450"
    />
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

export default {
  name: "PassRates",
  components: {
    apexchart: VueApexCharts
  },
  data() {
    return {
      chartSeries: [],
      chartOptions: {
        chart: {
          type: "pie"
        },
        labels: ["Passed", "Failed", "Open"],
        colors: ["#4caf50", "#c40d1e", "#ff9800"],
        dataLabels: {
          enabled: true,
          formatter: (val) => `${val}%`
        },
        tooltip: {
          y: { formatter: (val) => `${val}%` }
        }
      }
    };
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch("http://localhost:8000/passRate/instructor");
        const data = await response.json();
        const userResults = data.userResults;

        let passed = 0;
        let failed = 0;
        let open = 0;

        Object.values(userResults).forEach(user => {
          passed += user.passed;
          failed += user.failed;
          open += user.open;
        });

        const total = passed + failed + open;

        this.chartSeries = [
          Math.round((passed / total) * 100) || 0,
          Math.round((failed / total) * 100) || 0,
          Math.round((open / total) * 100) || 0
        ];
      } catch (error) {
        console.error("Error fetching assessment data:", error);
      }
    }
  },
  mounted() {
    this.fetchData();
  }
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
