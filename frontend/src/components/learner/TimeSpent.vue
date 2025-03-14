<template>
  <div class="time-spent-container">
    <h3>Total Time Spent on Activities</h3>
    <p>in Minutes</p>
    <div class="chart-wrapper">
      <!-- ApexCharts component for rendering the bar chart -->
      <apexchart 
        type="bar" 
        :options="chartOptions" 
        :series="chartData" 
      />
    </div>
    <!-- Button to toggle the visibility of the table -->
    <button @click="toggleTable" class="view-more-button">
      {{ showTable ? 'View Less' : 'View More' }}
    </button>
    <!-- Table to display detailed time spent on each activity -->
    <table v-if="showTable" class="time-spent-table">
      <thead>
        <tr>
          <th>Activity</th>
          <th>Total Time Spent (minutes / hours)</th>
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
      showTable: false, // Controls the table visibility
      activities: [],
      totalTime: 0,
    };
  },
  computed: {
    // Data for the bar chart
    chartData() {
      return [
        {
          name: 'Time Spent',
          data: this.activities.map((item) => item.duration),
        },
      ];
    },
    // Configuration options for the bar chart
    chartOptions() {
      return {
        chart: {
          type: 'bar',
          height: '100%',
          width: '100%',
        },
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: '80%',
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
            formatter: (val) => {
              const hours = (val / 60).toFixed(1);
              return `${val} minutes (${hours}h)`;
            },
          },
        },
        colors: ['#555555'],
      };
    },
  },
  methods: {
    // Function to toggle the visibility of the table
    toggleTable() {
      this.showTable = !this.showTable;
    },
    // Function to extract and transform activity name from activityId
    getActivityName(activityId) {
      return activityId.split('/').pop().replace(/_/g, ' ');
    },
    // Function to get a shortened version of the activity name
    getShortActivityName(activityId) {
      const name = this.getActivityName(activityId);
      return name.length > 10 ? name.substring(0, 10) + '...' : name;
    },
    // Function to format the duration in minutes and hours
    formatDuration(duration) {
      const hours = (duration / 60).toFixed(1);
      const minutesFormatted = duration % 1 === 0 ? duration.toFixed(0) : duration.toFixed(2);
      return `${minutesFormatted} (${hours}h)`;
    },
    // Function to fetch data from the server
    async fetchData() {
      try {
        const authToken = document.cookie.match(/(^| )auth_token=([^;]+)/)?.[2];
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
  // Fetch data when the component is mounted
  mounted() {
    this.fetchData();
  },
};
</script>

<style scoped>
.time-spent-container {
  width: 100%;
  max-width: 800px;
  margin: auto;
  text-align: center;
}

.chart-wrapper {
  width: 100%;
  height: 400px;
}

.view-more-button {
  background-color: grey;
  color: white;
  border: none;
  padding: 10px;
  cursor: pointer;
  border-radius: 5px;
  margin-top: 10px;
  border-color: grey;
}

.view-more-button:hover {
  background-color: darkgrey;
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

h3 {
  text-align: left; /* Align title to the left */
  font-size: 15px;
  color: black;
}

p {
  text-align: left; /* Align title to the left */
}
</style>
