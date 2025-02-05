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
      activityRevisits: null, 
      assessmentPerformance: null,
      timeSpentOnActivities: null,
      attemptsUntilPassed: null,
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
        activityRevisits === null ||
        assessmentPerformance === null ||
        timeSpentOnActivities === null ||
        attemptsUntilPassed === null
      ) {
        return "Loading recommendations...";
      }

      // Recommendations for Learner (in development - can add more)
        const LOW_PERFORMANCE_THRESHOLD = 50;
        const HIGH_PERFORMANCE_THRESHOLD = 75;
        const MIN_TIME_SPENT = 60;
        const DOUBLE_TIME_SPENT = 120;
        const HIGH_REVISIT_RATE = 5;
        const HIGH_ATTEMPTS_PASSED = 3;


        // Low Performance
        if (assessmentPerformance < LOW_PERFORMANCE_THRESHOLD) {
          if (attemptsUntilPassed > HIGH_ATTEMPTS_PASSED) {
            return "You're making multiple attempts on assessments, but your scores are low. Focus on understanding the concepts rather than memorizing answers.";
          } else if (timeSpentOnActivities < MIN_TIME_SPENT) {
            return "You're spending little time on activities and scoring low on assessments. Take more time to review and reflect on what you've learned.";
          } else if (timeSpentOnActivities > DOUBLE_TIME_SPENT && activityRevisits > HIGH_REVISIT_RATE) {
            return "You're spending a lot of time and revisiting content frequently, but your assessment performance is still low. Try breaking down the material into smaller, focused study sessions.";
          } else {
            return "Your performance is currently low, but every challenge is a learning opportunity! Focus on reviewing core concepts, practicing regularly, and seeking clarification where needed.";
          }
        }

          // Moderate Performance
          else if (assessmentPerformance >= LOW_PERFORMANCE_THRESHOLD && assessmentPerformance < HIGH_PERFORMANCE_THRESHOLD) {
            //moderate performance but little time spent (assuming the average duration of a course is around 60)
            if (timeSpentOnActivities < MIN_TIME_SPENT) {
              return "You're performing moderately well, but you may benefit from spending more time on learning activities to strengthen your understanding and retaining the gained knowledge.";
            // moderate performance but much time spent (assuming the average duration of a course is around 60)
            } else if (timeSpentOnActivities > DOUBLE_TIME_SPENT) { 
              return "You're investing a lot of time in learning. Consider refining your study methods to improve efficiency without overextending your study sessions.";
            // moderate performance but high revisit rate
            } else if (activityRevisits > HIGH_REVISIT_RATE) {
              return "You're reviewing the material multiple times, which shows dedication! However, try to absorb the key information more effectively during the initial sessions to reduce the need for frequent revisits and improve your assessment scores further.";
            // moderate performance but multiple attempts needed
            } else if (attemptsUntilPassed > HIGH_ATTEMPTS_PASSED) {
              return "You're making multiple attempts but maintaining a moderate score. Try spending more time reviewing the study material to improve your understanding.";
            }else {
              return "You're doing well! Keep practicing to improve your consistency and reach a higher level of mastery.";
            }
          }

          // High Performance
          else if (assessmentPerformance >= HIGH_PERFORMANCE_THRESHOLD) {
            //high score & one attempt
            if (assessmentPerformance >= 90 && attemptsUntilPassed === 1) {
              return "Excellent work! You're mastering assessments on the first attempt. Keep challenging yourself with more advanced topics.";
            } else if (attemptsUntilPassed === 1 && timeSpentOnActivities < MIN_TIME_SPENT) {
              return "You're scoring high with minimal attempts and study time. Keep up the efficiency while ensuring deep understanding.";
            // great performance but much time spent (assuming the average duration of a course is around 60)
            } else if (timeSpentOnActivities > DOUBLE_TIME_SPENT) {
              return "You're investing a lot of time in learning, and your high scores show the results. However, consider optimizing your study approach to reduce time while maintaining your performance. Focus on key concepts and avoid overstudying.";
            // great performance but little time spent (assuming the average duration of a course is around 60)
            } else if (timeSpentOnActivities < MIN_TIME_SPENT) {
              return "You have a great performance, but you may be able to deepen your understanding by spending more time on the activities. This will help you retain the knowledge over time.";
            // generally good
            } else {
              return "You're performing at a good level! Maintain your momentum and challenge yourself to keep growing.";
            }
          }

          // Default Message
          else {
          return "It looks like we don’t have enough data to provide recommendations yet. Start engaging with activities and assessments, and check back soon for personalized insights!";
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
          fetch("http://localhost:8000/dailyAverageScoreofTheWeek", {
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
        const totalAssessmentPerformance = assessmentPerformanceData.score || [];
          if (totalAssessmentPerformance.length > 0) {
            this.assessmentPerformance = Number(totalAssessmentPerformance[totalAssessmentPerformance.length - 1].averageScore);
          } else {
            this.assessmentPerformance = null;
          }

        console.log("TOTAL ASSESSMENT POINTS", this.assessmentPerformance);

        // Calculate average time spent on activities (in minutes)
        const totalTimeSpentOnActivities = timeSpentOnActivitiesData.activities.reduce(
          (sum, activity) => sum + activity.duration,
          0
        );
        this.timeSpentOnActivities = (
          totalTimeSpentOnActivities / timeSpentOnActivitiesData.activities.length 
        ).toFixed(2); 

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
