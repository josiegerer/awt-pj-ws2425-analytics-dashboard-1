<template>
  <div class="educator-container">
    <!-- Header -->
    <header class="dashboard-header">
      <div class="logo-greeting">
        <div class="logo">
          <img src="@/assets/lms-Logo.png" alt="LMS Logo" />
        </div>
        <div class="greeting">
          <h1>Welcome, {{ userName }}</h1>
        </div>
      </div>
    </header>

    <!-- Dashboard Content -->
    <div class="dashboard">
      <div class="grid-container">

        <!-- Assessment Marks -->
        <div class="grid-item assessment-marks">
          <AssessmentMarks />
        </div>
        
        <!-- Pass Rates -->
        <div class="grid-item pass-rates">
          <PassRatesInstructor />
        </div>

        <!-- Educator Ranking -->
        <div class="grid-item educator-rating">
          <EducatorRating />
        </div>

        <!-- Activity Revisits -->
        <div class="grid-item activity-revisits">
          <ActivityRevisits />
        </div>
      
        <!-- Course Completion -->
        <div class="grid-item course-completion">
          <CourseCompletion />
        </div>
      

      </div>
    </div>
  </div>
</template>

<script>
import PassRatesInstructor from '../components/educator/PassRatesInstructor.vue';
import AssessmentMarks from '../components/educator/AssessmentMarks.vue';
import ActivityRevisits from '../components/educator/ActivityRevisits.vue';
import CourseCompletion from '../components/educator/CourseCompletion.vue';
import EducatorRating from '@/components/educator/EducatorRating.vue';

// insert all charts
export default {
  name: 'EducatorDashboard',
  components: {
    PassRatesInstructor,
    AssessmentMarks,
    ActivityRevisits,
    CourseCompletion,
    EducatorRating
  },
  data() {
    return {
      userName: 'Instructor',
      adminToken: localStorage.getItem("instructorToken"), // Load admin token
    };
  },
};
</script>

<style scoped>
.educator-container {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  width: 100%;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  grid-gap: 20px;
  padding: 20px;
  background-color: #f5f5f5;
}

.grid-item {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Grid Layout */
.pass-rates {
  grid-column: span 6;
  grid-row: span 1;
}

.assessment-marks {
  grid-column: span 6;
  grid-row: span 1;
}

.activity-revisits {
  grid-column: span 6;
  grid-row: span 1;
}

.educator-rating{
  grid-column: span 6;
  grid-row: span 1;
}

.course-completion {
  grid-column: span 12;
  grid-row: span 1;
}

@media (max-width: 768px) {
  .grid-container {
    grid-template-columns: repeat(6, 1fr);
  }
}
</style>