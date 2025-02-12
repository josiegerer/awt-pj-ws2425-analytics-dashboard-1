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
          toolbar: { show: false }
        },
        dataLabels: { enabled: false }, // Hide numbers in heatmap cells
        plotOptions: {
          heatmap: {
            radius: 3,
            enableShades: true,
            colorScale: {
              ranges: [
                { from: 0, to: 0, color: "#f8e8cf", name: "No Activity" },
                { from: 1, to: 59, color: "#F8C373", name: "< 1 Hour" },
                { from: 60, to: 120, color: "#FF6C00", name: "1-2 Hours" },
                { from: 121, to: 180, color: "#C40D1E", name: "2-3 Hours" },
                { from: 181, to: 240, color: "#76020C", name: "3-4 Hours" },
              ],
            },
          },
        },
        xaxis: {
          categories: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
          position: "top",
          labels: { style: { colors: "#000", fontSize: "12px" } },
          axisBorder: { show: false },
          axisTicks: { show: false }
        },
        yaxis: {
          labels: {
            style: { colors: "#000", fontSize: "13px" }, // Slightly bigger font
            offsetX: -10, // Moves labels left to prevent cutoff
          },
          reversed: true
        },
        tooltip: {
          y: {
            formatter: function(val) {
              if (val === 0) return "No Activity";
              const roundedMinutes = Math.round(val);
              if (roundedMinutes < 60) return roundedMinutes + " minutes";
              const hours = Math.floor(roundedMinutes / 60);
              const minutes = roundedMinutes % 60;
              return `${hours}h ${minutes}`;
            },
          },
        },
        legend: {
          show: true,
          position: "bottom",
          horizontalAlign: "center",
          labels: { colors: "#000" },
          markers: { radius: 3, size: 8 }
        },
        grid: {
          padding: { top: 0, right: 0, bottom: 0, left: 20 } // Increased left padding
        },
        stroke: { width: 1 }
      },
    };
  },
  methods: {
    getCookie(name) {
      const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
      return match ? match[2] : null;
    },

    async fetchActiveHours() {
      const token = this.getCookie("auth_token");

      if (!token) {
        console.error("No authentication token found.");
        return;
      }

      try {
        const response = await fetch("http://localhost:8000/activeHoursThisWeek", {
          headers: { Authorization: `Bearer ${token}` }
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        
        const timeSlots = [
          "00:00-04:00", "04:00-08:00", "08:00-12:00",
          "12:00-16:00", "16:00-20:00", "20:00-24:00"
        ];

        this.chartData = timeSlots.map(slot => ({
          name: slot,
          data: Array(7).fill(0)
        }));

        data.activeHours.forEach((day, dayIndex) => {
          day.hours.forEach(hourData => {
            const timeSlotIndex = Math.floor(hourData.hour / 4);
            if (timeSlotIndex >= 0 && timeSlotIndex < 6) {
              this.chartData[timeSlotIndex].data[dayIndex] += hourData.timeSpent;
            }
          });
        });

      } catch (error) {
        console.error("Error fetching active hours data:", error);
      }
    }
  },
  mounted() {
    this.fetchActiveHours();
  }
};
</script>

<style scoped>
.heatmap-container {
  padding: 20px;
}

h3 {
  text-align: left;
  font-size: 15px;
  color: black;
  margin-bottom: 20px;
}
</style>
