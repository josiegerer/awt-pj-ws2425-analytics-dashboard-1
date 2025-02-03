<template>
  <div class="last-assessment-attempts">
    <h3>Assessment Attempts</h3>
    <ul>
      <li v-for="attempt in displayedAttempts" :key="attempt.id">
        <h4 class="assessment-title">{{ attempt.subcourse }}</h4>
        <p :class="{ passed: attempt.achieved === 'Passed', failed: attempt.achieved === 'Failed' }">
          Achieved: {{ attempt.achieved }}
        </p>
        <p>Score: {{ attempt.score }}%</p>
        <p>Last Attempt: {{ formatDate(attempt.timestamp) }}</p>
      </li>
    </ul>
    <button @click="toggleShowMore" class="view-more-button">
      {{ showMore ? 'Show Less' : 'Show More' }}
    </button>
  </div>
</template>

<script>
export default {
  name: 'LastAssessmentAttempts',
  data() {
    return {
      attempts: [],
      showMore: false,
    };
  },
  computed: {
    displayedAttempts() {
      return this.showMore ? this.attempts : this.attempts.slice(0, 3);
    },
  },
  methods: {
    getCookie(name) {
      const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
      return match ? match[2] : null;
    },
    async fetchAssessmentAttempts() {
      const token = this.getCookie('auth_token');
      if (!token) {
        console.error('No authentication token found.');
        return;
      }
      try {
        const [attemptsRes, effectivenessRes] = await Promise.all([
          fetch('http://localhost:8000/assessmentAttempts', {
            headers: { Authorization: `Bearer ${token}` }
          }),
          fetch('http://localhost:8000/learningEffectiveness', {
            headers: { Authorization: `Bearer ${token}` }
          })
        ]);

        if (!attemptsRes.ok || !effectivenessRes.ok) {
          throw new Error("Failed to fetch data");
        }

        const attemptsData = await attemptsRes.json();
        const effectivenessData = await effectivenessRes.json();

        this.processData(attemptsData, effectivenessData);
      } catch (error) {
        console.error(error);
      }
    },
    processData(attemptsData, effectivenessData) {
      if (!attemptsData || !effectivenessData.activitiesEfficiency) return;

      const scoredActivities = new Map();
      effectivenessData.activitiesEfficiency.forEach(activity => {
        if (activity.scores.length > 0) {
          const lastScore = activity.scores.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))[0];
          scoredActivities.set(activity.activityId, {
            score: lastScore.score,
            timestamp: lastScore.timestamp
          });
        }
      });

      this.attempts = Object.entries(attemptsData.activitiesScored)
        .filter(([activityId]) => scoredActivities.has(activityId))
        .map(([activityId, passed]) => ({
          id: activityId,
          subcourse: activityId.split('/').pop().replace(/_/g, ' '), // Extract and format subcourse name
          achieved: passed ? 'Passed' : 'Failed',
          score: scoredActivities.get(activityId).score,
          timestamp: scoredActivities.get(activityId).timestamp
        }))
        .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)); // Sort most recent first
    },
    formatDate(timestamp) {
      return new Date(timestamp).toLocaleDateString(); // Removes the hour, only keeps the date
    },
    toggleShowMore() {
      this.showMore = !this.showMore;
    },
  },
  mounted() {
    this.fetchAssessmentAttempts();
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
}
.last-assessment-attempts li {
  padding: 10px;
  cursor: pointer;
  border-bottom: 1px solid #ccc;
}
.assessment-title {
  font-size: 14px; /* Smaller title */
  font-weight: bold;
}
.passed {
  color: green;
  font-weight: bold;
}
.failed {
  color: red;
  font-weight: bold;
}
.view-more-button {
  margin-top: 10px;
  padding: 5px 10px;
  border: none;
  background-color: white;
  color: black;
  cursor: pointer;
}
h3 {
  text-align: left; /* Align title to the left */
  font-size: 15px;
  color: black;
}
</style>
