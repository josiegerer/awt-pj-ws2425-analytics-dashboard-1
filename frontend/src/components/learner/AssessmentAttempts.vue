<template>
  <div class="last-assessment-attempts">
    <h3>Assessment Attempts</h3>
    <ul>
      <li v-for="attempt in displayedAttempts" :key="attempt.id" @click="viewMore(attempt.id)">
        <h3>{{ attempt.subcourse }}</h3>
        <p :class="{ passed: attempt.achieved === 'Passed', failed: attempt.achieved === 'Failed' }">
          Achieved: {{ attempt.achieved }}
        </p>
        <button @click.stop="viewMore(attempt.id)">View More</button>
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
        const response = await fetch('http://localhost:8000/assessmentAttempts', {
          headers: { Authorization: `Bearer ${token}` }
        });
        if (!response.ok) throw new Error("Failed to fetch assessment attempts");
        this.attempts = await response.json();
      } catch (error) {
        console.error(error);
      }
    },
    viewMore(id) {
      console.log("View more details for attempt ID:", id);
    },
    toggleShowMore() {
      this.showMore = !this.showMore;
    },
  },
  mounted() {
    this.fetchAttempts();
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
</style>
