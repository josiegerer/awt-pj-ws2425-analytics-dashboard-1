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
    chartData: [],
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
              { from: 0, to: 0, color: "#f8e8cf", name: "No Activity" }, // Hide 0 values
              { from: 1, to: 59, color: "#F8C373", name: "< 1 Hour" }, // Light Yellow
              { from: 60, to: 120, color: "#FF6C00", name: "1-2 Hours" }, // Orange
              { from: 121, to: 180, color: "#C40D1E", name: "2-3 Hours" }, // Red
              { from: 181, to: 240, color: "#76020C", name: "3-4 Hours" }, // Dark Red
            ],
          },
        },
      },
      xaxis: {
        categories: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        position: "top",
        labels: {
          style: {
            colors: "#000",
            fontSize: "12px",
          },
        },
      },
      yaxis: {
        title: {
          text: "Time of Day",
        },
      },
      tooltip: {
        y: {
          formatter: function (val) {
            return val > 0 ? `${val} minutes` : "No Activity";
          },
        },
      },
      legend: {
        show: true,
        position: "bottom",
        horizontalAlign: "center",
        labels: {
          colors: "#000",
        },
        markers: {
          size: 8,
        },
      },
    },
  };
  },
  methods: {
    async fetchActiveHours() {
      try {
        const response = await fetch("http://localhost:8000/activeHoursThisWeek");
        const data = await response.json();
        console.log("Received Data:", data);

        // Initialize data structure for 4-hour intervals
        let aggregatedData = {
          "0:00-4:00": [0, 0, 0, 0, 0, 0, 0],  // Mon-Sun
          "4:00-8:00": [0, 0, 0, 0, 0, 0, 0],
          "8:00-12:00": [0, 0, 0, 0, 0, 0, 0],
          "12:00-16:00": [0, 0, 0, 0, 0, 0, 0],
          "16:00-20:00": [0, 0, 0, 0, 0, 0, 0],
          "20:00-24:00": [0, 0, 0, 0, 0, 0, 0],
        };

        // Map API data to intervals
        data.activeHours.forEach((dayData, dayIndex) => {
          dayData.hours.forEach(hourData => {
            const interval = this.mapHourToInterval(hourData.hour);
            if (interval) {
              aggregatedData[interval][dayIndex] += this.roundToNearest(hourData.timeSpent, 10); // Hier wird gerundet
            }
          });
        });

        // Convert aggregated data to chart format
        this.chartData = Object.keys(aggregatedData).map(interval => ({
          name: interval,
          data: aggregatedData[interval]
        }));

      } catch (error) {
        console.error("Error fetching active hours data:", error);
      }
    },

    roundToNearest(value, step = 10) {
      return Math.round(value / step) * step; // Rundet auf nächste 10 Minuten
    },

    mapHourToInterval(hour) {
      if (hour >= 0 && hour < 4) return '0:00-4:00';
      if (hour >= 4 && hour < 8) return '4:00-8:00';
      if (hour >= 8 && hour < 12) return '8:00-12:00';
      if (hour >= 12 && hour < 16) return '12:00-16:00';
      if (hour >= 16 && hour < 20) return '16:00-20:00';
      if (hour >= 20 && hour < 24) return '20:00-24:00';
      return null;
    },
  },
  mounted() {
    this.fetchActiveHours();
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
