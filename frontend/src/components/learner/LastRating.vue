<template>
  <div class="last-rating-container">
    <h3>Your Last Rating</h3>
    <div v-if="lastRating">
      <div class="stars">
        <span v-for="star in fullStars" :key="star" class="star full">&#9733;</span>
        <span v-for="star in emptyStars" :key="star" class="star empty">&#9734;</span>
      </div>
      <p>{{ lastRating.score }} out of 5</p>
      <div class="rating-content">
        <p><strong>Activity:</strong> {{ getActivityName(lastRating.activity) }}</p>
        <p><strong>Date:</strong> {{ formatDate(lastRating.timestamp) }}</p>
      </div>
    </div>
    <div v-else>
      <p>No ratings available.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "LastRating",
  data() {
    return {
      lastRating: null, // Holds the most recent rating
    };
  },
  computed: {
    fullStars() {
      return this.lastRating ? Math.floor(this.lastRating.score) : 0;
    },
    emptyStars() {
      return this.lastRating ? 5 - Math.floor(this.lastRating.score) : 5;
    },
  },
  methods: {
    getCookie(name) {
      const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
      return match ? match[2] : null;
    },
    async fetchLastRatings() {
      const token = this.getCookie("auth_token");

      if (!token) {
        console.error("No authentication token found.");
        return;
      }

      try {
        const response = await fetch("http://localhost:8000/activityRatings/learner", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        const ratings = data.lastRatings;

        // Find the most recent rating
        let mostRecentRating = null;
        for (const activity in ratings) {
          const rating = ratings[activity];
          if (!mostRecentRating || new Date(rating.timestamp) > new Date(mostRecentRating.timestamp)) {
            mostRecentRating = {
              activity: activity,
              score: rating.score,
              timestamp: rating.timestamp,
            };
          }
        }

        this.lastRating = mostRecentRating;
      } catch (error) {
        console.error("Error fetching last ratings:", error);
      }
    },
    getActivityName(activityId) {
      // Extract the activity name from the URL
      return activityId.split('/').pop().replace(/_/g, ' ');
    },
    formatDate(timestamp) {
      // Format the timestamp to a readable date
      const date = new Date(timestamp);
      return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    },
  },
  mounted() {
    this.fetchLastRatings();
  },
};
</script>

<style scoped>
h3 {
  text-align: left;
  font-size: 15px;
  color: black;
}

.rating-content {
  margin-top: 10px;
}

.rating-content p {
  margin: 5px 0;
}

.last-rating-container {
  text-align: center;
}

.stars {
  display: flex;
  justify-content: center;
  margin: 10px 0;
}

.star {
  font-size: 24px;
  color: gold;
}

.star.empty {
  color: lightgray;
}
</style>
