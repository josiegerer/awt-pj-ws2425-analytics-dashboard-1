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
          <th>Compared to Last Week (%)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in data" :key="item.activity">
          <td>{{ item.activity }}</td>
          <td>{{ item.current }}</td>
          <td :class="getComparisonClass(item)">
            {{ getComparison(item) }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

export default {
  name: "TimeSpent",
  components: {
    apexchart: VueApexCharts
  },
  props: {
    data: {
      type: Array,
      required: true,
      default: () => [
        { activity: "Activity 1", current: 120, previous: 100 },
        { activity: "Activity 2", current: 90, previous: 80 },
        { activity: "Activity 3", current: 60, previous: 70 },
        { activity: "Activity 4", current: 150, previous: 140 },
        { activity: "Activity 5", current: 200, previous: 180 },
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
          name: 'Current Week',
          data: this.data.map(item => item.current)
        },
        {
          name: 'Previous Week',
          data: this.data.map(item => item.previous)
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
            endingShape: 'rounded'
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
          categories: this.data.map(item => item.activity),
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
        colors: ['lightgrey', 'grey'], 
      };
    }
  },
  methods: {
    toggleTable() {
      this.showTable = !this.showTable;
      this.$emit('button-click');
    },
    getComparison(item) {
      const percentage = ((item.current - item.previous) / item.previous) * 100;
      return `${percentage.toFixed(2)}%`;
    },
    getComparisonClass(item) {
      return ((item.current - item.previous) / item.previous) * 100 >= 0 ? 'positive' : 'negative';
    }
  }
}
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
  font-size: 14px;
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

.positive {
  color: #49cb40;
}

.negative {
  color: #c40d1e;
}
</style>
