<template>
    <div class="overview-box">
        <h3>Total Courses</h3>
        <x>{{ totalCourses }}</x>
    </div>
</template>

<script>
export default {
  data() {
    return {
      totalCourses: 0,  // Default before API call
      adminToken: localStorage.getItem("adminToken") // Load token from local storage
    };
  },
  methods: {
    async fetchTotalCourses() {
      try {
        const response = await fetch("http://localhost:8000/totalCourses", {
          headers: { Authorization: `Bearer ${this.adminToken}` }
        });

        if (!response.ok) {
          throw new Error("Failed to fetch totalCourses");
        }

        const data = await response.json();
        
        if (data.totalCourses && Array.isArray(data.totalCourses)) {
          this.totalCourses = data.totalCourses.length; // Count total courses
        }
      } catch (error) {
        console.error("Error fetching totalCourses:", error);
      }
    }
  },
  created() {
    this.fetchTotalCourses(); // Fetch API data when component is created
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
