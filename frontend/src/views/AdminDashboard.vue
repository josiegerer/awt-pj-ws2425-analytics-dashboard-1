<template>
  <div class="admin-container">
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
        <!-- Users Chart -->
        <div class="grid-item users-chart">
          <div class="chart-header">
            <h3>Users in the last 30 days</h3>
            <span class="change negative">-5 % this month</span>
          </div>
          <UsersChart :data="usersData" />
        </div>

        <!-- Popular Times -->
        <div class="grid-item popular-times">
          <h3>Popular times</h3>
          <PopularTimesChart :data="popularTimesData" />
        </div>

        <!-- Stats -->
        <div class="grid-item stats">
          <StatCard 
            title="Total Courses" 
            value="103" 
            change="+3"
            changeType="positive" 
          />
          <StatCard 
            title="Total Activities" 
            value="1,185" 
            change="+30"
            changeType="positive" 
          />
          <StatCard 
            title="Total Users" 
            value="1,203" 
            change="-65"
            changeType="negative" 
          />
        </div>

        <!-- Keywords -->
        <div class="grid-item keywords">
          <h3>Top 5 Keywords</h3>
          <KeywordsList :keywords="topKeywords" />
        </div>

        <!-- Search Trends -->
        <div class="grid-item search-trends">
          <h3>Search Trends</h3>
          <SearchTrendsChart :data="searchTrendsData" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import jwtDecode from 'jwt-decode';
import UsersChart from '../components/admin/UsersChart.vue';
import PopularTimesChart from '../components/admin/PopularTimesChart.vue';
import StatCard from '../components/admin/StatCard.vue';
import KeywordsList from '../components/admin/KeywordsList.vue';
import SearchTrendsChart from '../components/admin/SearchTrendsChart.vue';

export default {
  name: 'AdminDashboard',
  components: {
    UsersChart,
    PopularTimesChart,
    StatCard,
    KeywordsList,
    SearchTrendsChart
  },
  data() {
    return {
      userName: 'Admin',
      usersData: [
        { date: '2023-11-05', users: 280 },
        { date: '2023-11-15', users: 260 },
        { date: '2023-11-25', users: 250 },
        { date: '2023-12-05', users: 231 },
      ],
      popularTimesData: [
        { hour: '3', users: 50 },
        { hour: '6', users: 100 },
        { hour: '9', users: 200 },
        { hour: '12', users: 400 },
        { hour: '15', users: 350 },
        { hour: '18', users: 300 },
        { hour: '21', users: 150 },
        { hour: '24', users: 75 },
      ],
      topKeywords: [
        { name: 'Kompetenzen', count: 154, change: '+20' },
        { name: 'Grundlagen', count: 130, change: '+30' },
        { name: 'Gefahren', count: 115, change: '+25' },
        { name: 'Pflege', count: 80, change: '+5' },
        { name: 'Klettern', count: 74, change: '+5' },
      ],
      searchTrendsData: [
        { date: '5.11.', searches: 80 },
        { date: '12.11.', searches: 70 },
        { date: '19.11.', searches: 60 },
        { date: '26.11.', searches: 85 },
        { date: '3.12.', searches: 120 },
        { date: '10.12.', searches: 90 },
      ]
    }
  },
  created() {
    const token = localStorage.getItem('token');
    if (token) {
      const decodedToken = jwtDecode(token);
      this.userName = decodedToken.name;
    }
  }
}
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

.users-chart {
  grid-column: span 6;
  grid-row: span 2;
}

.popular-times {
  grid-column: span 6;
  grid-row: span 2;
}

.stats {
  grid-column: span 12;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.keywords {
  grid-column: span 6;
}

.search-trends {
  grid-column: span 6;
}

.dashboard-header {
  padding: 20px;
  background: white;
  border-bottom: 1px solid #eee;
}

.logo-greeting {
  display: flex;
  align-items: center;
  gap: 20px;
}

.change.positive {
  color: #22bb33;
}

.change.negative {
  color: #cc0000;
}

@media (max-width: 768px) {
  .grid-container {
    grid-template-columns: repeat(6, 1fr);
  }

  .users-chart,
  .popular-times,
  .keywords,
  .search-trends {
    grid-column: span 6;
  }

  .stats {
    grid-template-columns: 1fr;
  }
}
</style>