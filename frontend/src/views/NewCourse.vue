<template lang='pug'>
div
  SmallHeader
  br
  br
  .container
    .columns.is-centered
      .column.is-8
        h1.title.is-3 Begin a New Course
        .form
          .field
            label.label Course Name
            p.help What do you want to learn? Discrete Maths Fundementals? Basket weaving 101?
            .control
              input.input(v-model='name' placeholder='Course Name')
          .field
            label.label Course Syllabus
            p.help Be specific here. What are you going to learn. Use actual university syllabii or online courses to assist you in the topics. You will need to do some research.
            .control
              textarea.textarea(v-model='description' placeholder='Course Description')
          .field
            label.label Course Assessment
            p.help How will I know that you've succeeded? What are the assessables and when are they due?
            .control
              textarea.textarea(v-model='description' placeholder='Course Assessment')
          .field
            label.label Course Price
            p.help I am going to charge your card for this. You'll get it back if you don't fuck this up. It should be an amount that will hurt enough to make you do the work.
            br
            .control
              //- input.input(v-model='price' type='number' placeholder='Deposit Price')
              input.price-slider(v-model='price' type='range' min=0 max=2000 step=5)
              p cost if you fail: ${{price}}.00

            
          .field
            .control
              .select.is-primary
                select(v-model='status')
                  option(value='completing') completing
                  option(value='passed') passed
                  option(value='failed') failed
          .field
            .control
              button.button(@click='createCourse') Create Course
</template>

<script>
import { API } from 'aws-amplify'
import { createCourse } from '../graphql/mutations'

import SmallHeader from '@/components/SmallHeader'


export default {
  components: {SmallHeader},
  data() {
    return {
        name: "",
        description: "",
        price: 0,
        status: "completing",
    }
  },
  methods: {
    async createCourse() {
        console.log("create course")
        const {name, description, status, price} = this;
        // if (!name || !description) return
        const course = {name, description, status, price}
        await API.graphql({
          query: createCourse,
          variables: {input: course}
        })

        this.name = ''
        this.description = ''
        this.status = 'completing'

        this.$router.push('/transcript')
      },
  }
}
</script>

<style lang='scss' scoped>
  .price-slider {
    width: 500px;
  }
</style>