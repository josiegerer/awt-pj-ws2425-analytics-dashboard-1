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
            {{ course.completed }} / {{ course.assigned }} students 
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
                {{ subcourse.completed }} / {{ subcourse.assigned }} students 
                ({{ subcourse.progress }}%)
              </span>
              <button class="toggle-button">{{ subcourse.open ? '▼' : '▶' }}</button>
            </div>
            <ul v-if="subcourse.open" class="assessment-list">
              <li v-for="assessment in subcourse.assessments" :key="assessment.id">
                <div class="assessment-details">
                  <span>{{ assessment.name }}</span>
                  <div class="progress-bar">
                    <div class="progress" :style="{ width: assessment.passRate + '%' }"></div>
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
    <p v-if="loading">Loading...</p>
  </div>
</template>

<script>

export default {
  name: "CourseCompletionChart",
  data() {
    return {
      chartSeries: [], // Will hold fetched data
      chartOptions: {
        chart: {
          type: "bar",
          zoom: { enabled: false },
          toolbar: { show: false }
        },
        plotOptions: {
          bar: {
            horizontal: true,
            columnWidth: "70%",
            endingShape: "rounded"
          }
        },
        dataLabels: {
          enabled: true,
          style: {
            fontSize: "10px"
          },
          formatter: (val) => `${val}%`,
          offsetX: 5
        },
        xaxis: {
          categories: [], // Will be dynamically updated
          labels: {
            style: { fontSize: "10px" },
            trim: false,
            maxHeight: 120,
            wrap: true
          }
        },
        yaxis: {
          min: 0,
          max: 100,
          labels: {
            formatter: (val) => `${val}%`
          },
          title: { text: "Completion Rate (%)" }
        },
        colors: ["#4caf50"], // Green for completion rate
        tooltip: {
          y: { formatter: (val) => `${val}%` }
        }
      }
    };
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch("http://localhost:8000/courseCompletionRate");
        const data = await response.json();
        const activities = data.activitiesSummary;

        // Extract course names and completion rates
        this.chartOptions = {
          ...this.chartOptions,
          xaxis: {
            categories: activities.map(activity =>
              activity.activityId.split("/").pop().replace(/_/g, " ")
            )
          }
        };

        this.chartSeries = [
          {
            name: "Completion Rate",
            data: activities.map(activity =>
              Math.round((activity.completed / activity.assigned) * 100) || 0 // Prevent NaN errors
            )
          }
        ];
      } catch (error) {
        console.error("Error fetching course completion data:", error);
      }
    }
  },
  mounted() {
    this.fetchData();
  }
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
  background-color: #f9f9f9;
  border-radius: 5px;
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
  background-color: #4caf50; /* Green for completion rate */
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
