<template>
  <div class="assessment-marks-container">
    <h3>Assessment Performance Overview</h3>
    <p>Class Average Grades per Assessment</p>
    <apexchart
      type="line"
      :options="chartOptions"
      :series="[{
        name: 'Class Average',
        data: data.map(item => item.averageGrade)
      }]"
      height="300"
    />
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

export default {
  name: "AssessmentMarks",
  components: {
    apexchart: VueApexCharts
  },
  props: {
    data: {
      type: Array,
      required: true
    }
  },
  computed: {
    chartOptions() {
      return {
        chart: {
          type: 'line',
          zoom: {
            enabled: false
          },
          toolbar: {
            show: false
          }
        },
        stroke: {
          curve: 'smooth',
          width: 2
        },
        dataLabels: {
          enabled: true,
          formatter: function(val) {
            return val + '%'
          }
        },
        xaxis: {
          categories: this.data.map(item => item.name),
          labels: {
            style: {
              fontSize: '12px'
            },
            rotateAlways: true,
            rotate: -45,
            trim: false,
            maxHeight: 100
          }
        },
        yaxis: {
          min: 0,
          max: 100,
          labels: {
            formatter: function(val) {
              return val + '%'
            }
          },
          title: {
            text: 'Class Average (%)'
          }
        },
        colors: ['#c40d1e'],
        markers: {
          size: 5,
          hover: {
            size: 7
          }
        },
        tooltip: {
          y: {
            formatter: function(val) {
              return val + '%'
            }
          }
        }
      }
    }
  }
}
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
