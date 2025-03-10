<template>
  <div class="app-container">
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
        <!-- Date box -->
        <div class="date-box">
          <span>{{ currentDate }}</span>
        </div>
      </div>
    </header>

    <!-- Dynamic Content -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
import { jwtDecode } from 'jwt-decode'

const LTI_ROLES = {
  STUDENT: 'http://purl.imsglobal.org/vocab/lis/v2/membership#Learner',
  TEACHER: 'http://purl.imsglobal.org/vocab/lis/v2/membership#Instructor',
  ADMIN: 'http://purl.imsglobal.org/vocab/lis/v2/system/person#Administrator'
}

export default {
  name: 'App',
  data() {
    return {
      userName: 'User',
      roles: [],
      currentDate: '',
    }
  },
  computed: {
    showHeader() {
      return !['/educator-dashboard', '/lti/launch'].includes(this.$route.path)
    },
    isStudent() {
      return this.roles.some(role => role === LTI_ROLES.STUDENT)
    },
    isTeacher() {
      return this.roles.some(role => role === LTI_ROLES.TEACHER)
    },
    isAdmin() {
      return this.roles.some(role => role === LTI_ROLES.ADMIN)
    }
  },
  methods: {
    navigateTo(route) {
      this.$router.push(route)
    },
    getCookie(name) {
      const value = `; ${document.cookie}`
      const parts = value.split(`; ${name}=`)
      return parts.length === 2 ? parts.pop().split(';').shift() : null
    },
    fetchUserData() {
      const token = this.getCookie('auth_token')
      
      if (token) {
        try {
          const decoded = jwtDecode(token)
          console.log('Raw Token Data:', decoded)

          // Proxy-Array in normales Array umwandeln
          const rawRoles = decoded.roles || [] // Anpassung für dein Token
          this.roles = JSON.parse(JSON.stringify(rawRoles))
          
          console.log('Processed Roles:', this.roles)
          console.log('Is Student:', this.isStudent)

          this.userName = decoded.name || 'Unknown User'
          this.autoRedirect()

        } catch (error) {
          console.error('Token Error:', error)
          this.$router.push('/login')
        }
      } else {
        this.$router.push('/login')
      }
    },
    autoRedirect() {
      const currentPath = this.$route.path
      console.log('Current Path:', currentPath)

      if (this.isAdmin && !currentPath.includes('admin')) {
        console.log('Redirecting to admin dashboard')
        this.$router.replace('/admin-dashboard')
      }
      else if (this.isTeacher && !currentPath.includes('educator')) {
        console.log('Redirecting to educator dashboard')
        this.$router.replace('/educator-dashboard')
      }
      else if (this.isStudent && !currentPath.includes('student')){
        console.log('Redirecting to student dashboard')
        this.$router.replace('/overall')
      }
      else {
        console.warn('No matching role, staying on current page.')
      }
    },
    getFormattedDate() {
      const date = new Date();
      const options = { weekday: "long", day: "2-digit", month: "2-digit", year: "numeric" };
      return date.toLocaleDateString("en-GB", options).replace(",", ""); // Format: Monday 03/02/2025
    },
  },
  created() {
    this.fetchUserData()
    this.currentDate = this.getFormattedDate(); // Set the date when component is created
  }
}
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

/* Logo Styling */
.logo {
  margin-right: 10px; /* Minimal space between logo and greeting */
}

.logo img {
  height: 40px; /* Adjust the height as needed */
}

/* Main Content */
.main-content {
  height: calc(100vh - 100px); /* Viewport height minus header height */
  overflow-y: auto;
  padding: 20px;
  background-color: #f5f5f5;
}

.date-box {
  background-color: white;
  color: black;
  padding: 8px 15px;
  border-radius: 5px;
  font-weight: bold;
  font-size: 14px;
  position: absolute;
  right: 20px;
  top: 15px;
}
</style>

<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
