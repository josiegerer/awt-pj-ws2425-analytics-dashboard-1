<template>
  <!-- Card Chart with number of total activities-->
  <div class="overview-box">
      <h3>Total Activities</h3>
      <x>{{ totalActivities }}</x>
  </div>
</template>

<script>
export default {
data() {
  return {
    totalActivities: 0  // Default before API call
  };
},
methods: {
  // get cookie
  getCookie(name) {
      const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
      return match ? match[2] : null;
    },
  async fetchTotalActivities() {
    try {
      // Get the authentication token from cookie
        const auth_Token = this.getCookie("auth_token");

        if (!auth_Token) {
          console.error("No authentication token found.");
          return;
        }
         // fetch data from url endpoint
        const response = await fetch("http://localhost:8000/totalActivities", {
          headers: {
            Authorization: `Bearer ${auth_Token}`,
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("API Response:", data);
        
        // get number of total activities
        if (data.activities && Array.isArray(data.activities)) {
        this.totalActivities = data.activities.length; 
      }
      } catch (error) {
        console.error("Error fetching totalCourses:", error);
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
