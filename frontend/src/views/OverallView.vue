<template>
      <nav v-if="showHeader" class="nav-buttons">
      <button @click="navigateTo('/overall')">Overall</button>
      <button @click="navigateTo('/performance')">Performance</button>
      <button @click="navigateTo('/engagement')">Engagement</button>
    </nav>
  <div class="dashboard">
    <div class="grid-container">
      <!-- Time Spent Daily -->
      <div class="grid-item time-spent-daily">
        <TimeSpentDaily :data="timeSpentDailyData" />
      </div>
      <!-- Learning Effectiveness Chart -->
      <div class="grid-item learning-effectiveness">
        <LearningEffectivenessChart :data="learningEffectivenessData" />
      </div>
      <!-- Daily Streak -->
      <div class="grid-item daily-streak">
        <DailyStreak :streak="dailyStreak" />
      </div>
      <!-- Recommendation Box -->
      <div class="grid-item recommendation-box">
        <RecommendationBox />
      </div>
      <!-- Course Completion Chart -->
      <div class="grid-item course-completion-chart">
        <CourseCompletionChart :courses="coursesData" />
      </div>
    </div>
  </div>
</template>

<script>
import TimeSpentDaily from "../components/learner/TimeSpentDaily.vue";
import CourseCompletionChart from "../components/learner/CourseCompletionChart.vue";
import DailyStreak from "../components/learner/DailyStreak.vue";
import LearningEffectivenessChart from "../components/learner/LearningEffectivenessChart.vue";
import RecommendationBox from "../components/learner/RecommendationBox.vue";


export default {
  name: "OverallView",
  components: {
    TimeSpentDaily,
    CourseCompletionChart,
    DailyStreak,
    LearningEffectivenessChart,
    RecommendationBox
  },
  data() {
    return {
      timeSpentDailyData: [
        { day: "Monday", minutes: 120 },
        { day: "Tuesday", minutes: 90 },
        { day: "Wednesday", minutes: 60 },
        { day: "Thursday", minutes: 150 },
        { day: "Friday", minutes: 200 },
        { day: "Saturday", minutes: 180 },
        { day: "Sunday", minutes: 100 },
      ],
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
      dailyStreak: 3,
      learningEffectivenessData: [
        { x: 10, y: 20 },
        { x: 20, y: 30 },
        { x: 30, y: 10 },
        { x: 40, y: 50 },
      ],
    };
  },
};
</script>

<style scoped>

.grid-container {
  display: grid;
  grid-template-rows: repeat(12, auto); /* Define flexible rows */
  grid-template-columns: repeat(12, 1fr); /* 12 equal columns */
  grid-gap: 20px; /* Space between items */
  grid-template-areas:
    "time-spent-daily learning-effectiveness daily-streak recommendation-box"
    "time-spent-daily learning-effectiveness daily-streak recommendation-box"
    "course-completion-chart course-completion-chart course-completion-chart course-completion-chart";
}

.grid-item {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Layout Definition */
.time-spent-daily {
  grid-column: span 4;
  grid-row: span 3;
}

.learning-effectiveness {
  grid-column: span 4;
  grid-row: span 3;
}

.daily-streak {
  grid-column: span 4;
  grid-row: span 1;
}

.recommendation-box {
  grid-column: span 4;
  grid-row: span 2;
  background-image: linear-gradient(to right, #ff6c00, #c40d1e);
  padding: 20px;
  color: white;
  font-family: 'Inter', sans-serif;
  font-weight: bold;
  display: flex;
  justify-content: center; 
  align-items: center;    
  text-align: center;
}

.course-completion-chart {
  grid-column: span 12; /* Full width */
  grid-row: span 12; 
}

</style>