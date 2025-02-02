<template>
  <div style="width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
    <div style="flex: 1;">
      <h3>Learning Effectiveness</h3>
      <p>Assessment points vs. Additional Time Spent on Activity</p>
      <canvas ref="scatterChart" style="width: 100%; height: 100%;"></canvas>
    </div>
    <!-- Manual Legend -->
    <div class="manual-legend" style="display: flex; justify-content: center; margin-top: 10px;">
      <div style="display: flex; align-items: center; margin-right: 20px;">
        <div style="width: 15px; height: 15px; background-color: orange; margin-right: 5px;"></div>
        <span class="legend-text">Improvement Potential</span>
      </div>
      <div style="display: flex; align-items: center;">
        <div style="width: 15px; height: 15px; background-color: green; margin-right: 5px;"></div>
        <span class="legend-text">Best Practice</span>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, onMounted, ref } from "vue";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

export default defineComponent({
  name: "ScatterPlot",
  setup() {
    const scatterChart = ref(null);
    const scatterData = ref([]);

    // ✅ Function to retrieve cookies
    const getCookie = (name) => {
      const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
      return match ? match[2] : null;
    };

    // ✅ Fetch data from API
    const fetchData = async () => {
      try {
        const authToken = getCookie("auth_token");

        if (!authToken) {
          console.error("No authentication token found.");
          return;
        }

        const response = await fetch("http://localhost:8000/learningEffectiveness", {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("API Response:", data);

        // ✅ Correctly extract and map scores and time spent
        scatterData.value = data.activitiesEfficiency.flatMap(activity =>
          activity.scores.map(score => {
            const duration = score.duration;
            const hours = parseInt(duration.match(/PT(\d+)H/)?.[1] || 0);
            const minutes = parseInt(duration.match(/H(\d+)M/)?.[1] || 0);
            const totalMinutes = hours * 60 + minutes;
            return { 
              x: totalMinutes, // Time Spent (in minutes)
              y: score.score   // Correct score value
            };
          })
        );

        renderChart();
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    // ✅ Render the scatter plot with background image
    const renderChart = () => {
      const ctx = scatterChart.value?.getContext("2d");
      if (!ctx) {
        console.error("Failed to get canvas context.");
        return;
      }

      new Chart(ctx, {
        type: "scatter",
        data: {
          datasets: [
            {
              label: "Learning Effectiveness",
              data: scatterData.value,
              backgroundColor: "rgba(75, 192, 192, 1)",
            },
          ],
        },
        options: {
          plugins: {
            legend: { display: false },
          },
          scales: {
            x: {
              type: "linear",
              title: {
                display: true,
                text: "Time Spent (minutes)",
                font: { size: 12, weight: "bold" },
              },
              min: 0,
              max: 120,
              stepSize: 20,
            },
            y: {
              title: {
                display: true,
                text: "Assessment Points",
                font: { size: 12, weight: "bold" },
              },
              min: 0,
              max: 100,
              stepSize: 20,
            },
          },
        },
        plugins: [
          {
            id: "backgroundImage",
            beforeDraw: (chart) => {
              if (chart?.chartArea) {
                const ctx = chart.ctx;
                const { top, left, width, height } = chart.chartArea;

                const img = new Image();
                img.src = require("@/assets/learning_effectiveness_background.png");
                img.onload = () => {
                  ctx.drawImage(img, left, top, width, height);
                };
              }
            },
          },
        ],
      });
    };

    onMounted(fetchData);

    return { scatterChart };
  },
});
</script>

<style scoped>
h3 {
  text-align: left;
  font-size: 15px;
  color: black;
}

p {
  font-size: 12px;
}

.manual-legend .legend-text {
  font-size: 12pt;
}
</style>
