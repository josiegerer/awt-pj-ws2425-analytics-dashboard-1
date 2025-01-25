<template>
    <nav v-if="showHeader" class="nav-buttons">
      <button @click="navigateTo('/overall')">Overall</button>
      <button @click="navigateTo('/performance')">Performance</button>
      <button @click="navigateTo('/engagement')">Engagement</button>
    </nav>
  <div class="dashboard">
    <div class="grid-container">
      <!-- Assessment Points Over Time -->
      <div class="grid-item assessment-performance-chart">
        <AssessmentPerformanceChart />
      </div>

      <!-- Daily Streak  -->
      <div class="grid-item daily-streak">
        <DailyStreak :streak="dailyStreak" />
      </div>

      <!-- Average Attempts Until Passed -->
      <div class="grid-item average-attempts">
        <AttemptsUntilPassedCard :data="attemptsUntilPassed" />
      </div>
      
      <!-- Pass Rate Chart-->
      <div class="grid-item pass-rate-chart">
        <PassRateChart :data="passRateData" />
      </div>

      <!-- Course Completion Chart-->
      <div class="grid-item course-completion-chart">
        <CourseCompletionChart :courses="coursesData" />
      </div>

      <!-- Assessment Attempts  -->
      <div class="grid-item assessment-attempts-chart">
        <AssessmentAttempts :data="assessmentAttemptsData" />
      </div>
    </div>
  </div>
</template>

<script>
import CourseCompletionChart from '../components/learner/CourseCompletionChart.vue';
import DailyStreak from '../components/learner/DailyStreak.vue';
import PassRateChart from '../components/learner/PassRateChart.vue';
import AssessmentAttempts from '../components/learner/AssessmentAttempts.vue';
import AttemptsUntilPassedCard from '../components/learner/AttemptsUntilPassedCard.vue';
import AssessmentPerformanceChart from '../components/learner/AssessmentPerformanceChart.vue'; 

export default {
  name: 'PerformanceView',
  components: {
    CourseCompletionChart,
    DailyStreak,
    PassRateChart,
    AssessmentAttempts,
    AttemptsUntilPassedCard,
    AssessmentPerformanceChart, 
  },
  data() {
    return {
      dailyStreak: 3,
      attemptsUntilPassed: 5,
      coursesData: [
        {
          id: 1,
          name: "Main Course 1",
          progress: 50,
          completedAssessments: 5,
          totalAssessments: 10,
          open: false,
          subcourses: [
            {
              id: 1,
              name: "Subcourse 1",
              progress: 60,
              completedAssessments: 3,
              totalAssessments: 5,
              open: false,
              assessments: [
                { id: 1, name: "Assessment 1", status: "passed" },
                { id: 2, name: "Assessment 2", status: "not passed" },
              ],
            },
            {
              id: 2,
              name: "Subcourse 2",
              progress: 40,
              completedAssessments: 2,
              totalAssessments: 5,
              open: false,
              assessments: [
                { id: 3, name: "Assessment 3", status: "passed" },
                { id: 4, name: "Assessment 4", status: "not passed" },
              ],
            },
          ],
        },
        {
          id: 2,
          name: "Main Course 2",
          progress: 70,
          completedAssessments: 7,
          totalAssessments: 10,
          open: false,
          subcourses: [
            {
              id: 3,
              name: "Subcourse 3",
              progress: 80,
              completedAssessments: 4,
              totalAssessments: 5,
              open: false,
              assessments: [
                { id: 5, name: "Assessment 5", status: "passed" },
                { id: 6, name: "Assessment 6", status: "not passed" },
              ],
            },
          ],
        },
      ],
    };
  },
};
</script>

<style scoped>
.grid-container {
  display: grid;
  grid-template-columns: repeat(12, 1fr); /* Create 12 equal columns */
  gap: 20px;
  grid-template-rows: repeat(12, 50 px) ;

}

.grid-item {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Assessment Points Over Time*/
.assessment-performance-chart {
  grid-column: span 9; 
  grid-row: span 3;
}

/* Daily Streak */
.daily-streak {
  grid-column: span 3; 
  grid-row: span 1;
}

/* Average Attempts Until Passed */
.average-attempts {
  grid-column: span 3;
  grid-row: span 1;
}

/* Pass Rate Chart */
.pass-rate-chart {
  grid-column: span 3;
  grid-row: span 1;
}

/* Course Completion Chart */
.course-completion-chart {
  grid-column: span 9;
  grid-row: span 2;
}

/* Assessment Attempts */
.assessment-attempts-chart {
  grid-column: span 3;
  grid-row: span 2;
}
</style>
