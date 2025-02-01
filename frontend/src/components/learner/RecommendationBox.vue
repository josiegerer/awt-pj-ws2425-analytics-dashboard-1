<template>
  <div class="recommendation-box">
    <p>{{ recommendationMessage }}</p>
  </div>
</template>

<script>
export default {
  name: "RecommendationBox",
  inject: ["activities", "totalTime", "passRate"],
  computed: {
    recommendationMessage() {
      const {
        activityRevisits,
        assessmentPerformance,
        courseCompletionRate,
        passRate,
        attemptsOnAssessments,
      } = this;

      //Recommendations

      //
      if (assessmentPerformance < 50 && attemptsOnAssessments > 3) {
        return "You're making multiple attempts on assessments, but your scores are low. Focus on understanding the concepts rather than memorizing answers.";
      //
      } else if (assessmentPerformance < 50 && courseCompletionRate < 50) {
        return "You're completing fewer activities and scoring low on assessments. This might mean you're struggling with the material. Take time to review and reflect on what you've learned.";
      //
      } else if (courseCompletionRate < 50 && passRate < 50 &&  this.timeSpent > 60) {
        return "You're spending a lot of time, completing fewer activities, and achieving low pass rates. This might mean your study methods could be more effective. Try using active learning techniques.";
      //
      } else if (passRate < 50 && this.timeSpent > 60 && activityRevisits > 5) {
        return "You're spending a lot of time and revisiting content frequently, but your pass rate is low. This might mean you're struggling with the material despite your effort. Try breaking down the material into smaller parts.";
      //
      } else {
        return `You're doing great! Keep up the good work and continue to challenge yourself.
                Time Spent: ${this.timeSpent} hours
                Activity Revisits: ${activityRevisits} times
                Assessment Performance: ${assessmentPerformance}%
                Course Completion Rate: ${courseCompletionRate}%
                Pass Rate: ${passRate}%
                Attempts on Assessments: ${attemptsOnAssessments} attempts%`;
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
          //timeSpentResponse,
          activityRevisitsResponse,
          assessmentPerformanceResponse,
          courseCompletionRateResponse,
          passRateResponse,
          attemptsOnAssessmentsResponse,
          learningEffectivenessResponse,
        ] = await Promise.all([
          //fetch("http://localhost:8000/timeSpentOnActivities/learner", {
            //headers: { Authorization: `Bearer ${authToken}` },
          //}),
          fetch("http://localhost:8000/activityRevisits", {
            headers: { Authorization: `Bearer ${authToken}` },
          }),
          fetch("http://localhost:8000/assessmentPerformance", {
            headers: { Authorization: `Bearer ${authToken}` },
          }),
          fetch("http://localhost:8000/courseCompletionRate", {
            headers: { Authorization: `Bearer ${authToken}` },
          }),
          fetch("http://localhost:8000/passRate/learner", {
            headers: { Authorization: `Bearer ${authToken}` },
          }),
          fetch("http://localhost:8000/assessmentAttempts", {
            headers: { Authorization: `Bearer ${authToken}` },
          }),
        ]);

        // Parse responses
        //this.timeSpent = (await timeSpentResponse.json()).totalTime;
        this.activityRevisits = (await activityRevisitsResponse.json()).count;
        this.assessmentPerformance = (await assessmentPerformanceResponse.json()).averageScore;
        this.courseCompletionRate = (await courseCompletionRateResponse.json()).rate;
        this.passRate = (await passRateResponse.json()).rate;
        this.attemptsOnAssessments = (await attemptsOnAssessmentsResponse.json()).attempts;
        this.learningEffectiveness = (await learningEffectivenessResponse.json()).effectiveness;
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
