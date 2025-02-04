<template>
  <div class="revisits-list">
    <h3>Top Revisits</h3>
    <div class="revisit-item" v-for="(item, index) in visibleData" :key="index">
      <div class="revisit-main">
        <span class="revisit-number">{{ index + 1 }}. </span>
        <span class="revisit-name">{{ item.course }}</span>
        <span class="revisit-count">{{ item.count }}x</span>
      </div>
    </div>
    <button @click="toggleView" class="view-more-button">
      {{ showAll ? 'View Less' : 'View All' }}
    </button>
  </div>
</template>

<script>
export default {
  name: "ActivityRevisits",
  data() {
    return {
      activities: [],
      showAll: false,
    };
  },
  computed: {
    visibleData() {
      return this.showAll ? this.activities : this.activities.slice(0, 5);
    },
  },
  methods: {
    getCookie(name) {
      const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
      return match ? match[2] : null;
    },

    async fetchActivityRevisits() {
        const token = this.getCookie("auth_token");

        if (!token) {
          console.error("No authentication token found.");
          return;
        }

        try {
          const response = await fetch("http://localhost:8000/activityRatings/instructor", {
            headers: { Authorization: `Bearer ${token}` },
          });

          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }

          const data = await response.json();
          console.log("Fetched educator rating data:", data); // Debugging line

          // Ensure data.activitiesVisits exists before mapping
          this.activities = data.activitiesVisits?.map((activity) => ({
            course: this.extractCourseName(activity.activityId),
            count: activity.visits,
          })) || []; // Fallback to empty array if undefined
        } catch (error) {
          console.error("Error fetching activity revisits:", error);
        }
      },

    extractCourseName(activityId) {
      return decodeURIComponent(activityId.split("/").pop().replace(/_/g, " "));
    },
    toggleView() {
      this.showAll = !this.showAll;
    },
  },
  mounted() {
    this.fetchActivityRevisits();
  },
};
</script>

<style scoped>
.revisits-list {
  padding: 10px 0;
  width: 100%;
}

.revisit-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.revisit-main {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-grow: 1;
}

.revisit-number {
  font-weight: 500;
}

.revisit-name {
  font-weight: 500;
  flex-grow: 1;
  text-align: left;
}

.revisit-count {
  color: #666;
  text-align: right;
  min-width: 40px;
}

.view-more-button {
  margin-top: 10px;
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  background-color: grey;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 14px;
}

.view-more-button:hover {
  background-color: darkgrey;
}
</style>