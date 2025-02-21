<template>
  <!-- Drop Down List with all Subcourses and Activities that the learner is enroled in-->
  <div class="course-completion-container">
    <h3>Course Completion</h3>
    <ul class="course-list">
      <li v-for="course in localCourses" :key="course.id">
        <div @click="toggleCourse(course.id)" class="course-header">
          <span>{{ course.name }}</span>
          <div class="progress-bar">
            <div
              class="progress"
              :style="{ width: course.progress + '%' }"
            ></div>
          </div>
          <span>{{ formatPercentage(course.progress) }}%</span>
          <span
            >{{ course.completedAssessments }}/{{
              course.totalAssessments
            }}</span
          >
          <button class="toggle-button">{{ course.open ? "▼" : "▶" }}</button>
        </div>
        <ul v-if="course.open" class="subcourse-list">
          <li v-for="subcourse in course.subcourses" :key="subcourse.id">
            <div
              @click="toggleSubcourse(course.id, subcourse.id)"
              class="subcourse-header"
            >
              <span>{{ subcourse.name }}</span>
              <div class="progress-bar">
                <div
                  class="progress"
                  :style="{ width: subcourse.progress + '%' }"
                ></div>
              </div>
              <span>{{ formatPercentage(subcourse.progress) }}%</span>
              <span
                >{{ subcourse.completedAssessments }}/{{
                  subcourse.totalAssessments
                }}</span
              >
              <button class="toggle-button">
                {{ subcourse.open ? "▼" : "▶" }}
              </button>
            </div>
            <ul v-if="subcourse.open" class="assessment-list">
              <li
                v-for="assessment in subcourse.assessments"
                :key="assessment.id"
              >
                <span>{{ assessment.name }}</span>
                <span
                  :class="{
                    passed: assessment.status === 'passed',
                    'not-passed': assessment.status === 'not passed',
                  }"
                >
                  {{ assessment.status }}
                </span>
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
      // store main course (with its subcourses)
      localCourses: [],
    };
  },
  methods: {
    transformName(url) {
      // Extract and transform url
      if (!url) return "";
      const parts = url.split("/");
      const namePart = parts[parts.length - 1];
      return namePart.replace(/_/g, " ");
    },
    formatPercentage(value) {
      // Format course completion rate as Percetage if possible
      return value % 1 === 0 ? value.toFixed(0) : value.toFixed(1);
    },
    async fetchData() {
      try {
        // Get the authentication token from cookie
        const authTokenMatch = document.cookie.match(/(^| )auth_token=([^;]+)/);
        const authToken = authTokenMatch ? authTokenMatch[2] : null;
        if (!authToken) {
          console.error("Authentication token not found.");
          return;
        }

        // Fetch parent data to determine the main course name
        const parentResponse = await fetch(
          "http://localhost:8000/parentsOfParents",
          {
            headers: { Authorization: `Bearer ${authToken}` },
          }
        );
        if (!parentResponse.ok) {
          throw new Error(
            `HTTP error from parentsOfParents! Status: ${parentResponse.status}`
          );
        }
        const parentData = await parentResponse.json();
        // Extract parents URL (All values are assumed to be the same)
        const parentUrls = Object.values(parentData.parentOfParents);
        const mainCourseUrl = parentUrls.length ? parentUrls[0] : "";
        const mainCourseName = this.transformName(mainCourseUrl);

        // Fetch the course completion data
        const response = await fetch(
          "http://localhost:8000/assessmentPerformance/learner",
          {
            headers: { Authorization: `Bearer ${authToken}` },
          }
        );
        if (!response.ok) {
          throw new Error(
            `HTTP error from assessmentPerformance! Status: ${response.status}`
          );
        }
        const data = await response.json();

        // Expected data format: { subcourses: [ { name, progress, completedAssessments, totalAssessments, assessments: [ ... ] }, ... ] }
        if (!data || !data.subcourses) {
          console.error("No subcourses found in fetched data", data);
          return;
        }

        // Transform subcourses
        const subcourses = data.subcourses.map((sub, index) => {
          return {
            id: index, 
            // Use URL transformation for subcourse name
            name: this.transformName(sub.name),
            progress: sub.progress,
            completedAssessments: sub.completedAssessments,
            totalAssessments: sub.totalAssessments,
            open: false,
            assessments: sub.assessments.map((assess, idx) => ({
              id: idx,
              // Use URL transformation for assessment names
              name: this.transformName(assess.activityId),
              status: assess.status,
            })),
          };
        });

        // Aggregate overall course data from subcourses
        const totalAssessments = subcourses.reduce(
          (sum, sub) => sum + sub.totalAssessments,
          0
        );
        const completedAssessments = subcourses.reduce(
          (sum, sub) => sum + sub.completedAssessments,
          0
        );
        const overallProgress =
          totalAssessments > 0
            ? (completedAssessments / totalAssessments) * 100
            : 0;

        // Create main course object using the parents name
        const course = {
          id: "course1",
          name: mainCourseName,
          progress: overallProgress,
          completedAssessments: completedAssessments,
          totalAssessments: totalAssessments,
          open: false,
          subcourses: subcourses,
        };

        this.localCourses = [course];
      } catch (error) {
        console.error("Error fetching courses:", error);
      }
    },
    // toggle/ dropdown for course
    toggleCourse(courseId) {
      const course = this.localCourses.find((course) => course.id === courseId);
      if (course) {
        course.open = !course.open;
      }
    },
     // toggle/dropdown for subcourses
    toggleSubcourse(courseId, subcourseId) {
      const course = this.localCourses.find((course) => course.id === courseId);
      if (course) {
        const subcourse = course.subcourses.find(
          (sub) => sub.id === subcourseId
        );
        if (subcourse) {
          subcourse.open = !subcourse.open;
        }
      }
    },
  },
  created() {
    this.fetchData();
  },
};
</script>

<style scoped>
.course-completion-container {
  margin-top: 20px;
  font-family: Arial, sans-serif;
}

h3 {
  text-align: left;
  font-size: 18px;
  color: #333;
  margin-bottom: 15px;
}

.course-list,
.subcourse-list,
.assessment-list {
  list-style-type: none;
  padding-left: 0;
}

.course-header,
.subcourse-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  padding: 10px;
  margin-bottom: 5px;
  background-color: #f9f9f9;
  border-radius: 4px;
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

.toggle-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: #555;
}

.assessment-list li {
  display: flex;
  justify-content: space-between;
  padding: 5px 10px;
  margin-bottom: 5px;
  background-color: #fff;
}

.passed {
  color: green;
}

.not-passed {
  color: #c40d1e;
}

.divider {
  border: none;
  border-bottom: 1px solid #ccc;
  margin: 10px 0;
}
</style>
