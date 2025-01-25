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
    props: {
      data: {
        type: Array,
        required: true,
      },
    },
    setup(props) {
      const scatterChart = ref(null);
  
      onMounted(() => {
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
                label: "Scatter Data",
                data: props.data,
                backgroundColor: "rgba(75, 192, 192, 1)",
              },
            ],
          },
          options: {
            plugins: {
              legend: {
                display: false,
              },
            },
            scales: {
            x: {
              type: "linear",
              position: "bottom",
              title: {
                display: true,
                text: "Time Spent", 
                font: {
                  size: 12,
                  weight: 'bold',
                },
              },
              min: 0,
              max: 120,
              stepSize: 20,
            },
            y: {
              title: {
                display: true,
                text: "Assessment Points", 
                font: {
                  size: 12,
                  weight: 'bold',
                },
              },
              min: 0,
              max: 100,
              stepSize: 20,
            },
          },
          legend: {
            display: false,
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
      });
  
      return {
        scatterChart,
      };
    },
  });
  </script>

<style scoped>
h3 {
  text-align: left; 
  font-size: 15px;
  color: black;
}

p{
  font-size: 12px;
}
.manual-legend .legend-text {
  font-size: 12pt;

  font-style: "Inter";
}
</style>


