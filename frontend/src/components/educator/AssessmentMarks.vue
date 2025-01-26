<template>
  <div class="assessment-marks-container">
    <h3>Assessment Performance Overview</h3>
    <p>Class Average Grades per Assessment</p>
    <apexchart
      type="bar"
      :options="chartOptions"
      :series="chartSeries"
      height="450"
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
  data() {
    return {
      chartSeries: [], 
      chartOptions: {
        chart: {
          type: "bar",
          zoom: { enabled: false },
          toolbar: { show: false }
        },
        plotOptions: {
          bar: {
            horizontal: false, 
            columnWidth: "60%", 
            endingShape: "rounded"
          }
        },
        dataLabels: {
          enabled: true,
          style: {
            fontSize: "10px" 
          },
          formatter: (val) => `${val}%`,
          offsetY: -5 
        },
        xaxis: {
          categories: [], 
          labels: {
            style: { fontSize: "10px" }, 
            rotate: -45,
            trim: false,
            maxHeight: 120, 
            wrap: true 
          }
        },
        yaxis: {
          min: 0,
          max: 100,
          labels: {
            formatter: (val) => `${val}%`
          },
          title: { text: "Class Average (%)" }
        },
        colors: ["#c40d1e"],
        tooltip: {
          y: { formatter: (val) => `${val}%` }
        }
      }
    };
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch("http://localhost:8000/assessmentPerformance");
        const data = await response.json();
        const activities = data.activitiesSummary;

        // Extract activity names and scores
        this.chartOptions = {
          ...this.chartOptions, 
          xaxis: {
            categories: activities.map((activity) =>
              activity.activityId.split("/").pop().replace(/_/g, " ") // Extract readable activity names
            ),
            labels: {
              style: { fontSize: "10px" },
              rotateAlways: true,
              rotate: -45,
              trim: false,
              maxHeight: 120,
              wrap: true 
            }
          }
        };

        this.chartSeries = [
          {
            name: "Class Average",
            data: activities.map((activity) => Math.round(activity.averageScore)) 
          }
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
