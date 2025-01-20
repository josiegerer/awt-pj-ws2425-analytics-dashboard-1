<template>
  <div class="pass-rates-container">
    <h3>Student Pass Rates</h3>
    <apexchart
      type="pie"
      :options="chartOptions"
      :series="[data.passed, data.failed]"
      height="300"
    />
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

export default {
  name: "PassRatesChart",
  components: {
    apexchart: VueApexCharts
  },
  props: {
    data: {
      type: Object,
      required: true
    }
  },
  computed: {
    chartOptions() {
      return {
        chart: {
          type: 'pie',
        },
        labels: ['Passed', 'Failed'],
        colors: ['#49cb40', '#c40d1e'],
        legend: {
          position: 'bottom'
        },
        tooltip: {
          y: {
            formatter: function(val) {
              return val + "%"
            }
          }
        }
      }
    }
  }
}
</script>

<style scoped>
.pass-rates-container {
  height: 100%;
}

h3 {
  text-align: left;
  font-size: 15px;
  color: black;
  margin-bottom: 15px;
}
</style>
