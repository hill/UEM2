<template lang='pug'>
div
  SmallHeader
  .header
    h1 {{ name }}
    p {{ userId }}
  h3 Current Courses
  h3 Completed Courses
</template>

<script>
import SmallHeader from '../components/SmallHeader'
export default {
    components: {SmallHeader},
    data() {
        return {
            name: "Tom Hill",
            userId: null
        }
    },
    mounted() {
        this.userId = this.$route.params.studentId;
    },
}
</script>

<style lang="scss" scoped>
@import '@/assets/theme.scss';
.header {
    background: $red;
    height: 150px;

    h1 {
        text-align: center;
        font-size: 4em;
        font-weight: 700;
        color: white;
    }
}
</style>