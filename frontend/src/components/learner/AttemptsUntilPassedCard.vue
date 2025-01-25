<template>
    <div class="attempts-until-passed-card">
      <h3>Average Attempts Until Passed</h3>
      <p class="attempts-number">ø {{ data }}</p> <!-- Prepending "ø" -->
    </div>
  </template>
  
  <script>
  export default {
    name: 'AttemptsUntilPassedCard',
    props: {
      data: {
        type: Number,
        required: true,
      },
    },
  };
  </script>
  
  <style scoped>

  .attempts-number {
    font-size: 24px;
    font-weight: bold;
    color: black;
    text-align: center;
  }

  h3 {
  text-align: left; /* Align title to the left */
  font-size: 15px;
  color: black;
 }
  </style>
  