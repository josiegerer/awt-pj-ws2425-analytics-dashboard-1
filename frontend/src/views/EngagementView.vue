<template>
  <div class="dashboard">
    <div class="grid-container">
      <!-- First Row -->
      <!-- Active Hours -->
      <div class="grid-item active-hours">
        <HeatmapChart />
      </div>

      <!-- Activity Engagement -->
      <div class="grid-item activity-engagement">
        <ActivityEngagement :data="activityEngagementData" />
      </div>

      <!-- Daily Streak -->
      <div class="grid-item daily-streak">
        <DailyStreak :streak="dailyStreak" />
      </div>

      <!-- Activity Revisits-->
      <div class="grid-item activity-revisits">
        <ActivityRevisits :data="activityRevisitsData" />
      </div>

      <!-- Second Row -->
      <!-- Time Spent -->
      <div class="grid-item time-spent">
        <TimeSpent :data="timeSpentData" />
      </div>

      <!-- Last Rating -->
      <div class="grid-item last-rating">
        <LastRating :rating="lastRatingData" />
      </div>
    </div>
  </div>
</template>

<script>
import HeatmapChart from '../components/ActiveHours.vue';
import ActivityEngagement from '../components/ActivityEngagement.vue';
import ActivityRevisits from '../components/ActivityRevisits.vue';
import TimeSpent from '../components/TimeSpent.vue';
import LastRating from '../components/LastRating.vue';
import DailyStreak from '../components/DailyStreak.vue';

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
      activityEngagementData: [],
      activityRevisitsData: [
        { course: "Course 1", count: 15, change: "+10 in the last 30 days" },
        { course: "Course 2", count: 13, change: "+13 in the last 30 days" },
        { course: "Course 3", count: 8, change: "+1 in the last 30 days" },
        { course: "Course 4", count: 20, change: "+5 in the last 30 days" },
        { course: "Course 5", count: 10, change: "+2 in the last 30 days" },
        { course: "Course 6", count: 18, change: "+7 in the last 30 days" },
      ],
      timeSpentData: [
        { activity: "Activity 1", current: 120, previous: 100 },
        { activity: "Activity 2", current: 90, previous: 80 },
      ],
      lastRatingData: 3,
      dailyStreak: 3,
    };
  },
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
  background-color: #f8f9fa;
}

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
.active-hours {
  grid-column: span 5;
  grid-row: span 2; 
}

.activity-engagement {
  grid-column: span 4; 
  grid-row: span 2; 
  overflow: auto; /* Add scrolling if content is too large */
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
  height: span 1;
}

/* Responsive Design */
@media (max-width: 768px) {
  .grid-container {
    grid-template-columns: repeat(6, 1fr);
  }

  .active-hours,
  .activity-engagement,
  .activity-revisits,
  .last-rating,
  .time-spent,
  .daily-streak {
    grid-column: span 6; 
  }
}
</style>
