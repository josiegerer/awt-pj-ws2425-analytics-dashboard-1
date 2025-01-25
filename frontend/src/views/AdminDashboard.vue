<template>
  <div class="admin-container">
    <!-- Dashboard Content -->
    <div class="dashboard">
      <div class="grid-container">
       
        <p class="subheader">Engagement</p>

        <!-- Users over time -->
        <div class="grid-item users-time">
          <UsersChart :data="usersOverTimeData" />
        </div>

        <!-- Popular Times -->
        <div class="grid-item popular-times">
          <PopularTimesChart :data="popularTimesData" />
        </div>

        <p class="subheader">Resource Utilization & Content Popularity</p>

        <!-- Active Users per Course -->
        <div class="grid-item active-users">
          <ActiveUsers :activeUsers="activeUsers" :change="activeUsersChange" />
        </div>

        <!--Total Users -->
        <div class="grid-item total-users">
          <TotalUsers :totalUsers="totalUsers" :change="totalUsersChange" />
        </div>

        <!--Total Courses -->
        <div class="grid-item total-courses">
          <TotalCourses :totalCourses="totalCourses" :change="totalCoursesChange" />
        </div>

        <!--Total Activities -->
        <div class="grid-item total-courses">
          <TotalActivities :totalActivities="totalActivities" :change="totalActivitiesChange" />
        </div>

        <!-- Search Trends -->
        <div class="grid-item search-trends">
          <SearchTrendsChart :data="searchTrendsData" />
        </div>

        <!-- Keyword List -->
        <div class="grid-item keyword-list">
          <KeywordsList :data="keywordsData" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import jwtDecode from 'jwt-decode';
import UsersChart from '../components/administrator/UsersChart.vue';
import PopularTimesChart from '../components/administrator/PopularTimesChart.vue';
import SearchTrendsChart from '../components/administrator/SearchTrendsChart.vue';
import KeywordsList from '../components/administrator/KeywordsList.vue';
import TotalUsers from '../components/administrator/TotalUsers.vue';
import TotalActivities from '../components/administrator/TotalActivities.vue';
import TotalCourses from '../components/administrator/TotalCourses.vue';
import ActiveUsers from '../components/educator/ActiveUsers.vue'

export default {
  name: 'AdminDashboard',
  components: {
    UsersChart,
    PopularTimesChart,
    SearchTrendsChart,
    KeywordsList,
    ActiveUsers,
    TotalActivities,
    TotalCourses,
    TotalUsers
  },
  data() {
    return {
      userName: 'Administrator',

      // Static Data
      usersOverTimeData: [
        { month: 'Jan', users: 120 },
        { month: 'Feb', users: 180 },
        { month: 'Mar', users: 250 },
        { month: 'Apr', users: 320 },
        { month: 'May', users: 280 },
        { month: 'Jun', users: 340 },
      ],

      popularTimesData: [
        { hour: '08:00', visits: 50 },
        { hour: '09:00', visits: 80 },
        { hour: '10:00', visits: 150 },
        { hour: '11:00', visits: 120 },
        { hour: '12:00', visits: 90 },
        { hour: '13:00', visits: 70 },
        { hour: '14:00', visits: 100 },
      ],

      searchTrendsData: [
        { query: 'Algebra', count: 500 },
        { query: 'Physics', count: 450 },
        { query: 'Machine Learning', count: 350 },
        { query: 'AI Basics', count: 320 },
        { query: 'Data Science', count: 290 },
      ],

      keywordsData: [
        { keyword: 'Deep Learning', count: 200 },
        { keyword: 'Statistics', count: 180 },
        { keyword: 'Python', count: 170 },
        { keyword: 'R Programming', count: 140 },
        { keyword: 'Linear Algebra', count: 130 },
      ],
      activeUsers: 120,
      activeUsersChange: -65,
      totalUsers: 1234,
      totalUsersChange: +34,
      totalCourses: 2,
      totalCoursesChange: +1,
      totalActivities: 122,
      totalActivitiesChange: +11,
    };
  },
  created() {
    try {
      const token = localStorage.getItem('token');
      if (token) {
        const decodedToken = jwtDecode(token);
        this.userName = decodedToken.name || 'Administrator';
      }
    } catch (error) {
      console.error('Error decoding token:', error);
      localStorage.removeItem('token'); // Prevent invalid tokens from causing errors
    }
  }
};
</script>

<style scoped>
.admin-container {
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
.users-time{
  grid-column: span 6;
  grid-row: span 1;
}

.popular-times{
  grid-column: span 6;
  grid-row: span 1;
}

.total-users
.total-activities
.total-courses
.active-users {
  grid-column: span 3;
  grid-row: span 1; 
}

.search-trends{
  grid-column: span 6;
  grid-row: span 1;
}

.keyword-list {
  grid-column: span 6;
  grid-row: span 1;
}

.subheader{
  grid-column: span 12;
  grid-row: span 1;
  font-style: oblique;
  font-size: medium;
}

@media (max-width: 768px) {
  .grid-container {
    grid-template-columns: repeat(6, 1fr);
  }

  .grid-item {
    grid-column: span 6;
  }
}
</style>