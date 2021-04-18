<template lang='pug'>
div
  SmallHeader
  br
  br
  .container(v-if='course')
    h1.title {{course.name}}
    p {{course}}
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
    // const courseRes = await API.graphql({query: getCourse, variables: {id: this.$route.params.id}})
    // this.course = courseRes.data.getCourse
    CourseService.get(this.$route.params.id).then(({data}) => {
      this.course = data
    })
  }
}
</script>

<style lang='scss' scoped>

</style>