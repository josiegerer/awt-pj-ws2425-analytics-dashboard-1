<template>
  <div class="attempts-until-passed-card">
    <h3>Average Attempts Until Passed</h3>
    <p class="attempts-number">ø {{ averageAttempts }}</p> <!-- Prepending "ø" -->
  </div>
</template>

<script>
export default {
  name: 'AttemptsUntilPassedCard',
  data() {
    return {
      averageAttempts: 0,
    };
  },
  methods: {
    getCookie(name) {
      const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
      return match ? match[2] : null;
    },

    async fetchAttemptsUntilPassed() {
      const token = this.getCookie("auth_token");

      if (!token) {
        console.error("No authentication token found.");
        return;
      }

      try {
        const response = await fetch("http://localhost:8000/attemptsUntilPassed", {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) {
          console.error("Error fetching attempts until passed:", response.statusText);
          return;
        }

        const data = await response.json();
        console.log("Received Attempts Until Passed Data:", data);

        const attemptsData = data.attemptsUntilPassed || {};
        const totalAssessments = 15; // Expected number of assessments
        let totalAttempts = 0;

        Object.values(attemptsData).forEach(attempts => {
          totalAttempts += attempts + 1; // Adding 1 to include the first attempt
        });

        // If some assessments are missing from data, assume first attempt (1) for them
        const missingAssessments = totalAssessments - Object.keys(attemptsData).length;
        totalAttempts += missingAssessments; 

        // Calculate average
        this.averageAttempts = (totalAttempts / totalAssessments).toFixed(2);
      } catch (error) {
        console.error("Error fetching attempts until passed:", error);
      }
    },
  },
  mounted() {
    this.fetchAttemptsUntilPassed();
  },
};
</script>

<style scoped>
.attempts-number {
  font-size: 24px;
  font-weight: bold;
  color: black;
  text-align: center;
}

h3 {
  text-align: left;
  font-size: 15px;
  color: black;
}
</style>

  