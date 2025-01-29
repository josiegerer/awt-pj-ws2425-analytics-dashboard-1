<template>
  <div class="activity-engagement-container">
    <h3>Activity Engagement</h3>
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
      chartData: [0, 0, 0], // [Not Started, In Progress, Completed]
      totalActivities: 0, // Wird durch API-Aufruf aktualisiert
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
    async fetchTotalActivities() {
      try {
        const response = await fetch("http://localhost:8000/assessmentAttempts", {
          headers: { Authorization: `Bearer ${localStorage.getItem("learnerToken")}` },
        });
        const data = await response.json();
        this.totalActivities = data.activities.length; // Gesamtanzahl der Aktivitäten setzen
        this.fetchActivityEngagement();
      } catch (error) {
        console.error("Error fetching total activities:", error);
      }
    },
    async fetchActivityEngagement() {
      try {
        const response = await fetch("http://localhost:8000/activityEngagement", {
          headers: { Authorization: `Bearer ${localStorage.getItem("learnerToken")}` },
        });
        const data = await response.json();
        console.log("Received Data:", data);

        let notStarted = 0;
        let inProgress = 0;
        let completed = 0;

        // Extract activities and verbs count
        const verbsCount = data.verbsCount || {};
        const receivedActivities = Object.keys(verbsCount);

        // Process each activity
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

        // Add missing activities to "Not Started"
        notStarted += this.totalActivities - receivedActivities.length;

        // Update chart data
        this.chartData = [notStarted, inProgress, completed];

      } catch (error) {
        console.error("Error fetching activity engagement data:", error);
      }
    },
  },
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
