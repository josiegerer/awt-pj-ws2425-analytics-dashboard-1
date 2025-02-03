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
    apexchart: VueApexCharts,
  },
  data() {
    return {
      chartSeries: [], // Initialize with empty data
      chartOptions: {
        chart: {
          type: "bar",
          zoom: { enabled: false },
          toolbar: { show: false },
        },
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: "60%",
            endingShape: "rounded",
          },
        },
        dataLabels: {
          enabled: true,
          style: {
            fontSize: "10px",
          },
          formatter: (val) => `${val}%`,
          offsetY: -5,
        },
        xaxis: {
          categories: [], // Will be populated with activity names
          labels: {
            style: { fontSize: "10px" },
            rotate: -45,
            trim: false,
            maxHeight: 120,
            wrap: true,
          },
        },
        yaxis: {
          min: 0,
          max: 100,
          labels: {
            formatter: (val) => `${val}%`,
          },
          title: { text: "Class Average (%)" },
        },
        colors: ["#c40d1e"],
        tooltip: {
          y: { formatter: (val) => `${val}%` },
        },
      },
    };
  },
  methods: {
    async fetchAssessmentMarks() {
      try {
        // Fetch assessment performance data
        const response = await fetch("http://localhost:8000/assessmentPerformance");
        const data = await response.json();
        const activities = data.activitiesSummary;

        // Fetch activity names
        const nameResponse = await fetch("http://localhost:8000/getNameForActivityId");
        const nameData = await nameResponse.json();
        const nameMap = this.createNameMap(nameData.objects);

        // Map activity names to their IDs
        const categories = activities.map((activity) => nameMap[activity.activityId] || activity.activityId);

        // Extract average scores
        const averageScores = activities.map((activity) => Math.round(activity.averageScore));

        // Update chart data
        this.chartOptions = {
          ...this.chartOptions,
          xaxis: {
            ...this.chartOptions.xaxis,
            categories: categories, // Set activity names as x-axis labels
          },
        };

        this.chartSeries = [
          {
            name: "Class Average",
            data: averageScores, // Set average scores as y-axis data
          },
        ];
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    createNameMap(objects) {
      // Create a mapping of activityId to activityName
      return objects.reduce((map, obj) => {
        map[obj.objectId] = obj.objectName;
        return map;
      }, {});
    },
  },
  mounted() {
    this.fetchAssessmentMarks();
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