<template>
  <div class="assessment-performance-chart">
    <h3>Assessment Performance Over Time</h3>
    <div style="height: 400px; width: 100%;">
      <LineChart v-if="chartData.labels.length" :data="chartData" :options="chartOptions" />
      <p v-else>No data available</p>
    </div>
  </div>
</template>

<script>
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, TimeScale } from 'chart.js';
import 'chartjs-adapter-date-fns'; // Required for time-based charts

// Register Chart.js components
ChartJS.register(Title, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, TimeScale);

export default {
  name: 'AssessmentPerformanceChart',
  components: {
    LineChart: Line,
  },
  data() {
    return {
      chartData: {
        labels: [],
        datasets: [
          {
            label: 'Assessment Scores',
            data: [],
            borderColor: '#42A5F5',
            backgroundColor: 'rgba(66, 165, 245, 0.2)',
            fill: true,
            tension: 0.4,
          },
          {
            label: 'Average',
            data: [],
            borderColor: 'red',
            borderWidth: 2,
            borderDash: [5, 5], // Dashed line for average
            pointRadius: 0, // No points for this line
            fill: false,
          },
        ],
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          tooltip: {
            callbacks: {
              label: (context) => `Score: ${context.raw}`,
            },
          },
          legend: {
            display: true,
            position: 'bottom',
            labels: {
              color: '#000',
              font: { size: 12 },
            },
          },
        },
        scales: {
          x: {
            type: 'time',
            time: {
              unit: 'day',
              tooltipFormat: 'MMM dd, yyyy',
              displayFormats: {
                day: 'MMM dd',
              },
            },
            title: {
              display: true,
              text: 'Date',
            },
            ticks: {
              autoSkip: true,
              maxTicksLimit: 10,
            },
          },
          y: {
            title: {
              display: true,
              text: 'Assessment Score',
            },
            beginAtZero: true,
            min: 0,
            max: 100,
          },
        },
      },
    };
  },
  methods: {
    getCookie(name) {
      const match = document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`));
      return match ? match[2] : null;
    },

    async fetchAssessmentScores() {
      const token = this.getCookie('auth_token');

      if (!token) {
        console.error('No authentication token found.');
        return;
      }

      try {
        const response = await fetch('http://localhost:8000/learningEffectiveness', {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch assessment scores');
        }

        const data = await response.json();

        // Process the data
        const scores = data.activitiesEfficiency.flatMap(activity =>
          activity.scores.map(score => ({
            date: new Date(score.timestamp),
            formattedDate: new Date(score.timestamp).toISOString().split('T')[0], // Convert to "YYYY-MM-DD"
            score: score.score,
          }))
        );

        console.log('Assessment Scores:', scores);

        // Sort scores by date
        scores.sort((a, b) => a.date - b.date);

        // Extract labels and data
        const labels = scores.map(score => score.formattedDate);
        const scoresData = scores.map(score => score.score);

        // Calculate average score
        const averageValue = scoresData.length
          ? scoresData.reduce((acc, val) => acc + val, 0) / scoresData.length
          : 0;
        const averageData = Array(scoresData.length).fill(averageValue);

        // Ensure Vue reactivity updates chart data correctly
        this.chartData = {
          labels,
          datasets: [
            { ...this.chartData.datasets[0], data: scoresData },
            { ...this.chartData.datasets[1], data: averageData },
          ],
        };
      } catch (error) {
        console.error('Error fetching assessment scores:', error);
      }
    },
  },
  async mounted() {
    await this.fetchAssessmentScores();
  },
};
</script>

<style scoped>
h3 {
  text-align: left;
  font-size: 15px;
  color: black;
  margin-bottom: 20px;
}
</style>
