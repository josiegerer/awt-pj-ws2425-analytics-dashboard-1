<template>
  <div class="course-completion-container">
    <h3>Course Completion</h3>
    <ul class="course-list">
      <li v-for="parent in parentCourses" :key="parent.activityId">
        <!-- Parent Course -->
        <div @click="toggleCourse(parent.activityId)" class="course-header">
          <span>{{ parent.name }}</span>
          <div class="progress-bar">
            <div class="progress" :style="{ width: parent.progress + '%' }"></div>
          </div>
          <span>{{ formatPercentage(parent.progress) }}%</span>
          <span>{{ parent.completed }}/{{ parent.assigned }}</span>
          <button class="toggle-button">{{ parent.open ? '▼' : '▶' }}</button>
        </div>

        <!-- Subcourses (only visible if parent is expanded) -->
        <ul v-if="parent.open" class="subcourse-list">
          <li v-for="subcourse in parent.subcourses" :key="subcourse.activityId">
            <div @click.stop="toggleCourse(subcourse.activityId)" class="subcourse-header">
              <span>{{ subcourse.name }}</span>
              <div class="progress-bar">
                <div class="progress" :style="{ width: subcourse.progress + '%' }"></div>
              </div>
              <span>{{ formatPercentage(subcourse.progress) }}%</span>
              <span>{{ subcourse.completed }}/{{ subcourse.assigned }}</span>
              <button class="toggle-button">{{ subcourse.open ? '▼' : '▶' }}</button>
            </div>

            <!-- Activities inside Subcourse -->
            <ul v-if="subcourse.open" class="details-list">
              <li v-for="assessment in subcourse.assessments" :key="assessment.id">
                <span>{{ assessment.name }}</span>
                <span :class="{ 'passed': assessment.status === 'passed', 'not-passed': assessment.status === 'not passed' }">
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
      parentCourses: [] // Stores structured courses
    };
  },
  async created() {
    await this.fetchData();
  },
  methods: {
    getCookie(name) {
      const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
      return match ? match[2] : null;
    },
    formatPercentage(value) {
      return value % 1 === 0 ? value.toFixed(0) : value.toFixed(1);
    },
    async fetchData() {
      try {
        const authToken = this.getCookie("auth_token");
        if (!authToken) {
          console.error('Authentication token not found.');
          return;
        }

        // Fetch course completion data
        const [courseCompletionRes, activityNamesRes, parentsRes] = await Promise.all([
          fetch('http://localhost:8000/courseCompletionRate', { headers: { Authorization: `Bearer ${authToken}` } }),
          fetch('http://localhost:8000/getNameForActivityId', { headers: { Authorization: `Bearer ${authToken}` } }),
          fetch('http://localhost:8000/parentsOfActivities', { headers: { Authorization: `Bearer ${authToken}` } })
        ]);

        if (!courseCompletionRes.ok || !activityNamesRes.ok || !parentsRes.ok) {
          throw new Error("Error fetching data");
        }

        const courseCompletionData = await courseCompletionRes.json();
        const activityNamesData = await activityNamesRes.json();
        const parentsData = await parentsRes.json();

        // Create activity name map
        const activityNameMap = new Map();
        activityNamesData.objects.forEach(obj => {
          activityNameMap.set(obj.objectId, obj.objectName);
        });

        // Process the fetched data
        let parentMap = new Map();

        courseCompletionData.activitiesSummary.forEach(activity => {
          let parentId = parentsData.activityParents[activity.activityId]?.[0] || activity.activityId;
          let parentName = activityNameMap.get(parentId) || this.transformName(parentId);

          if (!parentMap.has(parentId)) {
            parentMap.set(parentId, {
              activityId: parentId,
              name: parentName,
              assigned: activity.assigned,
              completed: activity.completed,
              progress: (activity.completed / activity.assigned) * 100,
              open: false,
              subcourses: []
            });
          }

          parentMap.get(parentId).subcourses.push({
            activityId: activity.activityId,
            name: activityNameMap.get(activity.activityId) || this.transformName(activity.activityId),
            assigned: activity.assigned,
            completed: activity.completed,
            progress: (activity.completed / activity.assigned) * 100,
            open: false,
            assessments: activity.assessments || []
          });
        });

        this.parentCourses = Array.from(parentMap.values());
      } catch (error) {
        console.error('Error fetching course data:', error);
      }
    },
    toggleCourse(activityId) {
      const toggleInTree = (courses) => {
        for (let course of courses) {
          if (course.activityId === activityId) {
            course.open = !course.open;
            return;
          }
          if (course.subcourses) toggleInTree(course.subcourses);
        }
      };
      toggleInTree(this.parentCourses);
    },
    transformName(url) {
      if (!url) return '';
      const parts = url.split('/');
      return parts[parts.length - 1].replace(/_/g, ' ');
    }
  }
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
