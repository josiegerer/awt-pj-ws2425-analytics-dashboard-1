<template>
  <div class="stat-card">
    <h3>{{ title }}</h3>
    <div class="stat-content">
      <div class="value">{{ value }}</div>
      <div :class="['change', changeType]">
        {{ change }} in the last 30 days
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: String,
    value: String,
    change: String,
    changeType: String
  }
}
</script>

<style scoped>
.stat-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stat-content {
  display: flex;
  align-items: baseline;
  gap: 10px;
}

.value {
  font-size: 24px;
  font-weight: bold;
}

.change {
  font-size: 14px;
}

.positive {
  color: #22c55e;
}

.negative {
  color: #ef4444;
}
</style>
