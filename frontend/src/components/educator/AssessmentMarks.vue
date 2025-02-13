<template>
  <div class="assessment-marks-container">
    <h3>Assessment Performance Overview</h3>
    <p>Class Average Grades per Assessment</p>
    <apexchart
      type="bar"
      :options="chartOptions"
      :series="chartSeries"
      height="550"
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
      chartSeries: [], 
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
          categories: [], 
          labels: {
            style: { fontSize: "10px" },
            rotate: -45,
            trim: false,
            maxHeight: 120,
            wrap: true,
            hideOverlappingLabels: true,
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
    getCookie(name) {
      const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
      return match ? match[2] : null;
    },
    async fetchAssessmentMarks() {
      try {
        const authToken = this.getCookie("auth_token");
        if (!authToken) {
          console.error("No authentication token found.");
          return;
        }

        // Fetch assessment performance data
        const response = await fetch("http://localhost:8000/assesmentPerformance/instructor", {
          headers: { Authorization: `Bearer ${authToken}` }
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        const activities = data.activitiesSummary;

        // Fetch activity names
        const nameResponse = await fetch("http://localhost:8000/getNameForActivityId", {
          headers: { Authorization: `Bearer ${authToken}` }
        });

        if (!nameResponse.ok) {
          throw new Error(`HTTP error! Status: ${nameResponse.status}`);
        }

        const nameData = await nameResponse.json();
        const nameMap = this.createNameMap(nameData.objects || []);

        // Map activity names to their IDs
        const categories = activities.map((activity) => nameMap[activity.activityId] || activity.activityId);

        // Extract average scores
        const averageScores = activities.map((activity) => Math.round(activity.averageScore));

        // Update chart data
        this.chartOptions = {
          ...this.chartOptions,
          xaxis: {
            ...this.chartOptions.xaxis,
            categories: categories, 
          },
        };

        this.chartSeries = [
          {
            name: "Class Average",
            data: averageScores, 
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