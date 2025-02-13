<template>
  <!-- Card Chart with number of total courses-->
    <div class="overview-box">
        <h3>Total Courses</h3>
        <x>{{ totalCourses }}</x>
    </div>
</template>

<script>
export default {
  data() {
    return {
      totalCourses: 0  // Default before API call
    };
  },
  methods: {
    // get cookie
    getCookie(name) {
      const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
      return match ? match[2] : null;
    },
    async fetchTotalCourses() {
      // Get the authentication token from cookie
      const token = this.getCookie("auth_token");
      if (!token) {
        console.error("No authentication token found.");
        return;
      }

      try {
         // fetch data from url endpoint
        const response = await fetch("http://localhost:8000/totalCourses", {
          headers: { Authorization: `Bearer ${token}` }
        });

        if (!response.ok) {
          throw new Error("Failed to fetch totalCourses");
        }

        // get number of total courses
        const data = await response.json();
        if (data.totalCourses && Array.isArray(data.totalCourses)) {
          this.totalCourses = data.totalCourses.length;
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
