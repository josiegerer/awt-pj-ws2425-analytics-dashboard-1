<template>
  <div class="time-spent-daily-container">
    <h3>Time Spent on Activities (Daily)</h3>
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
  props: {
    data: {
      type: Array,
      required: true,
      default: () => [
        { day: "Monday", minutes: 120 },
        { day: "Tuesday", minutes: 90 },
        { day: "Wednesday", minutes: 60 },
        { day: "Thursday", minutes: 150 },
        { day: "Friday", minutes: 200 },
        { day: "Saturday", minutes: 180 },
        { day: "Sunday", minutes: 100 },
      ],
    },
  },
  data() {
    return {
      showTable: false,
    };
  },
  computed: {
    chartData() {
      return [
        {
          name: 'Time Spent',
          data: this.data.map(item => item.minutes)
        }
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
            colors: {
              ranges: [{
                from: 0,
                to: Infinity,
                color: '#b0b0b0'
              }]
            }
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
                hover: {
                  text: 'Average'
                }
              }
            }
          ]
        }
      };
    },
    averageTimeSpent() {
      const totalMinutes = this.data.reduce((sum, item) => sum + item.minutes, 0);
      return totalMinutes / this.data.length;
    }
  },
  methods: {
    toggleTable(event) {
      event.preventDefault();
      this.showTable = !this.showTable;
    }
  }
};
</script>

<style scoped>

h3 {
  text-align: left; /* Align title to the left */
  font-size: 15px;
  color: black;
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
