<template>
  <div class="dashboard">
    <div class="grid-container">
      <!-- Time Spent Daily -->
      <div class="grid-item time-spent-daily">
        <TimeSpentDaily :data="timeSpentDailyData" />
      </div>  
      <!-- Daily Streak -->
      <div class="grid-item daily-streak">
        <DailyStreak :streak="dailyStreak" />
      </div>
      <!-- Learning Effectiveness-->
      <div class="grid-item learning-effectiveness">
        <LearningEffectivenessChart />
      </div>
         <!-- Recommendation-->
         <div class="grid-item recommendation">
        <Recommendation />
      </div>
      <!-- Course Completion Chart -->
      <div class="grid-item course-completion-chart">
        <CourseCompletionChart :courses="coursesData" />
      </div>
    </div>
  </div>
</template>

<script>
import TimeSpentDaily from '../components/TimeSpentDaily.vue';
import CourseCompletionChart from '../components/CourseCompletionChart.vue';
import DailyStreak from '../components/DailyStreak.vue';
import Recommendation from '../components/Recommendation.vue';

export default {
  name: 'OverallView',
  components: {
    TimeSpentDaily,
    CourseCompletionChart,
    DailyStreak,
    Recommendation,
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
      lastAssessmentAttemptsData: [
        { id: 1, subcourse: "Subcourse 1", assessment: "Assessment 1", date: "2023-12-01", score: 85, status: "passed" },
        { id: 2, subcourse: "Subcourse 2", assessment: "Assessment 2", date: "2023-12-02", score: 70, status: "not passed" },
      ]
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
}

.grid-item {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Layout Definition */
.time-spent-daily {
  grid-column: span 9; /* Spans 9 columns */
  grid-row: span 2; /* Spans 2 rows */
}

.last-assessment-attempts {
  grid-column: span 3; /* Spans 3 columns */
  grid-row: span 2; /* Spans 2 rows */
}

.course-completion-chart {
  grid-column: span 9; /* Spans 12 columns */
  grid-row: span 2; /* Spans 2 rows */
}

.daily-streak {
  grid-column: span 3; /* Spans 3 columns */
  grid-row: span 1; /* Spans 1 row */
  height: span 1;
}

/* Responsive Design */
@media (max-width: 768px) {
  .grid-container {
    grid-template-columns: repeat(6, 1fr); /* Adjust to 6 columns */
  }

  .time-spent-daily,
  .course-completion-chart,
  .daily-streak,
  .last-assessment-attempts {
    grid-column: span 6; /* Full width for smaller screens */
  }
}
</style>
