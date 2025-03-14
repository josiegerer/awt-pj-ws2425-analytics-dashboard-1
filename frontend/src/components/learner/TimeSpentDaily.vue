<template>
  <div class="time-spent-daily-container">
    <h3>Time Spent on Activities (last 7 days)</h3>
    <p>in Minutes</p>
    <!-- ApexCharts component for rendering the bar chart -->
    <apexchart 
      type="bar" 
      :options="chartOptions" 
      :series="chartData" 
      height="350" 
    />
    <!-- Button to toggle the visibility of the table -->
    <button @click.prevent="toggleTable" class="view-more-button">
      {{ showTable ? 'View Less' : 'View More' }}
    </button>
    <!-- Table to display detailed time spent on each day -->
    <table v-if="showTable" class="time-spent-table">
      <thead>
        <tr>
          <th>Day</th>
          <th>Time Spent (minutes)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in data" :key="item.day">
          <td>{{ item.day }}</td>
          <td>{{ item.minutes }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

export default {
  name: "TimeSpentDaily",
  components: {
    apexchart: VueApexCharts
  },
  data() {
    return {
      data: [], // Store fetched data here
      showTable: false, // Controls the table visibility
    };
  },
  computed: {
    // Data for the bar chart
    chartData() {
      return [
        {
          name: 'Time Spent',
          data: this.data.map(item => item.minutes)
        }
      ];
    },
    // Configuration options for the bar chart
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
          enabled: false
        },
        stroke: {
          show: true,
          width: 2,
          colors: ['transparent']
        },
        xaxis: {
          categories: this.data.map(item => item.day),
        },
        yaxis: {
          title: {
            text: 'Minutes'
          }
        },
        fill: {
          opacity: 1
        },
        tooltip: {
          y: {
            formatter: function (val) {
              return `${val} minutes`;
            }
          }
        },
        annotations: {
          yaxis: [
            {
              y: this.averageTimeSpent,
              borderColor: '#9013fe',
              label: {
                borderColor: '#9013fe',
                style: {
                  color: '#fff',
                  background: '#9013fe'
                },
                text: this.averageTimeSpent.toFixed(2),
              }
            }
          ]
        }
      };
    },
    // Calculate the average time spent
    averageTimeSpent() {
      if (!this.data.length) return 0;
      const totalMinutes = this.data.reduce((sum, item) => sum + item.minutes, 0);
      return totalMinutes / this.data.length;
    }
  },
  methods: {
    // Function to get a cookie value by name
    getCookie(name) {
      const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
      return match ? match[2] : null;
    },
    // Function to fetch time spent data from the server
    async fetchTimeSpentData() {
      const token = this.getCookie("auth_token");
      if (!token) {
        console.error("No authentication token found");
        return;
      }
      try {
        const response = await fetch("http://localhost:8000/timeSpentOnLastSevenDays/learner", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (!response.ok) {
          throw new Error("Failed to fetch data");
        }
        const responseData = await response.json();
        this.data = responseData.timeSpentDaily || [];
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    // Function to toggle the visibility of the table
    toggleTable() {
      this.showTable = !this.showTable;
    }
  },
  // Fetch time spent data when the component is mounted
  mounted() {
    this.fetchTimeSpentData();
  }
};
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

.view-more-button {
  position: relative;
  top: 10px;
  right: 10px;
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  background-color: rgb(255, 255, 255);
  color: rgb(189, 186, 186);
  cursor: pointer;
  transition: background-color 0.3s;
}

.view-more-button:hover {
  background-color: rgb(253, 252, 252);
}

.time-spent-table {
  margin-top: 20px;
  width: 100%;
  border-collapse: collapse;
}

.time-spent-table th, .time-spent-table td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: left;
}

.time-spent-table th {
  background-color: #f5f5f5;
}
</style>
