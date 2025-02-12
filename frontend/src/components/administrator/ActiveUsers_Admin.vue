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
      activeUsers: 0,
      previousActiveUsers: 0,
      userChange: 0
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
    getCookie(name) {
      const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
      return match ? match[2] : null;
    },
    async fetchActiveUsers() {
      const token = this.getCookie("auth_token");
      if (!token) {
        console.error("No authentication token found.");
        return;
      }

      try {
        const response1 = await fetch("http://localhost:8000/activeUser/1", {
          headers: { Authorization: `Bearer ${token}` }
        });

        if (!response1.ok) {
          throw new Error("Failed to fetch activeUser (1 days)");
        }

        const data1 = await response1.json();
        if (data1.activeUser !== undefined) {
          this.activeUsers = data1.activeUser;
        }

        const response30 = await fetch("http://localhost:8000/activeUser/30", {
          headers: { Authorization: `Bearer ${token}` }
        });

        if (!response30.ok) {
          throw new Error("Failed to fetch activeUser (30 day)");
        }

        const data30 = await response30.json();
        if (data30.activeUser !== undefined) {
          this.previousActiveUsers = data30.activeUser;
        }

        this.userChange = this.activeUsers - this.previousActiveUsers;

      } catch (error) {
        console.error("Error fetching activeUser data:", error);
      }
    }
  },
  created() {
    this.fetchActiveUsers();
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
  font-size: 30px;
}

.text-green {
  color: green;
  font-size: 15px;
}

.text-red {
  color: red;
  font-size: 15px;
}
</style>
