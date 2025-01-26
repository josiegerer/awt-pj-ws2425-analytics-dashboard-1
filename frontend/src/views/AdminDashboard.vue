<template>
  <div class="admin-container">
    <!-- Dashboard Content -->
    <div class="dashboard">
      <div class="grid-container">

        <p class="subheader-1">Engagement</p>

        <p class="subheader-2">Resource Availability & Content Popularity</p>

        <!-- Active Users last days with dropdown-->
        <div class="grid-item users-time">
          <ActiveUsersChart />
        </div>

        <!-- Popular Times -->
        <div class="grid-item popular-times">
          <PopularTimesChart />
        </div>

        <!-- Stats Row (4 Equal Boxes) -->
        <div class="stats-row">
          <div class="grid-item">
            <ActiveUsers />
          </div>

          <div class="grid-item">
            <TotalUsers />
          </div>

          <div class="grid-item">
            <TotalCourses />
          </div>

          <div class="grid-item">
            <TotalActivities />
          </div>
        </div>

        <!-- Search Trends -->
        <div class="grid-item search-trends">
          <SearchTrendsChart />
        </div>

        <!-- Keyword List -->
        <div class="grid-item keyword-list">
          <KeywordsList />
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import ActiveUsersChart from '../components/administrator/ActiveUsersChart.vue';
import PopularTimesChart from '../components/administrator/PopularTimesChart.vue';
import SearchTrendsChart from '../components/administrator/SearchTrendsChart.vue';
import KeywordsList from '../components/administrator/KeywordsList.vue';
import TotalUsers from '../components/administrator/TotalUsers.vue';
import TotalActivities from '../components/administrator/TotalActivities.vue';
import TotalCourses from '../components/administrator/TotalCourses.vue';
import ActiveUsers from '../components/educator/ActiveUsers.vue';

// insert all charts
export default {
  name: 'AdminDashboard',
  components: {
    ActiveUsersChart,
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
      adminToken: localStorage.getItem("adminToken"), // Load admin token
    };
  },
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

/* Stats Row (4 Boxes Stacked) */
.stats-row {
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: repeat(4, auto); 
  grid-column: span 2;
  grid-gap: 10px;
}

.stats-row .grid-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 15px; 
  min-height: 100px; 
  text-align: center;
}

.search-trends {
  grid-column: span 12;
}

.users-time {
  grid-column: span 5;
}

.popular-times {
  grid-column: span 5;
}

.keyword-list {
  grid-column: span 6;
}

.subheader-1{
  grid-column: span 10;
  font-style: oblique;
  font-size: medium;
}
.subheader-2{
  grid-column: span 2;
  font-style: oblique;
  font-size: medium;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .grid-container {
    grid-template-columns: repeat(6, 1fr);
  }

  .grid-item {
    grid-column: span 6;
  }

  .stats-row {
    grid-template-columns: repeat(2, 1fr); 
  }

  .search-trends {
    grid-column: span 6;
  }
}
</style>
