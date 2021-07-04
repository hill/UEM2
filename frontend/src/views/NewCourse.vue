<template lang='pug'>
div
  SmallHeader
  br
  br
  .container
    .columns.is-centered
      .column.is-12
        h1.title.is-3 Begin a New Course
        .form
          .help-field
            .field
              label.label Course Name
              .control
                input.input(v-model='name' placeholder='Course Name')
              p.help.is-danger(v-if='errors.name') {{errors.name.join(',')}}
            .side
              p What are you learning?
          .help-field
            .field
              label.label Due
              .control
                input.input(v-model='due' type='date' placeholder='Due At')
                //- label.radio
                //-   input(type="radio" name="date")
                //-   span 1 month
                //- label.radio
                //-   input(type="radio" name="date")
                //-   span 3 months
                //- label.radio
                //-   input(type="radio" name="date")
                //-   span 6 months

              p.help.is-danger(v-if='errors.due') {{errors.due.join(',')}}
            .side
              p When do you plan on completing the course by?
          .help-field
            .field
              label.label Primary Resources
              .control
                input.input(placeholder="Lectures / online courses / textbooks")
              .suggested
                b Suggested Resources:
                ul
                  li
                    a Introduction to NLP
                  li
                    a Standford NLP
                  li
                    a NLP Basics with Tensorflow and Pytorch
            .side
              p 
                | What resources are you using to learn this content?
                br
                br
                router-link.button.is-link.is-light.is-small(to='/resources') Find Resources
          .help-field
            .field
              label.label Course Syllabus
              //- .control
              //- textarea.textarea(v-model='description' placeholder='Course Description')
              //- ol
              //-   li(v-for='(item, idx) in syllabus') {{ item }} <ion-icon @click='removeSyllabusItem(idx)' name="close-circle-outline"></ion-icon>
              table.table.is-fullwidth
                thead
                  th
                  th Course Point
                  th Assessment
                  th Delete
                tbody
                  tr(v-for='(item, idx) in syllabus')
                    td {{idx + 1}}
                    td {{item.name}}
                    td
                      textarea.textarea
                    td
                      a(@click='removeSyllabusItem(idx)') <ion-icon name="close-circle-outline"></ion-icon>
              div
                .control.has-icons-right
                  input.input(v-model='newItem' @keyup='addSyllabusItem' placeholder="New syllabus point")
                  span.icon.is-small.is-right
                    span.tag <ion-icon name="return-down-back-outline"></ion-icon> <p>enter</p>

              p.help.is-danger(v-if='errors.description') {{errors.description.join(',')}}
            .side
              p What are you going to learn? Use your primary resource to guide. Use chapter headings / lecture titles to guide your syllabus.
          .help-field
            .field
              label.label Course Assessment
              .control
                textarea.textarea(v-model='description' placeholder='Course Assessment')
            .side
              p How will I know that you've succeeded? What are the assessables and when are they due? Some ideas: chapter summaries; capstone project that uses the skills you learnt.
          .help-field
            .field
              label.label Course Price
              br
              .control
                input.price-slider(v-model='price' type='range' min=0 max=500 step=10)
                p cost if you fail: ${{price}}.00
            .side
              p This is the "extrinsic" part. Put some skin in the game. It should be an amount that will hurt enough to make you complete the work. If you pass 50% of the content you get it back. (This is optional, but I find I will actually complete things if I am about to loose a bunch of casss$ssh)

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
        errors: {},
        newItem: "",
        syllabus: []
    }
  },
  methods: {
    async createCourse() {
        console.log("create course")
        const {name, description, due, status, price, syllabus} = this;
        console.log(name, description, due)
        CourseService.create(name, description, due, syllabus).then(res => {
          console.log(res)
          this.$router.push('/transcript')
        }).catch(err => {
          if (err.response) {
            this.errors = err.response.data.errors;
          }
        })
      },
    addSyllabusItem(e) {
      if (e.key == "Enter") {
        this.syllabus.push({
          name: this.newItem,
          completed: false
        })
        this.newItem = ""
      }
    },
    removeSyllabusItem(idx) {
      this.syllabus.splice(idx, 1);
    }
  }
}
</script>

<style lang='scss' scoped>
  @import '@/assets/theme.scss';
  .price-slider {
    width: 500px;
  }

  .help-field {
    display: flex;
    .field {
      flex: 3;
    }
    .side {
      flex: 1;
      padding: 24px 15px;
      p {
        // font-family: $family-primary;
        text-align: right;
        font-size: 12px;
        font-style: italic;
      }
    }
  }

  .suggested {
    font-size: 12px;
  }
</style>