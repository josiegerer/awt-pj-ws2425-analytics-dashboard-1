<template>
  <!-- Container for the activity revisits list -->
  <div class="activity-revisits-container">
    <h3>Activity Revisits</h3>
    <div class="activity-revisits-content">
      <ol class="activity-list">
        <!-- Loop through visibleData to display each activity -->
        <li v-for="item in visibleData" :key="item.activityId" class="activity-item">
          <div class="activity-info">
            <span>{{ item.course }}</span>
          </div>
          <div class="activity-count">{{ item.count }}x</div>
        </li>
      </ol>
    </div>
    <!-- Button to toggle between showing all activities or just a few -->
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
      activities: [], // Store fetched data here
      showAll: false, // Control whether to show all activities or just a few
    };
  },
  computed: {
    // Compute the visible data based on showAll flag
    visibleData() {
      return this.showAll ? this.activities : this.activities.slice(0, 3);
    },
  },
  methods: {
    // Function to get a cookie value by name
    getCookie(name) {
      const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
      return match ? match[2] : null;
    },
    // Function to fetch activity revisits data from the server
    async fetchActivityRevisits() {
      const token = this.getCookie("auth_token");
      if (!token) {
        console.error("No authentication token found.");
        return;
      }
      try {
        const response = await fetch("http://localhost:8000/activityRevists/learner", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (!response.ok) {
          throw new Error(`Failed to fetch data: ${response.status}`);
        }
        const data = await response.json();
        console.log("Fetched Data:", data);

        // Transform API data to match expected structure and sort by count in descending order
        this.activities = (data.activitiesVisits || [])
          .map((activity) => ({
            course: this.extractCourseName(activity.activityId), // Extract name from URL
            count: activity.visits,
            activityId: activity.activityId, // Keep activityId for uniqueness
          }))
          .sort((a, b) => b.count - a.count); // Sort by count in descending order
      } catch (error) {
        console.error("Error fetching activity revisits:", error);
      }
    },
    // Function to extract readable course name from activityId URL
    extractCourseName(activityId) {
      return decodeURIComponent(activityId.split("/").pop().replace(/_/g, " "));
    },
    // Function to toggle between showing all activities or just a few
    toggleView() {
      this.showAll = !this.showAll;
    },
  },
  // Fetch activity revisits data when the component is mounted
  mounted() {
    this.fetchActivityRevisits();
  },
};
</script>

<style scoped>
h3 {
  text-align: left;
  font-size: 15px;
  color: black;
}

.activity-revisits-content {
  margin-top: 20px;
}

.activity-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.activity-info {
  display: flex;
  flex-direction: column;
}

.activity-list {
  list-style-type: decimal;
  font-family: Inter, ui-sans-serif, system-ui, sans-serif;
  font-weight: 600;
  color: black;
}

.activity-count {
  font-size: 20px;
  font-family: Inter, ui-sans-serif, system-ui, sans-serif;
  font-weight: 600;
  color: black;
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