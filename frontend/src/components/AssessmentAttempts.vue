<template>
    <div class="last-assessment-attempts">
      <h3>Assessment Attempts</h3>
      <ul>
        <li v-for="attempt in attempts" :key="attempt.id" @click="viewMore(attempt.id)">
          <h3>{{ attempt.subcourse }}</h3>
          <p>Points: {{ attempt.points }}</p>
          <p :class="{ passed: attempt.achieved === 'Passed', failed: attempt.achieved === 'Failed' }">
            Achieved: {{ attempt.achieved }}
          </p>
          <button @click.stop="viewMore(attempt.id)">View More</button>
        </li>
      </ul>
    </div>
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
  </template>
  

<script>
export default {
    name: 'LastAssessmentAttempts',
    data() {
        return {
            attempts: [
                // Example data, replace with actual data
                { id: 1, subcourse: 'Auf Bäume klettern', points: 85, achieved: 'Passed' },
                { id: 2, subcourse: 'Bäume schützen', points: 90, achieved: 'Passed' },
                { id: 3, subcourse: 'Bäume auskappen', points: 45, achieved: 'Failed' },
            ],
        };
    },
    methods: {
        viewMore(id) {
            // Logic to view more details about the assessment attempt
            console.log('View more details for attempt ID:', id);
        },
    },
};
</script>

<style scoped>
.last-assessment-attempts {
  padding: 20px;
}

.last-assessment-attempts ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column; /* Stack list items vertically */
  gap: 15px; /* Add spacing between list items */
}

.last-assessment-attempts li {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  cursor: pointer;
  justify-content: space-between; 
}

.last-assessment-attempts li:hover {
  background-color: #f9f9f9;
}

.last-assessment-attempts button {
  margin-top: 10px;
}

/* Add styles for Passed and Failed */
.passed {
  color: green;
  font-weight: bold;
}

.failed {
  color: red;
  font-weight: bold;
}

h3 {
  text-align: left; /* Align title to the left */
  font-size: 15px;
  color: black;
  margin-bottom: 10px;
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
  color: black;
}
</style>
