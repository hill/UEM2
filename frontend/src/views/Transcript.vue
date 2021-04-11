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
            .column.is-3
              CourseCard(title='Natural Language Processing', status='completing', price='$1200')
            .column.is-3
              CourseCard(title='Linear Algebra', status='completing', price='$200')
            .column.is-3
              CourseCard(title='+ add new course', :newCourse='true')
          h3.title.is-4 Semester 2
          .columns.is-multiline.course-columns
            .column.is-3
              CourseCard(title='Natural Language Processing', status='passed', price='$1200')
            .column.is-3
              CourseCard(title='Discrete Mathematics', status='failed', price='$1200')
          h3.title.is-4 Semester 1
          .columns.is-multiline.course-columns
            .column.is-3(v-for='course in courses' :key='course.id')
              CourseCard(:title='course.name' :id='course.id' :status='course.status')
</template>

<script>

import SmallHeader from '../components/SmallHeader'
import CourseCard from '../components/CourseCard'

import { API } from 'aws-amplify'
import { listCourses } from '../graphql/queries'
import { onCreateCourse } from '../graphql/subscriptions';

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
    this.getCourses()
    this.subscribe()

    // get the user associated with the cognito identity
    
  },
  methods: {
    async getCourses() {
      const courses = await API.graphql({
        query: listCourses
      })

      this.courses = courses.data.listCourses.items;
    },
    subscribe() {
      API.graphql({query: onCreateCourse}).subscribe({
        next: (eventData) => {
          let course = eventData.value.data.onCreateCourse
          if (this.courses.some(item => item.name === course.name)) return; // remove duplications
          this.courses = [...this.courses, course]; // add the course to the course list
        }
      })
    }
  }
}
</script>

<style lang='scss' scoped>

$ripped-height: 20px;
$paper-color: #f3f3f3;

.transcript {
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
}

.transcript-container {
  position: relative;
  min-height: 100vh;
  background-image: url("/bg_pattern.png");
  background-repeat: no-repeat;
  background-position: -300px 300px;
}

.course-columns {
  display: flex;
  direction: column;
}
</style>