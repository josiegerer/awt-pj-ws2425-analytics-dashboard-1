<template>
    <div class="overview-box">
        <h3>Active Users in Course</h3>
        <x>{{ activeUsers }}</x>
        <p :class="userChangeClass">{{ userChangeText }}</p>
    </div>
</template>

<script>
export default {
  data() {
    return {
      activeUsers: 0,  // Default before API call (last day)
      previousActiveUsers: 0,  // Last 30 days
      userChange: 0, 
      adminToken: localStorage.getItem("adminToken") 
    };
  },
  computed: {
    userChangeText() {
      return `${this.userChange >= 0 ? '+' : ''}${this.userChange} Users in the last 30 days`;
    },
    userChangeClass() {
      return {
        'text-green': this.userChange > 0,
        'text-red': this.userChange < 0
      };
    }
  },
  methods: {
    async fetchActiveUsers() {
      try {
        // Fetch Active Users for last day
        const response1 = await fetch("http://localhost:8000/activeUser/1", {
          headers: { Authorization: `Bearer ${this.adminToken}` }
        });

        if (!response1.ok) {
          throw new Error("Failed to fetch activeUser (30 days)");
        }

        const data1 = await response1.json();
        if (data1.activeUser !== undefined) {
          this.activeUsers = data1.activeUser;
        }

        // Fetch Active Users for last 30 days
        const response30 = await fetch("http://localhost:8000/activeUser/30", {
          headers: { Authorization: `Bearer ${this.adminToken}` }
        });

        if (!response30.ok) {
          throw new Error("Failed to fetch activeUser (1 day)");
        }

        const data30 = await response30.json();
        if (data30.activeUser !== undefined) {
          this.previousActiveUsers = data30.activeUser;
        }

        // Calculate change in active users
        this.userChange = this.activeUsers - this.previousActiveUsers;

      } catch (error) {
        console.error("Error fetching activeUser data:", error);
      }
    }
  },
  created() {
    this.fetchActiveUsers(); // Fetch API data when component is created
  }
};
</script>

<style scoped>
h3 {
  text-align: left;
  font-size: 15px;
  color: black;
  margin-bottom: 15px;
}

x {
  text-align: center;
  font-size: 42px;
}

.text-green {
  color: green;
}

.text-red {
  color: red;
}
</style>
