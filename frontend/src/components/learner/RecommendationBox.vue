<template>
  <div class="recommendation-box">
    <p>{{ recommendationMessage }}</p>
  </div>
</template>

<script>
export default {
  name: "RecommendationBox",
  data() {
    return {
      activityRevisits: undefined, // Define as reactive property
      assessmentPerformance: undefined, // Define as reactive property
      timeSpentOnActivities: undefined, // Define as reactive property
      attemptsUntilPassed: undefined, // Define as reactive property
    };
  },
  computed: {
    recommendationMessage() {
      const {
        activityRevisits,
        assessmentPerformance,
        timeSpentOnActivities,
        attemptsUntilPassed,
      } = this;

      // If any of the values are still undefined, show a loading message
      if (
        activityRevisits === undefined ||
        assessmentPerformance === undefined ||
        timeSpentOnActivities === undefined ||
        attemptsUntilPassed === undefined
      ) {
        return "Loading recommendations...";
      }

      // Recommendations for Learner (in development - can add more)

        // Low Performance
          if (assessmentPerformance < 50 && attemptsUntilPassed > 3) {
          return "You're making multiple attempts on assessments, but your scores are low. Focus on understanding the concepts rather than memorizing answers.";
          } else if (assessmentPerformance < 50 && timeSpentOnActivities < 60) {
          return "You're spending little time on activities and scoring low on assessments. This might mean you're struggling with the material. Take time to review and reflect on what you've learned.";
          } else if (timeSpentOnActivities > 120 && activityRevisits > 5 && assessmentPerformance < 50) {
          return "You're spending a lot of time and revisiting content frequently, but your assessment performance is low. This might mean you're struggling with the material despite your effort. Try breaking down the material into smaller parts.";
          } 

          // Moderate Performance
          else if (assessmentPerformance >= 50 && assessmentPerformance < 75) {
            if (timeSpentOnActivities < 60) {
              return "You're performing moderately well, but you may benefit from spending more time on learning activities to strengthen your understanding.";
            } else if (activityRevisits > 3) {
              return "You're reviewing the material multiple times, which is great! Keep refining your approach to improve your assessment scores further.";
            } else {
              return "You're doing well! Keep practicing to improve your consistency and reach a higher level of mastery.";
            }
          }

          // High Performance
          else if (assessmentPerformance >= 75) {
            if (assessmentPerformance >= 90 && attemptsUntilPassed === 1) {
              return "Excellent work! You're mastering assessments on the first attempt. Keep challenging yourself with more advanced topics.";
            } else if (timeSpentOnActivities > 100) {
              return "You're investing a lot of time in learning, and your high scores show the results. Keep up the great work and consider exploring deeper topics.";
            } else {
              return "You're performing at a high level! Maintain your momentum and challenge yourself to keep growing.";
            }
          }

          // Default Message
          else {
          return "You're doing great! Keep up the good work and continue to challenge yourself.";
          }

    },
  },
  methods: {
    getCookie(name) {
      const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
      return match ? match[2] : null;
    },
    async recommendationBoxData() {
      const token = this.getCookie("auth_token");

      if (!token) {
        console.error("No authentication token found.");
        return;
      }

      try {
        // Fetch all metrics
        const [
          activityRevisitsResponse,
          assessmentPerformanceResponse,
          timeSpentOnActivitiesResponse,
          attemptsUntilPassedResponse,
        ] = await Promise.all([
          fetch("http://localhost:8000/activityRevists/learner", {
            headers: { Authorization: `Bearer ${token}` },
          }),
          fetch("http://localhost:8000/assessmentPerformance/learner", {
            headers: { Authorization: `Bearer ${token}` },
          }),
          fetch("http://localhost:8000/timeSpentOnActivities/learner", {
            headers: { Authorization: `Bearer ${token}` },
          }),
          fetch("http://localhost:8000/attemptsUntilPassed", {
            headers: { Authorization: `Bearer ${token}` },
          }),
        ]);

        // Parse responses
        const activityRevisitsData = await activityRevisitsResponse.json();
        const assessmentPerformanceData = await assessmentPerformanceResponse.json();
        const timeSpentOnActivitiesData = await timeSpentOnActivitiesResponse.json();
        const attemptsUntilPassedData = await attemptsUntilPassedResponse.json();

        // Calculate average activity revisits
        const totalActivityRevisits = activityRevisitsData.activitiesVisits.reduce(
          (sum, activity) => sum + activity.visits,
          0
        );
        this.activityRevisits = (
          totalActivityRevisits / activityRevisitsData.activitiesVisits.length
        ).toFixed(2);

        console.log("TOTAL ACTIVITY REVISITS", this.activityRevisits);

        // Calculate average assessment performance
        const totalAssessmentPerformance = assessmentPerformanceData.subcourses.reduce(
          (sum, subcourse) => sum + subcourse.progress,
          0
        );
        this.assessmentPerformance = (
          totalAssessmentPerformance / assessmentPerformanceData.subcourses.length
        ).toFixed(2);

        console.log("TOTAL ASSESSMENT POINTS", this.assessmentPerformance);

        // Calculate average time spent on activities (in minutes)
        const totalTimeSpentOnActivities = timeSpentOnActivitiesData.activities.reduce(
          (sum, activity) => sum + activity.duration,
          0
        );
        this.timeSpentOnActivities = (
          totalTimeSpentOnActivities / timeSpentOnActivitiesData.activities.length / 60
        ).toFixed(2); // Convert to minutes

        console.log("TOTAL TIME SPENT", this.timeSpentOnActivities);

        // Calculate average attempts until passed
        const attemptsData = attemptsUntilPassedData.attemptsUntilPassed || {};
        let totalAttempts = 0;
        let count = 0;

        // Sum only non-zero values and count them
        Object.values(attemptsData).forEach((attempts) => {
          if (attempts !== 0) {
            totalAttempts += attempts;
            count++;
          }
        });

        if (count > 0) {
          this.attemptsUntilPassed = (totalAttempts / count).toFixed(2);
        } else {
          this.attemptsUntilPassed = "User didn't have an attempt yet.";
        }

        console.log("TOTAL AVERAGE ATTEMPTS", this.attemptsUntilPassed);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
  },
  created() {
    this.recommendationBoxData();
  },
};
</script>
