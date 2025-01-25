<template>

    <div class="overview-box">
        <h3>Total Courses</h3>
        <x>{{ totalCourses }} </x>
        <p :class="courseChangeClass">{{ courseChangeText }}</p>
    </div>
</template>

<script>
export default {
data() {
    return {
        totalCourses: 2, // Example number, replace with actual data
        courseChange: +1 // Example change, replace with actual data
    };
},
computed: {
    courseChangeText() {
        const absChange = Math.abs(this.courseChange);
        return `${this.courseChange > 0 ? '+' : '-'}${absChange} Users in the last 30 days`;
    },
    courseChangeClass() {
        return {
            'text-green': this.courseChange > 0,
            'text-red': this.courseChange < 0
        };
    }
}
};
</script>

<style scoped>

h3 {
text-align: left;
font-size: 15px;
color: black;
margin-bottom: 15px;
}
x{
text-align: center;
font-size: 42px;

}

.text-green {
color: green;
}

.text-red {
color: red;
}
</style>