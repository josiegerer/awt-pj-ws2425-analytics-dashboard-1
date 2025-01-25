<template>
  <div class="admin-container">
    <!-- Dashboard Content -->
    <div class="dashboard">
      <div class="grid-container">

        <p class="subheader">Engagement</p>

        <!-- Active Users last 30 days-->
        <div class="grid-item users-time">
          <ActiveUsersChart />
        </div>

        <!-- Popular Times -->
        <div class="grid-item popular-times">
          <PopularTimesChart />
        </div>

        <p class="subheader">Resource Utilization & Content Popularity</p>

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

        <!-- Search Trends (Full Width in New Row) -->
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
import ActiveUsersChart from '../components/administrator/ActiveUsersChart.vue';
import PopularTimesChart from '../components/administrator/PopularTimesChart.vue';
import SearchTrendsChart from '../components/administrator/SearchTrendsChart.vue';
import KeywordsList from '../components/administrator/KeywordsList.vue';
import TotalUsers from '../components/administrator/TotalUsers.vue';
import TotalActivities from '../components/administrator/TotalActivities.vue';
import TotalCourses from '../components/administrator/TotalCourses.vue';
import ActiveUsers from '../components/educator/ActiveUsers.vue';


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

/* Stats Row (4 Equal Boxes in One Row) */
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-gap: 20px;
  grid-column: span 12; /* Full row width */
}

/* Search Trends (New Row, Full Width) */
.search-trends {
  grid-column: span 12;
}

/* Users Time & Popular Times */
.users-time {
  grid-column: span 6;
}

.popular-times {
  grid-column: span 6;
}

.keyword-list {
  grid-column: span 6;
}

.subheader {
  grid-column: span 12;
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
    grid-template-columns: repeat(2, 1fr); /* Show 2 per row on small screens */
  }

  .search-trends {
    grid-column: span 6;
  }
}
</style>
