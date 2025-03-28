<template>
  <div class="educator-rating-container">
    <h3>Rating Overview - Average per Activity</h3>
    <div v-if="loaded">
      <div v-if="ratings.length > 0" class="rating-list">
        <!-- Loop through ratings to display each activity's rating -->
        <div v-for="(activity, index) in ratings" :key="index" class="rating-item">
          <div class="activity-info">
            <p><strong>{{ activity.name }}</strong></p>
          </div>
          <div class="stars">
            <span v-for="star in activity.fullStars" :key="star" class="star full">&#9733;</span>
            <span v-for="star in activity.emptyStars" :key="star" class="star empty">&#9734;</span>
          </div>
          <p class="rating-text">{{ activity.rating.toFixed(1) }} / 5</p>
        </div>
      </div>
      <p v-else class="empty-message">No ratings available.</p>
    </div>
    <p v-else class="loading-message">Loading...</p>
  </div>
</template>

<script>
export default {
  name: "EducatorRating",
  data() {
    return {
      ratings: [], // Store fetched ratings data here
      loaded: false, // Control whether data has been loaded
    };
  },
  methods: {
    // Function to get a cookie value by name
    getCookie(name) {
      const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
      return match ? match[2] : null;
    },

    // Function to fetch educator ratings data from the server
    async fetchEducatorRatings() {
      // Get the authentication token from cookie
      const token = this.getCookie("auth_token");

      if (!token) {
        console.error("No authentication token found.");
        return;
      }

      try {
        // Fetch data from the server
        const response = await fetch("http://localhost:8000/activityRatings/instructor", {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Fetched educator rating data:", data);

        const activities = data.activitiesRatings || [];

        // Process and transform the fetched data
        this.ratings = activities.map((activity) => {
          const rating = parseFloat(activity.meanRating.toFixed(1)); 
          return {
            name: this.extractCourseName(activity.activityId),
            rating: rating,
            fullStars: Math.floor(rating), // Full stars
            emptyStars: 5 - Math.floor(rating), // Empty stars
          };
        });

        this.loaded = true;
      } catch (error) {
        console.error("Error fetching educator rating data:", error);
        this.loaded = true; 
      }
    },

    // Function to extract readable course name from activityId URL
    extractCourseName(activityId) {
      return decodeURIComponent(activityId.split("/").pop().replace(/_/g, " "));
    },
  },
  // Fetch educator ratings data when the component is mounted
  mounted() {
    this.fetchEducatorRatings(); 
  },
};
</script>

<style scoped>
.educator-rating-container {
  height: 100%;
  text-align: center;
}

h3 {
  text-align: left;
  font-size: 15px;
  color: black;
  margin-bottom: 5px;
}

p .subheader{
  text-align: left;
  font-size: 12px;
  color: grey;
  margin-bottom: 15px;
}

.rating-list {
  margin-top: 10px;
}

.rating-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
}

.activity-info {
  flex: 1;
  display: flex;
  align-items: center;
  text-align: left;
}

.stars {
  display: flex;
  min-width: 100px; /* Consistent width */
  justify-content: flex-start;
}

.star {
  font-size: 20px;
  color: gold;
  margin-right: 3px;
}

.star.empty {
  color: lightgray;
}

.rating-text {
  font-size: 14px;
  display: flex;
  align-items: center;
  text-align: left;
  min-width: 60px; /* Ensure consistent placement */
}

.loading-message,
.empty-message {
  text-align: center;
  font-size: 14px;
  color: #888;
  margin-top: 20px;
}
</style>
