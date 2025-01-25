<template>
  <div class="keywords-list">
    <h3>Top 5 Keywords</h3>
    <div class="keyword-item" v-for="(keyword, index) in keywords" :key="index">
      <div class="keyword-main">
        <span class="keyword-number">{{ index + 1 }}. </span>
        <span class="keyword-name">{{ keyword.keyword }}</span> <!-- FIXED -->
        <span class="keyword-count">{{ keyword.count }}x</span>
      </div>
      <span class="keyword-change">{{ keyword.change }} in the last 30 days</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'KeywordsList',
  props: {
    keywords: Array
  }
}
</script>

<style scoped>
.keywords-list {
  padding: 10px 0;
}

.keyword-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.keyword-main {
  display: flex;
  align-items: center;
  gap: 8px;
}

.keyword-number {
  font-weight: 500;
}

.keyword-name {
  font-weight: 500;
}

.keyword-count {
  color: #666;
}

.keyword-change {
  color: #22bb33;
  font-size: 0.9em;
}
</style>
