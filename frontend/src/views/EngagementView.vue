<template>
  <div class="engagement-container">
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

        <!-- Activity Hours -->
        <div class="grid-item active-hours">
          <HeatmapChart />
        </div>

        <!-- Activity Engagement -->
        <div class="grid-item activity-engagement">
          <ActivityEngagement />
        </div>

        <!-- Daily Streak -->
        <div class="grid-item daily-streak">
          <DailyStreak />
        </div>

        <!-- Activity Revisits -->
        <div class="grid-item activity-revisits">
          <ActivityRevisits />
        </div>

        <!-- Time Spent -->
        <div class="grid-item time-spent">
          <TimeSpent @button-click="handleTimeSpentClick" />
        </div>

         <!-- Last Rating -->
        <div class="grid-item last-rating">
          <LastRating />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import HeatmapChart from '../components/learner/ActiveHours.vue';
import ActivityEngagement from '../components/learner/ActivityEngagement.vue';
import ActivityRevisits from '../components/educator/ActivityRevisits.vue';
import TimeSpent from '../components/learner/TimeSpent.vue';
import LastRating from '../components/learner/LastRating.vue';
import DailyStreak from '../components/learner/DailyStreak.vue';

// insert all charts
export default {
  name: 'EngagementView',
  components: {
    HeatmapChart,
    ActivityEngagement,
    ActivityRevisits,
    TimeSpent,
    LastRating,
    DailyStreak,
  },
  data() {
    return {
      showHeader: true, 
    }
  },
  methods: {
    navigateTo(route) {
      this.$router.push(route);
    },
    handleTimeSpentClick() {
      console.log('Time Spent button clicked');
    }
  }
};
</script>

<style scoped>
/* Container */
.engagement-container {
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
  grid-template-rows: repeat(12, auto);
  grid-template-columns: repeat(12, 1fr);
  grid-gap: 20px;
}

.grid-item {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Layout Definition */
.active-hours {
  grid-column: span 5;
  grid-row: span 2; 
}

.activity-engagement {
  grid-column: span 4; 
  grid-row: span 2; 
  overflow: auto;
  min-height: 300px; 
}

.activity-revisits {
  grid-column: span 3;
  grid-row: span 1; 
}

.last-rating {
  grid-column: span 3; 
  grid-row: span 1; 
}

.time-spent {
  grid-column: span 9; 
  grid-row: span 2;
}

.daily-streak {
  grid-column: span 3; 
  grid-row: span 1;
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
