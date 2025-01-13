  <template>
  <div class="streak-container">
    <h3>Daily Streak</h3>
    <p>
      You have been active for 
      <span class="streak">{{ streak }}</span> 
      {{ streak === 1 ? 'day' : 'days' }} in a row!
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
  props: {
    streak: {
      type: Number,
      required: true,
    },
    activeDays: {
      type: Array,
      required: true,
      default: () => ['Mon', 'Tue'], // Example active days
    },
  },
  computed: {
    daysOfWeek() {
      return ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    },
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
  margin-top: 10px;
  gap: 10px; /* Space between the bubbles */
}

.streak-day {
  width: 40px; /* Set a base width */
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

