<template>
  <div class="course-completion-container">
    <h3>Course Completion</h3>
    <ul class="course-list">
      <li v-for="course in localCourses" :key="course.id">
        <div @click="toggleCourse(course.id)" class="course-header">
          <span>{{ course.name }}</span>
          <div class="progress-bar">
            <div class="progress" :style="{ width: course.progress + '%' }"></div>
          </div>
          <span>{{ course.progress }}%</span>
          <span>{{ course.completedAssessments }}/{{ course.totalAssessments }}</span>
          <button class="toggle-button">{{ course.open ? '▼' : '▶' }}</button>
        </div>
        <ul v-if="course.open" class="subcourse-list">
          <li v-for="subcourse in course.subcourses" :key="subcourse.id">
            <div @click="toggleSubcourse(course.id, subcourse.id)" class="subcourse-header">
              <span>{{ subcourse.name }}</span>
              <div class="progress-bar">
                <div class="progress" :style="{ width: subcourse.progress + '%' }"></div>
              </div>
              <span>{{ subcourse.progress }}%</span>
              <span>{{ subcourse.completedAssessments }}/{{ subcourse.totalAssessments }}</span>
              <button class="toggle-button">{{ subcourse.open ? '▼' : '▶' }}</button>
            </div>
            <ul v-if="subcourse.open" class="assessment-list">
              <li v-for="assessment in subcourse.assessments" :key="assessment.id">
                <span>{{ assessment.name }}</span>
                <span :class="assessment.status">{{ assessment.status }}</span>
              </li>
            </ul>
          </li>
        </ul>
        <hr class="divider" />
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "CourseCompletionChart",
  data() {
    return {
      localCourses: [],
    };
  },
  methods: {
    async fetchData() {
      try {
        const authToken = document.cookie.match(/(^| )auth_token=([^;]+)/)?.[2];
        if (!authToken) {
          console.error('Authentication token not found.');
          return;
        }

        const response = await fetch('http://localhost:8000/courseCompletionRate/learner', {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        this.localCourses = data.map(course => ({ ...course, open: false, subcourses: course.subcourses.map(sub => ({ ...sub, open: false })) }));
      } catch (error) {
        console.error("Error fetching courses:", error);
      }
    },
    toggleCourse(courseId) {
      const course = this.localCourses.find(course => course.id === courseId);
      if (course) course.open = !course.open;
    },
    toggleSubcourse(courseId, subcourseId) {
      const course = this.localCourses.find(course => course.id === courseId);
      if (course) {
        const subcourse = course.subcourses.find(sub => sub.id === subcourseId);
        if (subcourse) subcourse.open = !subcourse.open;
      }
    },
  },
  created() {
    this.fetchCourses();
  },
};
</script>

<style scoped>
.course-completion-container {
  margin-top: 20px;
}

.course-header, .subcourse-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  padding: 10px;
  margin-bottom: 5px;
}

.progress-bar {
  width: 50%;
  background-color: #f5f5f5;
  border-radius: 4px;
  overflow: hidden;
  margin: 0 10px;
}

.progress {
  height: 10px;
  background-color: #c40d1e;
}

.assessment-list {
  margin-left: 20px;
}

.assessment-list li {
  display: flex;
  justify-content: space-between;
  padding: 5px 10px;
  margin-bottom: 5px;
}

.passed {
  color: green;
}

.not-passed {
  color: #c40d1e;
}

.toggle-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
}

.course-list, .subcourse-list, .assessment-list {
  list-style-type: none;
  padding-left: 0;
}

.subcourse-list {
  margin-left: 20px;
}

.divider {
  border: 1px solid #ccc;
  margin: 10px 0;
}
</style>
