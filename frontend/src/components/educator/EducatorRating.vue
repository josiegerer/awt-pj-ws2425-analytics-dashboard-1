<template>
  <div class="last-rating-container">
    <h3>Your Last Rating</h3>
    <div class="stars">
      <span v-for="star in fullStars" :key="star" class="star full">&#9733;</span>
      <span v-for="star in emptyStars" :key="star" class="star empty">&#9734;</span>
    </div>
    <p>{{ rating }} out of 5</p>
    <div class="rating-content">
      <p><strong>Activity:</strong> {{ lastRating.activity }}</p>
      <p><strong>Date:</strong> {{ lastRating.date }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "LastRating",
  props: {
    rating: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      lastRating: {
        activity: "Course 3: Bäume ausdünnen",
        date: "2023-12-01"
      }
    };
  },
  computed: {
    fullStars() {
      return Math.floor(this.rating);
    },
    emptyStars() {
      return 5 - Math.floor(this.rating);
    },
  },
};
</script>

<style scoped>
h3 {
  text-align: left; /* Align title to the left */
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