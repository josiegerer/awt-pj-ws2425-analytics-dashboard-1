<template>
  <div class="heatmap-container">
    <h3>Active Hours</h3>
    <apexchart 
      type="heatmap" 
      :options="chartOptions" 
      :series="chartData" 
      height="350" 
    />
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

export default {
  name: "HeatmapChart",
  components: {
    apexchart: VueApexCharts
  },
  data() {
    return {
      chartData: [
        { name: "0:00-4:00", data: this.generateData(7, { min: 0, max: 240 }) },
        { name: "4:00-8:00", data: this.generateData(7, { min: 0, max: 240 }) },
        { name: "8:00-12:00", data: this.generateData(7, { min: 0, max: 240 }) },
        { name: "12:00-16:00", data: this.generateData(7, { min: 0, max: 240 }) },
        { name: "16:00-20:00", data: this.generateData(7, { min: 0, max: 240 }) },
        { name: "20:00-24:00", data: this.generateData(7, { min: 0, max: 240 }) },
      ],
      chartOptions: {
        chart: {
          height: 350,
          type: "heatmap",
        },
        dataLabels: {
          enabled: false,
        },
        plotOptions: {
          heatmap: {
            colorScale: {
              ranges: [
                { from: 0, to: 60, color: '#F8C373', name: '0-1 hour' },
                { from: 61, to: 120, color: '#FF6C00', name: '1-2 hours' },
                { from: 121, to: 180, color: '#C40D1E', name: '2-3 hours' },
                { from: 181, to: 240, color: '#76020C', name: '3-4 hours' },
              ],
            },
          },
        },
        xaxis: {
            categories: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            position: 'top', // Keep labels at the top
            labels: {
              style: {
                align: 'bottom', // Align text to the left
                colors: '#000', // Optional: Text color
                fontSize: '12px', // Optional: Font size
              },
            },
          },
        yaxis: {
          categories: ['0:00-4:00', '4:00-8:00', '8:00-12:00', '12:00-16:00', '16:00-20:00', '20:00-24:00'], // Ascending order
          title: {
            text: "Time of Day", // Label for the Y-axis
          },
        },
        tooltip: {
          y: {
            formatter: function (val) {
              return `${val} minutes`; // Tooltip format
            },
          },
        },
        legend: {
          show: true,
          position: 'bottom',
          horizontalAlign: 'center',
          labels: {
            colors: '#000',
          },
          markers: {
            size: 8, // Show individual markers
          },
        },
      },
    };
  },
  methods: {
    generateData(count, { min, max }) {
      let data = [];
      for (let i = 0; i < count; i++) {
        data.push(Math.floor(Math.random() * (max - min + 1)) + min);
      }
      return data;
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
