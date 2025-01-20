<template>
  <div class="admin-container">
    <!-- Header -->
    <header class="dashboard-header">
      <div class="logo-greeting">
        <div class="logo">
          <img src="@/assets/lms-Logo.png" alt="LMS Logo" />
        </div>
        <div class="greeting">
          <h1>Welcome, {{ userName }}</h1>
        </div>
      </div>
    </header>

    <!-- Dashboard Content -->
    <div class="dashboard">
      <div class="grid-container">
        
      </div>
    </div>
  </div>
</template>


<style scoped>
.educator-container {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  width: 100%;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  grid-gap: 20px;
  padding: 20px;
  background-color: #f5f5f5;
}

.grid-item {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Grid Layout */
.pass-rates {
  grid-column: span 4;
  grid-row: span 2;
}

.assessment-marks {
  grid-column: span 5;
  grid-row: span 2;
}

.active-users {
  grid-column: span 3;
  grid-row: span 1; /* Half height */
}

.course-completion {
  grid-column: span 12;
  grid-row: span 2;
}

.activity-revisits {
  grid-column: span 3;
  grid-row: span 1;
}

@media (max-width: 768px) {
  .grid-container {
    grid-template-columns: repeat(6, 1fr);
  }

  .pass-rates,
  .assessment-marks,
  .activity-revisits,
  .active-users,
  .course-completion {
    grid-column: span 6;
  }
}
</style>