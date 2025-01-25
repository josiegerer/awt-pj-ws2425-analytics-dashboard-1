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
        <!-- Pass Rates -->
        <div class="grid-item pass-rates">
          <PassRatesChart :data="passRatesData" />
        </div>

        <!-- Assessment Marks -->
        <div class="grid-item assessment-marks">
          <AssessmentMarks :data="assessmentMarksData" />
        </div>

        <!-- Active Users -->
        <div class="grid-item active-users">
          <ActiveUsers :activeUsers="activeUsers" :change="activeUsersChange" />
        </div>

        <!-- Activity Revisits -->
        <div class="grid-item activity-revisits">
          <ActivityRevisits :data="aggregatedRevisitsData" />
        </div>

        <!-- Course Completion -->
        <div class="grid-item course-completion">
          <CourseCompletion :courses="courseCompletionData" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import jwtDecode from 'jwt-decode';
import PassRatesChart from '../components/educator/PassRatesChart.vue';
import AssessmentMarks from '../components/educator/AssessmentMarks.vue';
import ActivityRevisits from '../components/learner/ActivityRevisits.vue';
import ActiveUsers from '../components/educator/ActiveUsers.vue';
import CourseCompletion from '../components/educator/CourseCompletion.vue';

export default {
  name: 'EducatorDashboard',
  components: {
    PassRatesChart,
    AssessmentMarks,
    ActivityRevisits,
    ActiveUsers,
    CourseCompletion,
  },
  data() {
    return {
      userName: 'Educator',
      passRatesData: {
        passed: 75,
        failed: 25
      },
      assessmentMarksData: [
        { name: 'A1', averageGrade: 85 },
        { name: 'A2', averageGrade: 56 },
        { name: 'A3', averageGrade: 92 },
        { name: 'A4', averageGrade: 88 },
        { name: 'A5', averageGrade: 95 },
        { name: 'A6', averageGrade: 20 }
      ],
      aggregatedRevisitsData: [
        { course: "Course 1", count: 150, change: "+100 in the last 30 days" },
        { course: "Course 2", count: 130, change: "+80 in the last 30 days" },
        { course: "Course 3", count: 80, change: "+45 in the last 30 days" }, 
        { course: "Course 1", count: 150, change: "+100 in the last 30 days" },
        { course: "Course 2", count: 130, change: "+80 in the last 30 days" },
        { course: "Course 3", count: 80, change: "+45 in the last 30 days" },
      ],
      activeUsers: 120,
      activeUsersChange: -65,
      courseCompletionData: [
  {
    id: 1,
    name: "Course 1",
    totalStudents: 89,
    subcourses: [
      {
        id: 1,
        name: "Subcourse 1",
        totalStudents: 89,
        assessments: [
          { id: 1, name: "Assessment 1", passedStudents: 70, totalStudents: 89, passRate: 79 },
          { id: 2, name: "Assessment 2", passedStudents: 50, totalStudents: 89, passRate: 56 },
        ],
        completionRate: 40,
      },
    ],
    completionRate: 20,
  },
]
    };
  },
  created() {
    const token = localStorage.getItem('token');
    if (token) {
      const decodedToken = jwtDecode(token);
      this.userName = decodedToken.name;
    }
  }
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
  grid-column: span 4;
  grid-row: span 2;
}

.assessment-marks {
  grid-column: span 5;
  grid-row: span 2;
}

.active-users {
  grid-column: span 3;
  grid-row: span 1; /* Half height */
}

.course-completion {
  grid-column: span 12;
  grid-row: span 2;
}

.activity-revisits {
  grid-column: span 3;
  grid-row: span 1;
}

@media (max-width: 768px) {
  .grid-container {
    grid-template-columns: repeat(6, 1fr);
  }

  .pass-rates,
  .assessment-marks,
  .activity-revisits,
  .active-users,
  .course-completion {
    grid-column: span 6;
  }
}
</style>