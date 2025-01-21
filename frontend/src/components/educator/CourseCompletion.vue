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
            <span>
              {{ course.completedStudents }} / {{ course.totalStudents }} students 
              ({{ course.progress }}%)
            </span>
            <button class="toggle-button">{{ course.open ? '▼' : '▶' }}</button>
          </div>
          <ul v-if="course.open" class="subcourse-list">
            <li v-for="subcourse in course.subcourses" :key="subcourse.id">
              <div @click="toggleSubcourse(course.id, subcourse.id)" class="subcourse-header">
                <span>{{ subcourse.name }}</span>
                <div class="progress-bar">
                  <div class="progress" :style="{ width: subcourse.progress + '%' }"></div>
                </div>
                <span>
                  {{ subcourse.completedStudents }} / {{ subcourse.totalStudents }} students 
                  ({{ subcourse.progress }}%)
                </span>
                <button class="toggle-button">{{ subcourse.open ? '▼' : '▶' }}</button>
              </div>
              <ul v-if="subcourse.open" class="assessment-list">
                <li v-for="assessment in subcourse.assessments" :key="assessment.id">
                  <div class="assessment-details">
                    <span>{{ assessment.name }}</span>
                    <div class="progress-bar">
                      <div
                        class="progress"
                        :style="{ width: assessment.passRate + '%' }"
                      ></div>
                    </div>
                    <span>
                      {{ assessment.passedStudents }} / {{ assessment.totalStudents }} students 
                      ({{ assessment.passRate }}%)
                    </span>
                  </div>
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
    name: "CourseCompletion",
    props: {
      courses: {
        type: Array,
        required: true,
        default: () => [],
      },
    },
    data() {
      return {
        localCourses: this.courses.map(course => ({
          ...course,
          completedStudents: this.calculateCompletedStudents(course),
          totalStudents: this.calculateTotalStudents(course),
          progress: this.calculateCourseProgress(course),
          subcourses: course.subcourses.map(subcourse => ({
            ...subcourse,
            completedStudents: this.calculateCompletedStudents(subcourse),
            totalStudents: subcourse.totalStudents || course.totalStudents,
            progress: this.calculateSubcourseProgress(subcourse),
          })),
        })),
      };
    },
    methods: {
      calculateCourseProgress(course) {
        const totalStudents = this.calculateTotalStudents(course);
        const completedStudents = this.calculateCompletedStudents(course);
        return totalStudents > 0
          ? Math.round((completedStudents / totalStudents) * 100)
          : 0;
      },
      calculateSubcourseProgress(subcourse) {
        const totalStudents = subcourse.totalStudents;
        const completedStudents = subcourse.assessments.every(
          assessment => assessment.passedStudents === assessment.totalStudents
        )
          ? totalStudents
          : 0;
        return totalStudents > 0
          ? Math.round((completedStudents / totalStudents) * 100)
          : 0;
      },
      calculateCompletedStudents(entity) {
        if (entity.assessments) {
          return entity.assessments.every(
            assessment => assessment.passedStudents === assessment.totalStudents
          )
            ? entity.totalStudents
            : 0;
        }
        if (entity.subcourses) {
          return entity.subcourses.filter(subcourse =>
            subcourse.assessments.every(
              assessment => assessment.passedStudents === assessment.totalStudents
            )
          ).length;
        }
        return 0;
      },
      calculateTotalStudents(entity) {
        if (entity.subcourses) {
          return entity.subcourses.reduce(
            (sum, subcourse) => sum + subcourse.totalStudents,
            0
          );
        }
        if (entity.assessments) {
          return entity.assessments.reduce(
            (sum, assessment) => sum + assessment.totalStudents,
            0
          );
        }
        return entity.totalStudents || 0;
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
  };
  </script>
  
  <style scoped>
  .course-completion-container {
    margin-top: 20px;
  }
  
  .course-header,
  .subcourse-header,
  .assessment-details {
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
    background-color: #4caf50; /* Green for pass rate */
  }
  
  .assessment-list {
    margin-left: 20px;
  }
  
  .toggle-button {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 16px;
  }
  
  .course-list,
  .subcourse-list,
  .assessment-list {
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
  