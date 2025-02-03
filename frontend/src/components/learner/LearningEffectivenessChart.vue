<template>
  <div style="width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
    <div style="flex: 1;">
      <h3>Learning Effectiveness</h3>
      <p>Assessment points vs. Additional Time Spent on Activity</p>
      <canvas ref="scatterChart" style="width: 100%; height: 100%;"></canvas>
    </div>

    <!-- Manual Legend -->
    <div class="manual-legend">
      <div class="legend-item">
        <div class="legend-color" style="background-color: orange;"></div>
        <span class="legend-text">Improvement Potential</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background-color: green;"></div>
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
  name: "LearningEffectivenessChart",
  setup() {
    const scatterChart = ref(null);
    const scatterData = ref([]);
    const maxDuration = ref(120); // Default max
    const currentDate = ref(new Date().toLocaleDateString());

    const getCookie = (name) => {
      const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
      return match ? match[2] : null;
    };

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

        let maxTimeSpent = 0; // Track highest time spent

        scatterData.value = data.activitiesEfficiency.flatMap(activity =>
          activity.scores.map(score => {
            let duration = score.duration;

            if (typeof duration === "number") {
              console.log(`Valid numeric duration: ${duration}`);
            } else if (typeof duration === "string") {
              // Handle ISO 8601 duration format (e.g., "PT2H30M")
              const hours = parseInt(duration.match(/PT(\d+)H/)?.[1] || 0);
              const minutes = parseInt(duration.match(/H(\d+)M/)?.[1] || 0);
              duration = hours * 60 + minutes;
              console.log(`Parsed duration: ${duration}`);
            } else {
              console.error("Invalid duration format:", duration);
              return null;
            }

            maxTimeSpent = Math.max(maxTimeSpent, duration); // Track max value

            return { x: duration, y: score.score };
          })
        ).filter(Boolean);

        maxDuration.value = Math.ceil(maxTimeSpent / 10) * 10; // Round up to nearest 10

        renderChart();
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    const renderChart = () => {
      const ctx = scatterChart.value?.getContext("2d");
      if (!ctx) {
        console.error("Failed to get canvas context.");
        return;
      }

      const img = new Image();
      img.src = require("@/assets/learning_effectiveness_background.png");

      img.onload = () => {
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
                max: maxDuration.value, // Dynamic max value
              },
              y: {
                title: {
                  display: true,
                  text: "Assessment Points",
                  font: { size: 12, weight: "bold" },
                },
                min: 0,
                max: 100,
              },
            },
          },
          plugins: [
            {
              id: "backgroundImage",
              beforeDraw: (chart) => {
                if (chart?.chartArea) {
                  const { top, left, width, height } = chart.chartArea;
                  chart.ctx.drawImage(img, left, top, width, height);
                }
              },
            },
          ],
        });
      };
    };

    onMounted(fetchData);

    return { scatterChart, currentDate };
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

.manual-legend {
  display: flex;
  justify-content: center;
  margin-top: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-right: 20px;
}

.legend-color {
  width: 15px;
  height: 15px;
  margin-right: 5px;
}
</style>
