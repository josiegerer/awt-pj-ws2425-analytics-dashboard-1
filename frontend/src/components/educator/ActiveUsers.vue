<template>

        <div class="overview-box">
            <h3>Active Users in Course</h3>
            <x>{{ activeUsers }} </x>
            <p :class="userChangeClass">{{ userChangeText }}</p>
        </div>
</template>

<script>
export default {
    data() {
        return {
            activeUsers: 120, // Example number, replace with actual data
            userChange: -65 // Example change, replace with actual data
        };
    },
    computed: {
        userChangeText() {
            const absChange = Math.abs(this.userChange);
            return `${this.userChange > 0 ? '+' : '-'}${absChange} Users in the last 30 days`;
        },
        userChangeClass() {
            return {
                'text-green': this.userChange > 0,
                'text-red': this.userChange < 0
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