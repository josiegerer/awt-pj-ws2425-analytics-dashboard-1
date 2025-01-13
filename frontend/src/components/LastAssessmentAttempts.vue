<template>
    <div class="last-assessment-attempts">
      <h3>Last Assessment Attempts</h3>
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
</style>
