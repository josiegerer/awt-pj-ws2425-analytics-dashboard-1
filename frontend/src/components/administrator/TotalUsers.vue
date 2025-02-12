<template>
    <div class="overview-box">
        <h3>Total Users</h3>
        <x>{{ totalUsers }}</x>
    </div>
</template>

<script>
export default {
  data() {
    return {
      totalUsers: 0  // Default before API call
    };
  },
  methods: {
    getCookie(name) {
      const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
      return match ? match[2] : null;
    },
    async fetchTotalUsers() {
      const token = this.getCookie("auth_token");
      if (!token) {
        console.error("No authentication token found.");
        return;
      }

      try {
        const response = await fetch("http://localhost:8000/totalUsers", {
          headers: { Authorization: `Bearer ${token}` }
        });

        if (!response.ok) {
          throw new Error("Failed to fetch totalUsers");
        }

        const data = await response.json();
        if (data.totalUsers !== undefined) {
          this.totalUsers = data.totalUsers;
        }
      } catch (error) {
        console.error("Error fetching totalUsers:", error);
      }
    }
  },
  created() {
    this.fetchTotalUsers(); // Fetch API data when component is created
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
