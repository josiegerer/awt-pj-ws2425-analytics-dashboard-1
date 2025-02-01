<template>
  <div class="keywords-list">
    <h3>Top 5 Keywords</h3>
    <div class="keyword-item" v-for="(keyword, index) in keywords" :key="index">
      <div class="keyword-main">
        <span class="keyword-number">{{ index + 1 }}. </span>
        <span class="keyword-name">{{ keyword.keyword }}</span>
        <span class="keyword-count">{{ keyword.count }}x</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "KeywordsList",
  data() {
    return {
      keywords: [], // Holds the top 5 keywords
    };
  },
  methods: {
    async fetchKeywords() {
      try {
        const authToken = document.cookie.match(/(^| )auth_token=([^;]+)/)?.[2];
        if (!authToken) {
          console.error("Authentication token not found.");
          return;
        }

        const response = await fetch("http://localhost:8000/searchCount", {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        this.processKeywords(data.searchCount);
      } catch (error) {
        console.error("Error fetching keywords:", error);
      }
    },
    processKeywords(searchData) {
      // Convert object into an array of keyword objects
      const keywordArray = Object.entries(searchData).map(([url, count]) => ({
        keyword: decodeURIComponent(url.split("/").pop().replace(/_/g, " ")), // Extract keyword
        count,
      }));

      // Sort by count (descending) and take the top 5
      this.keywords = keywordArray.sort((a, b) => b.count - a.count).slice(0, 5);
    },
  },
  mounted() {
    this.fetchKeywords();
  },
};
</script>

<style scoped>
.keywords-list {
  padding: 10px 0;
  width: 100%;
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
  flex-grow: 1; 
}

.keyword-number {
  font-weight: 500;
}

.keyword-name {
  font-weight: 500;
  flex-grow: 1; 
  text-align: left; 
}

.keyword-count {
  color: #666;
  text-align: right; 
  min-width: 40px; 
}
</style>
