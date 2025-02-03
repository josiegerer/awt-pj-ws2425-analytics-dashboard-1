<template>
  <div class="recommendation-box">
    <p>{{ recommendationMessage }}</p>
  </div>
</template>

<script>
export default {
  name: "RecommendationBox",
  computed: {
    recommendationMessage() {
      const {
        activityRevisits,
        assessmentPerformance,
        activeHoursThisWeek,
        passRate,
        attemptsUntilPassed,
      } = this;

      //Recommendations

      //
      if (assessmentPerformance < 50 && attemptsUntilPassed > 3) {
        return "You're making multiple attempts on assessments, but your scores are low. Focus on understanding the concepts rather than memorizing answers.";
      //
      } else if (assessmentPerformance < 50 && activeHoursThisWeek < 5) {
        return "You're completing fewer activities and scoring low on assessments. This might mean you're struggling with the material. Take time to review and reflect on what you've learned.";
      //
      } else if (activeHoursThisWeek < 5 && passRate < 50) {
        return "You're spending a lot of time, completing fewer activities, and achieving low pass rates. This might mean your study methods could be more effective. Try using active learning techniques.";
      //
      } else if (passRate < 50 && activeHoursThisWeek > 6 && activityRevisits > 5) {
        return "You're spending a lot of time and revisiting content frequently, but your pass rate is low. This might mean you're struggling with the material despite your effort. Try breaking down the material into smaller parts.";
      //
      } else {
        return `You're doing great! Keep up the good work and continue to challenge yourself.
                Activity Revisits: ${activityRevisits} times
                Assessment Performance: ${assessmentPerformance}%
                Course Completion Rate: ${activeHoursThisWeek}%
                Pass Rate: ${passRate}%
                Attempts on Assessments: ${attemptsUntilPassed} attempts%`;
      }
    },
  },
  methods: {
    async fetchData() {
      try {
        const authToken = document.cookie.match(/(^| )auth_token=([^;]+)/)?.[2];
        if (!authToken) {
          console.error("Authentication token not found.");
          return;
        }

        // Fetch all metrics
        const [
          activityRevisitsResponse,
          assessmentPerformanceResponse,
          activeHoursThisWeekResponse,
          passRateResponse,
          attemptsUntilPassedResponse,
        ] = await Promise.all([
          fetch("http://localhost:8000/activityRevists/learner", {
            headers: { Authorization: `Bearer ${authToken}` },
          }),
          fetch("http://localhost:8000/assessmentPerformance/learner", {
            headers: { Authorization: `Bearer ${authToken}` },
          }),
          fetch("http://localhost:8000/activeHoursThisWeek", {
            headers: { Authorization: `Bearer ${authToken}` },
          }),
          fetch("http://localhost:8000/passRate/learner", {
            headers: { Authorization: `Bearer ${authToken}` },
          }),
          fetch("http://localhost:8000/attemptsUntilPassed", {
          headers: { Authorization: `Bearer ${authToken}` },
        }),
        ]);

        // Parse responses
        this.activityRevisits = (await activityRevisitsResponse.json()).count;
        this.assessmentPerformance = (await assessmentPerformanceResponse.json()).averageScore;
        this.activeHoursThisWeek = (await activeHoursThisWeekResponse.json()).hours;
        this.passRate = (await passRateResponse.json()).rate;
        this.attemptsUntilPassed = (await attemptsUntilPassedResponse.json()).attempts;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
  },
  created() {
    this.fetchData();
  },
};
</script>
