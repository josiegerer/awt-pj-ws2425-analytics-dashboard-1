<template>
    <div class="recommendation-box">
      <p>Lorem ipsum dolor sit amet consectetur. Pellentesque quam est sed et nunc tortor. Eget pellentesque elementum convallis pharetra dui euismod odio praesent. Sem nisl sollicitudin nisi tincidunt nulla varius. </p>
    </div>
  </template>
  
  <script>
  export default {
    name: "RecommendationBox",
    props: {
      message: {
        type: String,
        default: "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
      },
    },
  };
  </script>
  
  <style scoped>
  .recommendation-box {
    padding: 20px;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  </style>
  