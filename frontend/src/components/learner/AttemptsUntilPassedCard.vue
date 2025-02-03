<template>
  <div class="attempts-until-passed-card">
    <h3>Average Attempts Until Passed</h3>
    <!-- Display "ø" only if average greater or equal to 1-->
    <p class="attempts-number">{{ averageAttempts !== "User didn't have an attempt yet." ? "ø " + averageAttempts : averageAttempts }}</p> 
  </div>
</template>
<script>
export default {
  name: 'AttemptsUntilPassedCard',
  data() {
    return {
      averageAttempts: "N/A",
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
        let totalAttempts = 0;
        let count = 0;

        // Sum only non-zero values and count them
        Object.values(attemptsData).forEach(attempts => {
          if (attempts !== 0) {
            totalAttempts += attempts;
            count++;
          }
        });

        if (count > 0) {
          this.averageAttempts = (totalAttempts / count).toFixed(2);
        } else {
          this.averageAttempts = "User didn't have an attempt yet.";
        }
        
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
