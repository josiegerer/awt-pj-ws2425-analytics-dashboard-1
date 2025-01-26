<template>
  <div class="overview-box">
      <h3>Total Activities</h3>
      <x>{{ totalActivities }}</x>
  </div>
</template>

<script>
export default {
data() {
  return {
    totalActivities: 0,  // Default before API call
    adminToken: localStorage.getItem("adminToken") // Load token from local storage
  };
},
methods: {
  async fetchTotalActivities() {
    try {
      const response = await fetch("http://localhost:8000/totalActivities", {
        headers: { Authorization: `Bearer ${this.adminToken}` }
      });

      if (!response.ok) {
        throw new Error("Failed to fetch totalActivities");
      }

      const data = await response.json();
      
      if (data.activities && Array.isArray(data.activities)) {
        this.totalActivities = data.activities.length; // Count total activities
      }
    } catch (error) {
      console.error("Error fetching totalActivities:", error);
    }
  }
},
created() {
  this.fetchTotalActivities(); // Fetch API data when component is created
}
};
</script>

<style scoped>
h3 {
text-align: left;
font-size: 15px;
color: black;
margin-bottom: 5px;
}

x {
text-align: center;
font-size: 30px;
}

.text-green {
color: green;
}

.text-red {
color: red;
}
</style>
