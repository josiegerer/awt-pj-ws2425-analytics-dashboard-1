<template>
  <div class="streak-container">
    <h3>Daily Streak</h3>
    <p>
      <span v-if="streak === 0">
        You don't have a streak. Your last streak was {{ daysSinceLastStreak }} days ago.
      </span>
      <span v-else-if="streak === 1">
        You were last active on one day, but your streak hasn't continued yet!
      </span>
      <span v-else>
        You have been active for 
        <span class="streak">{{ streak }}</span> 
        {{ streak === 1 ? 'day' : 'days' }} in a row!
      </span>
    </p>
    <div class="streak-visual">
      <div 
        v-for="(day, index) in daysOfWeek" 
        :key="index" 
        class="streak-day" 
        :class="{ active: activeDays.includes(day) }">
        <span class="day-label">{{ day }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DailyStreak',
  data() {
    return {
      streak: 0, // Current streak from the API
      lastActiveDate: null, // Last date the user was active
      daysSinceLastStreak: 0, // Days since last streak
      activeDays: [], // Days in the current week where the user was active
      daysOfWeek: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], // Days of the week
    };
  },
  methods: {
    getCookie(name) {
      const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
      return match ? match[2] : null;
    },
    calculateDaysSinceLastStreak(lastDate) {
      const today = new Date();
      const lastActive = new Date(lastDate);
      const differenceInTime = today - lastActive;
      return Math.floor(differenceInTime / (1000 * 60 * 60 * 24));
    },
    async fetchDailyStreak() {
      const token = this.getCookie("auth_token");

      if (!token) {
        console.error("No authentication token found.");
        return;
      }

      try {
        const response = await fetch("http://localhost:8000/dailyStreak", {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Daily Streak Data:", data);

        const today = new Date().toISOString().split("T")[0]; // Get current date in YYYY-MM-DD format
        if (data.lastDate === today) {
          this.streak = data.lastStreak;
          this.daysSinceLastStreak = 0; // Reset since user was active today
        } else {
          this.streak = 0; // Streak resets if not active today
          this.daysSinceLastStreak = this.calculateDaysSinceLastStreak(data.lastDate);
        }

        this.lastActiveDate = data.lastDate;
        this.fetchActiveDays();
      } catch (error) {
        console.error("Error fetching daily streak data:", error);
      }
    },
    async fetchActiveDays() {
      const token = this.getCookie("auth_token");

      if (!token) {
        console.error("No authentication token found.");
        return;
      }

      try {
        const response = await fetch("http://localhost:8000/activeHoursThisWeek", {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Active Hours Data:", data);

        // Extract active days from the response
        const activeDays = [];
        data.activeHours.forEach((dayData, index) => {
          if (dayData.hours.some(hour => hour.timeSpent > 0)) {
            activeDays.push(this.daysOfWeek[index]);
          }
        });

        this.activeDays = activeDays;
      } catch (error) {
        console.error("Error fetching active hours data:", error);
      }
    },
  },
  mounted() {
    this.fetchDailyStreak();
  },
};
</script>

<style scoped>
.streak {
  font-weight: bold;
  color: #49cb40;
}

.streak-visual {
  display: flex;
  justify-content: center;
  margin-top: 30px;
  gap: 10px; /* Space between the bubbles */
}

.streak-day {
  width: 50px; /* Set a base width */
  aspect-ratio: 1 / 1; /* Maintain a 1:1 aspect ratio */
  background: #e0e0e0; /* Default background for inactive days */
  border-radius: 50%; /* Circle shape */
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 12px;
  font-weight: bold;
  color: #333;
  position: relative;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.streak-day.active {
  background: #49cb40; /* Highlight active days */
  color: white;
}

.day-label {
  text-align: center;
  display: block;
}

h3 {
  text-align: left; /* Align title to the left */
  font-size: 15px;
  color: black;
}
</style>
