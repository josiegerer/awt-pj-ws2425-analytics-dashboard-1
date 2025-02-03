<template>
  <div class="performance-container">
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
        <!-- Assessment Performance -->
        <div class="grid-item assessment-performance-chart">
          <AssessmentPerformanceChart />
        </div>

        <!-- Daily Streak -->
        <div class="grid-item daily-streak">
          <DailyStreak />
        </div>

        <!-- Average Attempts Until Passed -->
        <div class="grid-item average-attempts">
          <AttemptsUntilPassedCard/>
        </div>

        <!-- Pass Rate Chart -->
        <div class="grid-item pass-rate-chart">
          <PassRateChart />
        </div>

        <!-- Course Completion Chart -->
        <div class="grid-item course-completion-chart">
          <CourseCompletionChart  />
        </div>

        <!-- Assessment Attempts -->
        <div class="grid-item assessment-attempts-chart">
          <AssessmentAttempts />
        </div>
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
/* Container */
.performance-container {
  position: relative;
  width: 100%;
  display: flex;
  flex-direction: column;
}

/* Navigation Container */
.nav-container {
  width: 100%;
  text-align: center;
  padding: 10px 0;
  border-radius: 8px;
  background-color: transparent !important;
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
  grid-template-columns: repeat(12, 1fr);
  grid-gap: 20px;
}

/* Grid Items */
.grid-item {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Layout Definition */
.assessment-performance-chart {
  grid-column: span 9; 
  grid-row: span 3;
}

.daily-streak {
  grid-column: span 3; 
  grid-row: span 1;
}

.average-attempts {
  grid-column: span 3;
  grid-row: span 1;
}

.pass-rate-chart {
  grid-column: span 3;
  grid-row: span 1;
}

.course-completion-chart {
  grid-column: span 9;
  grid-row: span 2;
}

.assessment-attempts-chart {
  grid-column: span 3;
  grid-row: span 2;
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
