<template>
  <div class="educator-rating-container">
    <h3>Educator Rating Overview</h3>
    <p>Average Ratings per Activity</p>
    <div v-if="loaded">
      <div class="rating-list">
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
    </div>
    <p v-else>Loading...</p>
  </div>
</template>

<script>
export default {
  name: "EducatorRating",
  data() {
    return {
      ratings: [], 
      loaded: false, 
    };
  },
  methods: {
    async fetchEducatorRatings() {
      try {
        console.log("Fetching educator rating data...");

       
        const token = localStorage.getItem("token");
        if (!token) {
          console.error("No authentication token found.");
          return;
        }

        const response = await fetch("http://localhost:8000/activityRatings/instructor", {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
          }
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch data: ${response.status}`);
        }

        const data = await response.json();
        console.log("Fetched educator rating data:", data);

        const activities = data.activitiesRatings;

        this.ratings = activities.map((activity) => {
          const rating = parseFloat(activity.meanRating.toFixed(1)); 
          return {
            name: this.extractCourseName(activity.activityId),
            rating: rating,
            fullStars: Math.floor(rating), // Full stars
            emptyStars: 5 - Math.floor(rating) // Empty stars
          };
        });

        this.loaded = true;
      } catch (error) {
        console.error("Error fetching educator rating data:", error);
      }
    },
    extractCourseName(activityId) {
      return decodeURIComponent(activityId.split("/").pop().replace(/_/g, " "));
    }
  },
  mounted() {
    this.fetchEducatorRatings();
  }
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

p {
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
  text-align: left;
}

.stars {
  display: flex;
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
  font-weight: bold;
}
</style>
