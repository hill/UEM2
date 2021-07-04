<template lang='pug'>
div
  SmallHeader
  br
  br
  .container(v-if='course')
    .is-flex
      h1.title.mr-3 {{course.name}}
      p.tag.is-medium.is-dark {{course.due}}
    progress.progress.is-primary.my-3(:value='syllabusComplete' max='100') {{syllabusComplete}}%
    .columns.mt-3
      .column.is-8
        .syllabus(v-if='course.syllabus')
          h3.is-4.title Syllabus ({{syllabusComplete}}%)
          hr
          ul.syllabus-content
            li(v-for='point in course.syllabus')
              input(type='checkbox' :id='point.name' :name='point.name' v-model='point.completed')
              label(:for='point.name') &nbsp;{{point.name}}
      .column.is-4
        h3.is-4.title Assessment
        hr
  .container(v-else)
    p Loading...
</template>

<script>

import SmallHeader from '@/components/SmallHeader'
import { CourseService } from '../services/api.service'

export default {
  components: {SmallHeader},
  data() {
    return {
      course: null,
    }
  },
  async created() {
    CourseService.get(this.$route.params.id).then(({data}) => {
      this.course = data
    })
  },
  computed: {
    syllabusComplete() {
      const sum = this.course.syllabus.map(point => point.completed ? 1 : 0).reduce((acc, curr) => acc + curr, 0)
      return Math.round(sum * 100 / this.course.syllabus.length);
    }
  },
  watch: {
    course: {
      deep: true,
      handler: (oldCourse, newCourse) => {
        console.log(oldCourse, newCourse)
        if (newCourse) {
          CourseService.update(
            newCourse.id,
            newCourse.name,
            newCourse.description,
            newCourse.due,
            newCourse.syllabus
          )
        }
      }
    }
  }
}
</script>

<style lang='scss' scoped>
.syllabus-content {
  border-right: 2px solid whitesmoke;
}

.progress::-webkit-progress-value {
  transition: width 0.5s ease;
}
</style>