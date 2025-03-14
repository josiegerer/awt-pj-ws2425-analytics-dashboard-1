<template>
  <!-- Container for the activity engagement pie chart -->
  <div class="activity-engagement-container">
    <h3>Activity Engagement</h3>
    <!-- ApexCharts component for rendering the pie chart -->
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
  name: "ActivityEngagement",
  components: {
    apexchart: VueApexCharts
  },
  data() {
    return {
      // Data for the pie chart
      chartData: [0, 0, 0], // [Not Started, In Progress, Completed]
      totalActivities: 0, 
      // Configuration options for the pie chart
      chartOptions: {
        chart: {
          type: 'pie',
        },
        labels: ['Not Started', 'In Progress', 'Completed'],
        colors: ['#C40D1E', '#FF6C00', '#49CB40'],
        legend: {
          position: 'bottom',
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

    // Function to fetch the total number of activities
    async fetchTotalActivities() {
      const token = this.getCookie("auth_token");

      if (!token) {
        console.error("No authentication token found.");
        return;
      }

      try {
        const response = await fetch("http://localhost:8000/passRate/learner", {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) {
          console.error("Error fetching total activities:", response.statusText);
          return;
        }

        const data = await response.json();
        this.totalActivities = (data.passed || 0) + (data.failed || 0) + (data.open || 0); 
        console.log("Total Activities:", this.totalActivities);
        this.fetchActivityEngagement();
      } catch (error) {
        console.error("Error fetching total activities:", error);
      }
    },

    // Function to fetch activity engagement data from the server
    async fetchActivityEngagement() {
      const token = this.getCookie("auth_token");

      if (!token) {
        console.error("No authentication token found.");
        return;
      }

      try {
        const response = await fetch("http://localhost:8000/activityEngagement", {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) {
          console.error("Error fetching activity engagement data:", response.statusText);
          return;
        }

        const data = await response.json();
        console.log("API Response:", data);

        if (!data.verbsCount) {
          console.error("Invalid data structure: verbsCount not found");
          return;
        }

        let notStarted = 0;
        let inProgress = 0;
        let completed = 0;

        const verbsCount = data.verbsCount || {};
        const receivedActivities = Object.keys(verbsCount);

        // Calculate the number of activities in each state
        receivedActivities.forEach(activity => {
          const verbs = verbsCount[activity];
          const initialized = verbs.initialized || 0;
          const completedCount = verbs.completed || 0;

          if (initialized === 0) {
            notStarted++;
          } else if (initialized > 0 && completedCount === 0) {
            inProgress++;
          } else if (initialized > 0 && completedCount > 0) {
            completed++;
          }
        });

        // Adjust notStarted count based on total activities
        notStarted += Math.max(0, this.totalActivities - receivedActivities.length);

        console.log("Calculated Values:", { notStarted, inProgress, completed });
        this.chartData = [notStarted, inProgress, completed];
      } catch (error) {
        console.error("Error fetching activity engagement data:", error);
      }
    },
  },
  // Fetch total activities data when the component is mounted
  mounted() {
    this.fetchTotalActivities();
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
