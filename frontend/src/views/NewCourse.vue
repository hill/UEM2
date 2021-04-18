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
            p.help.is-danger(v-if='errors.name') {{errors.name.join(',')}}
          .field
            label.label Due
            p.help When do you want to complete the course by?
            .control
              input.input(v-model='due' type='date' placeholder='Due At')
            p.help.is-danger(v-if='errors.due') {{errors.due.join(',')}}
          .field
            label.label Course Syllabus
            p.help Be specific here. What are you going to learn. Use actual university syllabii or online courses to assist you in the topics. You will need to do some research.
            .control
              textarea.textarea(v-model='description' placeholder='Course Description')
            p.help.is-danger(v-if='errors.description') {{errors.description.join(',')}}
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
import SmallHeader from '@/components/SmallHeader'
import { CourseService } from '../services/api.service'


export default {
  components: {SmallHeader},
  data() {
    return {
        name: "",
        description: "",
        due: "",
        price: 0,
        status: "completing",
        errors: {}
    }
  },
  methods: {
    async createCourse() {
        console.log("create course")
        const {name, description, due, status, price} = this;
        CourseService.create(name, description, due).then(res => {
          console.log(res)
          this.$router.push('/transcript')
        }).catch(err => {
          if (err.response) {
            this.errors = err.response.data.errors;
          }
        })
      },
  }
}
</script>

<style lang='scss' scoped>
  .price-slider {
    width: 500px;
  }
</style>