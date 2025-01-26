<template>
  <div class="activity-revisits-container">
    <h3>Activity Revisits</h3>
    <div class="activity-revisits-content">
      <ol class="activity-list">
        <li v-for="(item, index) in visibleData" :key="item.course" class="activity-item">
          <div class="activity-info">
            <span>{{ index + 1 }}. {{ item.course }}</span>
            <div class="activity-subtitle">{{ item.change }}</div>
          </div>
          <div class="activity-count">{{ item.count }}x</div>
        </li>
      </ol>
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
      activities: [], // Store fetched data here
      showAll: false,
    };
  },
  computed: {
    visibleData() {
      return this.showAll ? this.activities : this.activities.slice(0, 3);
    },
  },
  methods: {
    async fetchActivityRevisits() {
      try {
        const response = await fetch("http://localhost:8000/activityRevisits");
        if (!response.ok) {
          throw new Error(`Failed to fetch data: ${response.status}`);
        }
        const data = await response.json();

        console.log("Fetched Data:", data); 

        // Transform API data to match expected structure
        this.activities = data.activitiesVisits.map((activity) => ({
          course: this.extractCourseName(activity.activityId), // Extract name from URL
          count: activity.visits,
          change: "+X in the last 30 days" // Placeholder for real change calculation
        }));
      } catch (error) {
        console.error("Error fetching activity revisits:", error);
      }
    },
    extractCourseName(activityId) {
      // Extracts readable course name from activityId URL
      return decodeURIComponent(activityId.split("/").pop(                                          ).replace(/_/g, " "));
    },
    toggleView() {
      this.showAll = !this.showAll;
    },
  },
  mounted() {
    this.fetchActivityRevisits(); // Fetch data when the component loads
  }
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

.activity-subtitle {
  font-size: 12px;
  color: green;
  font-family: Roboto, ui-sans-serif, system-ui, sans-serif;
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
