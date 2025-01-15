<template>
<div class="app-container">
  <!-- Conditional Header -->
  <header class="dashboard-header">
    <div class="logo-greeting">
      <div class="logo">
        <img src="@/assets/lms-Logo.png" alt="LMS Logo" />
      </div>
      <div class="greeting">
        <h1>Welcome, {{ userName }}</h1>
        <p v-if="showHeader">Glad to see you again, ready for another session?</p>
        <p v-else>Great to have you back, ready to inspire and guide the next generation?</p>
      </div>
    </div>
    <nav v-if="showHeader" class="nav-buttons">
      <button @click="navigateTo('/overall')">Overall</button>
      <button @click="navigateTo('/performance')">Performance</button>
      <button @click="navigateTo('/engagement')">Engagement</button>
    </nav>
  </header>

  <!-- Dynamic Content -->
  <main class="main-content">
    <router-view />
  </main>
</div>
</template>

<script>
import jwtDecode from 'jwt-decode';

export default {
name: 'App',
data() {
  return {
    userName: 'User', // Default name
    role: '', // User role
  };
},
computed: {
  showHeader() {
    return this.$route.path !== '/educator-dashboard';
  }
},
methods: {
  navigateTo(route) {
    this.$router.push(route);
  },
  fetchUserName() {
    const token = localStorage.getItem('token'); // Fetch the token from local storage
    if (token) {
      const decodedToken = jwtDecode(token); // Decode the token
      this.userName = decodedToken.name;
      this.role = decodedToken.role; // Extract the user role from the token
      this.redirectBasedOnRole();
    } else {
      console.error('No token found');
    }
  },
  redirectBasedOnRole() {
    if (this.role === 'learner') {
      this.$router.push('/overall');
    } else if (this.role === 'admin') {
      this.$router.push('/admin-dashboard');
    } else if (this.role === 'educator') {
      this.$router.push('/educator-dashboard');
    }
  },
},
created() {
  this.fetchUserName();
},
};
</script>

<style>
/* Reset */
* {
margin: 0;
padding: 0;
box-sizing: border-box;
}

/* Font Family */
body {
font-family: 'Inter', sans-serif;
}

/* App Container */
.app-container {
display: flex;
flex-direction: column;
height: 100vh;
width: 100%;
overflow: hidden;
}

/* Header Styling */
.dashboard-header {
display: flex;
justify-content: space-between;
align-items: center;
background-color: #c40d1e; /* Red Background - TU Color */
height: 100px; /* Fixed height */
padding: 0 20px;
color: white;
}

.logo-greeting {
display: flex;
align-items: center;
}

.greeting {
text-align: left;
margin-left: 10px; /* Minimal space between logo and greeting */
}

.greeting h1 {
margin: 0;
font-size: 24px;
}

.greeting p {
margin: 0;
font-size: 14px;
}

/* Navigation Buttons */
.nav-buttons {
display: flex;
gap: 20px;
margin-left: auto; /* Align buttons to the right */
}

/* Logo Styling */
.logo {
margin-right: 10px; /* Minimal space between logo and greeting */
}

.logo img {
height: 40px; /* Adjust the height as needed */
}

/* Button Styling */
button {
padding: 20px 40px; /* Bigger inner padding */
border: 2px solid white; /* Hollow buttons with white border */
border-radius: 0; /* No rounded edges */
background-color: transparent; /* Transparent background */
color: white; /* White text */
font-size: 18px; /* Bigger font size */
font-family: 'Inter', sans-serif;
cursor: pointer;
transition: background-color 0.3s, transform 0.3s;
}

button:hover {
background-color: rgba(255, 255, 255, 0.1); /* Light white on hover */
transform: scale(1.05);
}

button:active {
background-color: rgba(255, 255, 255, 0.2); /* Slightly darker on click */
transform: scale(1);
}

/* Main Content */
.main-content {
height: calc(100vh - 100px); /* Viewport height minus header height */
overflow-y: auto;
padding: 20px;
background-color: #f5f5f5;
}
</style>

<!-- Add this in the <head> of your index.html -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">