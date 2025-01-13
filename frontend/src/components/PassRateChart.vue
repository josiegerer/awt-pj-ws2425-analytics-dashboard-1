<template>
    <div class="activity-engagement-container">
      <h3>Pass Rate</h3>
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
    props: {
      activityEngagementData: {
        type: Array,
        required: true,
        default: () => [30, 50, 20] // Example data
      },
    },
    data() {
      return {
        chartOptions: {
          chart: {
            type: 'pie',
          },
          labels: ['Not Passed', 'Open', 'Passed'],
          colors: ['#c40d1e', '#888888', '#49cb40'],
          legend: {
            position: 'bottom',
          },
        },
      };
    },
    computed: {
      chartData() {
        return this.activityEngagementData;
      },
    },
  };
  </script>
  
  <style scoped>
  
  
  h3 {
    text-align: left; /* Align title to the left */
    font-size: 15px;
    color: black;
  }
  </style>