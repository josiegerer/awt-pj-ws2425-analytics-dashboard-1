<template>
  <div class="activity-revisits-container">
    <h3>Activity Revisits</h3>
    <div class="activity-revisits-content">
      <ol class="activity-list">
        <li v-for="(item, index) in visibleData" :key="item.course" class="activity-item">
          <div class="activity-info">
            <span>{{ index + 1 }}. {{ item.course }}</span>
            <div class="activity-subtitle">{{ item.change }}</div>
          </div>
          <div class="activity-count">{{ item.count }}x</div>
        </li>
      </ol>
    </div>
    <button @click="toggleView" class="view-more-button">
      {{ showAll ? 'View Less' : 'View All' }}
    </button>
  </div>
</template>

<script>
export default {
  name: "ActivityRevisits",
  props: {
    data: {
      type: Array,
      required: true,
      default: () => [
        { course: "Course 1: Bäume pflanzen", count: 20, change: "+5 in the last 30 days" },
        { course: "Course 2: Bäume auskappen", count: 8, change: "+1 in the last 30 days" },
        { course: "Course 3: Bäume ausdünnen", count: 15, change: "+10 in the last 30 days" },
        { course: "Course 4: Bäume schützen", count: 13, change: "+13 in the last 30 days" },
        { course: "Course 5: Bäume gießen", count: 18, change: "+8 in the last 30 days" },
        { course: "Course 6: Bäume schneiden", count: 22, change: "+12 in the last 30 days" },
        { course: "Course 7: Bäume düngen", count: 10, change: "+3 in the last 30 days" },
      ],
    },
  },
  data() {
    return {
      showAll: false,
    };
  },
  computed: {
    visibleData() {
      return this.showAll ? this.data : this.data.slice(0, 3);
    },
  },
  methods: {
    toggleView() {
      this.showAll = !this.showAll;
    },
  },
};
</script>

<style scoped>
h3 {
  text-align: left; /* Align title to the left */
  font-size: 15px;
  color: black;
}

.activity-revisits-content {
  margin-top: 20px;
}

.activity-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.activity-info {
  display: flex;
  flex-direction: column;
}

.activity-list {
  list-style-type: decimal;
  font-family: Inter, ui-sans-serif, system-ui, sans-serif;
  font-weight: 600;
  color: black;
}

.activity-subtitle {
  font-size: 12px;
  color: green;
  font-family: Roboto, ui-sans-serif, system-ui, sans-serif;
}

.activity-count {
  font-size: 20px;
  font-family: Inter, ui-sans-serif, system-ui, sans-serif;
  font-weight: 600;
  color: black;
}

.view-more-button {
  margin-top: 10px;
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  background-color: grey;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 14px;
}

.view-more-button:hover {
  background-color: darkgrey;
  font-size: 14px;
}
</style>
