<template>
  <div class="time-spent-container">
    <h3>Time Spent on Activities</h3>
    <p>in Minutes</p>
    <apexchart 
      type="bar" 
      :options="chartOptions" 
      :series="chartData" 
      height="350" 
    />
    <button @click.prevent="toggleTable" class="view-more-button">
      {{ showTable ? 'View Less' : 'View More' }}
    </button>
    <table v-if="showTable" class="time-spent-table">
      <thead>
        <tr>
          <th>Activity</th>
          <th>Time Spent (minutes)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in activities" :key="item.activityId">
          <td>{{ getActivityName(item.activityId) }}</td>
          <td>{{ formatDuration(item.duration) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts';

export default {
  name: 'TimeSpent',
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      showTable: false,
      activities: [],
      totalTime: 0,
    };
  },
  computed: {
    chartData() {
      return [
        {
          name: 'Time Spent',
          data: this.activities.map((item) => item.duration),
        },
      ];
    },
    chartOptions() {
      return {
        chart: {
          type: 'bar',
          height: 350,
        },
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: '55%',
            endingShape: 'rounded',
          },
        },
        dataLabels: {
          enabled: false,
        },
        stroke: {
          show: true,
          width: 2,
          colors: ['transparent'],
        },
        xaxis: {
          categories: this.activities.map((item) => this.getShortActivityName(item.activityId)),
        },
        yaxis: {
          title: {
            text: 'Minutes',
          },
        },
        fill: {
          opacity: 1,
        },
        tooltip: {
          y: {
            formatter: (val) => this.formatDuration(val) + ' minutes',
          },
        },
        colors: ['#4CAF50'],
      };
    },
  },
  methods: {
    getCookie(name) {
      const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
      return match ? match[2] : null;
    },

    toggleTable() {
      this.showTable = !this.showTable;
      this.$emit('button-click');
    },

    getActivityName(activityId) {
      return activityId.split('/').pop().replace(/_/g, ' ');
    },

    getShortActivityName(activityId) {
      const name = this.getActivityName(activityId);
      return name.length > 10 ? name.substring(0, 10) + '...' : name;
    },

    formatDuration(duration) {
      return duration % 1 === 0 ? duration.toFixed(0) : duration.toFixed(2);
    },

    async fetchData() {
      try {
        const authToken = this.getCookie('auth_token');
        if (!authToken) {
          console.error('Authentication token not found.');
          return;
        }

        const response = await fetch('http://localhost:8000/timeSpentOnActivities/learner', {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        this.activities = data.activities;
        this.totalTime = data.totalTime;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
  },
  mounted() {
    this.fetchData();
  },
};
</script>

<style scoped>
.time-spent-container {
  max-width: 600px;
  margin: auto;
  text-align: center;
}
.view-more-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px;
  cursor: pointer;
  border-radius: 5px;
  margin-top: 10px;
}
.view-more-button:hover {
  background-color: #45a049;
}
.time-spent-table {
  width: 100%;
  margin-top: 10px;
  border-collapse: collapse;
}
.time-spent-table th, .time-spent-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
.time-spent-table th {
  background-color: #f2f2f2;
}
</style>
