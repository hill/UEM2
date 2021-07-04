<template lang='pug'>
div
  SmallHeader
  .header
    h1 {{ name }}
    .socials-container
      <ion-icon name="logo-twitter" />
      <ion-icon name="logo-github" />
      <ion-icon name="mail-outline" />
      <ion-icon name="globe-outline" />
  .columns.is-centered
    .card.column.is-6
      h3.is-3.title Current Courses
      hr
      h3.is-3.title Completed Courses
      hr
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

.socials-container {
  color: white;
  text-align: center;
  display: flex;
  justify-content: space-around;
  width: 10rem;
  margin: 0 auto;
}
</style>