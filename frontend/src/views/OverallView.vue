<template>
  <div class="overall-container">
    <!-- Navigation -->
    <div class="nav-container">
      <nav v-if="showHeader" class="nav-buttons">
        <button @click="navigateTo('/overall')">Overall</button>
        <button @click="navigateTo('/performance')">Performance</button>
        <button @click="navigateTo('/engagement')">Engagement</button>
      </nav>
    </div>

    <!-- Dashboard Content -->
    <div class="dashboard">
      <div class="grid-container">
        <!-- Time Spent Daily -->
        <div class="grid-item time-spent-daily">
          <TimeSpentDaily />
        </div>

        <!-- Learning Effectiveness Chart -->
        <div class="grid-item learning-effectiveness">
          <LearningEffectivenessChart />
        </div>

        <!-- Daily Streak -->
        <div class="grid-item daily-streak">
          <DailyStreak />
        </div>

        <!-- Recommendation Box -->
        <div class="grid-item recommendation-box">
          <RecommendationBox />
        </div>

        <!-- Course Completion Chart -->
        <div class="grid-item course-completion-chart">
          <CourseCompletionChart />
        </div>
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
      showHeader: true, 
    }
  },
  methods: {
    navigateTo(route) {
      this.$router.push(route);
    }
  }
};
</script>

<style scoped>
/* Container for overall layout */
.overall-container {
  position: relative;
  width: 100%;
  display: flex;
  flex-direction: column;
}

/* Navigation container */
.nav-container {
  width: 100%;
  text-align: center;
  padding: 10px 0;
}

/* Navigation Buttons */
.nav-buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.nav-buttons button {
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  background-color: #c40d1e;
  color: white;
  cursor: pointer;
  border-radius: 5px;
  transition: background 0.3s;
}

.nav-buttons button:hover {
  background-color: #9e0b19;
}


/* Grid Layout */
.grid-container {
  display: grid;
  grid-template-rows: repeat(12, auto);
  grid-template-columns: repeat(12, 1fr);
  grid-gap: 20px;
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
  grid-column: span 5;
  grid-row: span 3;
}

.daily-streak {
  grid-column: span 3;
  grid-row: span 1;
}

.recommendation-box {
  grid-column: span 3;
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
  grid-column: span 12;
  grid-row: span 12;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .grid-container {
    grid-template-columns: repeat(6, 1fr);
  }

  .grid-item {
    grid-column: span 6;
  }

  .nav-buttons {
    flex-direction: column;
  }
}
</style>