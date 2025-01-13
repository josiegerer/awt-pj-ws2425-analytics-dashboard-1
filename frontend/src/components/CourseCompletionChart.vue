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
  props: {
    courses: {
      type: Array,
      required: true,
      default: () => [],
    },
  },
  data() {
    return {
      localCourses: [...this.courses], // Initialize with prop data
    };
  },
  methods: {
    async fetchCourses() {
      try {
        const response = await fetch('/api/courses');
        const data = await response.json();
        this.localCourses = data; // Update local data property
      } catch (error) {
        console.error('Error fetching courses:', error);
      }
    },
    toggleCourse(courseId) {
      const course = this.localCourses.find(course => course.id === courseId);
      course.open = !course.open;
    },
    toggleSubcourse(courseId, subcourseId) {
      const course = this.localCourses.find(course => course.id === courseId);
      const subcourse = course.subcourses.find(subcourse => subcourse.id === subcourseId);
      subcourse.open = !subcourse.open;
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
  background-color: #c40d1e; /* Red color for the bars */
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
  list-style-type: none; /* Remove bullet points */
  padding-left: 0;
}

.subcourse-list {
  margin-left: 20px; /* Indent subpoints */
}

.divider {
  border: 1px solid #ccc;
  margin: 10px 0;
}
</style>
