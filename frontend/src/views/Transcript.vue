<template lang='pug'>
div
  <SmallHeader />
  .transcript-container
    .container
      .columns.is-centered
        .transcript.column.is-10
          h1.subtitle.is-4 Official Academic Transcript – Tom Hill
          h3.title.is-4 Current Semester
          .columns.is-multiline.course-columns
            .column.is-3(v-for='course in courses' :key='course.id')
              CourseCard(:title='course.name' :id='course.id' :status='course.status')
          .watermark
</template>

<script>

import {CourseService} from '../services/api.service'

import SmallHeader from '../components/SmallHeader'
import CourseCard from '../components/CourseCard'

export default {
  name: 'Transcript',
  components: {
    SmallHeader,
    CourseCard,
  },
  data() {
    return {
      
      courses: []
    }
  },
  async created() {
    CourseService.list().then(({data}) => {
      this.courses = data
    }).catch(err => {
      console.log(err)
    })
  },
}
</script>

<style lang='scss' scoped>

$ripped-height: 20px;
$paper-color: #f3f3f3;

.transcript {
    position: relative;
    margin-top: 5em;
    background: $paper-color;
    box-shadow:
    /* The top layer shadow */
    0 1px 2px rgba(0,0,0,0.50),
    /* The second layer */
    0 10px 0 -5px #eee,
    /* The second layer shadow */
    0 10px 1px -4px rgba(0,0,0,0.15),
      /* The third layer */
    0 20px 0 -10px #eee,
    /* The third layer shadow */
    0 20px 1px -9px rgba(0,0,0,0.15);
    min-height: 75vh;
}

.transcript-container {
  position: relative;
  min-height: 100vh;
  background-image: url("/bg_pattern.png");
  background-repeat: no-repeat;
  background-position: -300px 300px;
}

.watermark {
  width: 300px;
  height: 300px;
  position: absolute;
  bottom: 0;
  right: 0;
  background: url('/logo_watermark.png');
  background-repeat: no-repeat;
  background-size: 340px;
  opacity: 0.5;
}

.course-columns {
  display: flex;
  direction: column;
}
</style>