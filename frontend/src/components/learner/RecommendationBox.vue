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

      // Recommendations for Learner (in development - can add more) -> use averages of students in future
        const LOW_PERFORMANCE_THRESHOLD = 50;
        const HIGH_PERFORMANCE_THRESHOLD = 75;
        const MIN_TIME_SPENT = 90;
        const DOUBLE_TIME_SPENT = 180;
        const HIGH_REVISIT_RATE = 5;
        const HIGH_ATTEMPTS_PASSED = 3;

        const getRandomMessage = (messages) => messages[Math.floor(Math.random() * messages.length)];

        // Low Performance
        if (assessmentPerformance < LOW_PERFORMANCE_THRESHOLD) {
          if (attemptsUntilPassed > HIGH_ATTEMPTS_PASSED) {
            return getRandomMessage([
              "You're making multiple attempts on assessments, but your scores are low. Focus on understanding the concepts rather than memorizing answers.",
              "It's great that you're trying again, but consider reviewing key concepts before retaking assessments.",
              "Try breaking the problem into smaller parts before attempting again. Understanding the basics will improve your score."
            ]);
          } else if (timeSpentOnActivities < MIN_TIME_SPENT) {
            return getRandomMessage([
              "You're spending little time on activities and scoring low on assessments. Take more time to review and reflect on what you've learned.",
              "Increase your engagement with the material to improve your performance. Spending extra time can help.",
              "Rushing through activities may hurt your understanding. Slow down and review the key points carefully."
            ]);
          } else if (timeSpentOnActivities > DOUBLE_TIME_SPENT && activityRevisits > HIGH_REVISIT_RATE) {
            return getRandomMessage([
              "You're spending a lot of time and revisiting content frequently, but your performance is still low. Try breaking down the material into smaller, focused study sessions.",
              "Consider changing your approach. Maybe a different learning style (videos, notes, or quizzes) will help.",
              "Revisiting material is good, but are you actively engaging with it? Try taking notes or teaching someone else."
            ]);
          } else {
            return "Your performance is currently low, but every challenge is a learning opportunity! Focus on reviewing core concepts, practicing regularly, and seeking clarification where needed.";
          }
        }

          // Moderate Performance
          else if (assessmentPerformance >= LOW_PERFORMANCE_THRESHOLD && assessmentPerformance < HIGH_PERFORMANCE_THRESHOLD) {
            //moderate performance but little time spent (assuming the average duration of a course is around 60)
            if (timeSpentOnActivities < MIN_TIME_SPENT) {
              return getRandomMessage([
                "You're performing moderately well, but you may benefit from spending more time on learning activities to strengthen your understanding.",
                "Spending just a little extra time on activities could push your scores even higher!",
                "Consider revisiting past materials or taking more time on each task to solidify your understanding."
              ]);
            // moderate performance but much time spent (assuming the average duration of a course is around 60)
            } else if (timeSpentOnActivities > DOUBLE_TIME_SPENT) { 
              return getRandomMessage([
                "You're investing a lot of time in learning. Consider refining your study methods to improve efficiency without overextending your sessions.",
                "Quality over quantity! Are you focusing on key concepts, or just spending extra time? Try summarizing key points to save time.",
                "Avoid burnout by setting study limits and focusing on high-impact learning activities."
              ]);
            // moderate performance but high revisit rate
            } else if (activityRevisits > HIGH_REVISIT_RATE) {
              return getRandomMessage([
                "You're reviewing material multiple times, which shows dedication! Try summarizing key ideas instead of just rereading.",
                "You have a great habit of revisiting material! See if you can learn the same concepts faster next time.",
                "Revisiting helps, but active recall (quizzing yourself) will make your learning even stronger!"
              ]);
            // moderate performance but multiple attempts needed
            } else if (attemptsUntilPassed > HIGH_ATTEMPTS_PASSED) {
              return getRandomMessage([
                "You're making multiple attempts but maintaining a moderate score. Try spending more time reviewing study materials first.",
                "Before retaking an assessment, ask yourself: Do I really understand the concept, or just remember the last attempt?",
                "If you find yourself retaking assessments often, consider asking for help or breaking down the material differently."
              ]);
            }else {
              return "You're doing good! Keep practicing to improve your consistency and reach a higher level of mastery.";
            }
          }

          // High Performance
          else if (assessmentPerformance >= HIGH_PERFORMANCE_THRESHOLD) {
            //high score & one attempt
            if (assessmentPerformance >= 90 && attemptsUntilPassed === 1) {
              return getRandomMessage([
                "Excellent work! You're mastering assessments on the first attempt. Keep challenging yourself with more advanced topics.",
                "You're on fire! If this feels too easy, try exploring additional resources or harder exercises.",
                "Top performance! Consider mentoring others or sharing your learning strategies with peers."
              ]);
            } else if (attemptsUntilPassed === 1 && timeSpentOnActivities < MIN_TIME_SPENT) {
              return getRandomMessage([
                "You're scoring high with minimal study time. Keep up the efficiency while ensuring deep understanding.",
                "Efficiency is great, but make sure you're truly grasping concepts, not just answering correctly.",
                "Quick learning is impressive! Make sure you're retaining knowledge for long-term success."
              ]);
            // great performance but much time spent (assuming the average duration of a course is around 60)
            } else if (timeSpentOnActivities > DOUBLE_TIME_SPENT) {
              return getRandomMessage([
                "You're investing a lot of time in learning, and your high scores show it. Consider optimizing your study time while maintaining results.",
                "You’ve got great dedication! Try setting time limits to prevent burnout while keeping up your high scores.",
                "If you're studying a lot and already performing well, consider helping others or applying your knowledge in real-world situations."
              ]);
            // great performance but little time spent (assuming the average duration of a course is around 60)
            } else if (timeSpentOnActivities < MIN_TIME_SPENT) {
              return getRandomMessage([
                "You're doing great with minimal study time, but consider deepening your understanding by reviewing more.",
                "High scores with little time? Make sure you're absorbing information, not just answering quickly!",
                "Your approach is working well! If you want to retain knowledge long-term, spend a little more time reviewing key concepts."
              ]);
            // generally good
            } else {
              return getRandomMessage([
                "You're performing at a good level! Maintain your momentum and challenge yourself to keep growing.",
                "Excellent progress! Keep up your learning habits and aim even higher.",
                "You're excelling! Keep pushing yourself to stay ahead and explore new challenges."
          ]);
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
