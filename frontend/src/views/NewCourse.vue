<template lang='pug'>
div
  SmallHeader
  br
  br
  .container
    .columns.is-centered
      .column.is-10
        .form.columns
          .column.is-8
            section
              h3.title New Course
              label.label(for="name") Course Name
              input.input(v-model="name" type="text" name="name")
              label.label(for="due") Completion Date
              input.input(v-model="due" type="date" name="due")
              label.label(for="description") Description
              input.input(v-model="description" type="text" name="description")
            section
              h3.title Syllabus
              input.input(v-model="newSyllabusPoint" type="text" name="description")
              button.button Add
            section
              h3.title Assessment
          .column.is-4
            figure.coverart
</template>

<script>
import SmallHeader from '@/components/SmallHeader'
import { CourseService, ResourceService } from '../services/api.service'


export default {
  components: {SmallHeader},
  data() {
    return {
        name: "",
        description: "",
        due: null,
        syllabus: [],
        suggestedResources: [],
        newSyllabusPoint: "",
        errors: {},
    }
  },
  methods: {
    async createCourse() {
        const {name, description, due, syllabus} = this;
        CourseService.create(name, description, due, syllabus).then(res => {
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
          name: this.newSyllabusPoint,
          completed: false
        })
        this.newSyllabusPoint = ""
      }
    },
    removeSyllabusItem(idx) {
      this.syllabus.splice(idx, 1);
    }
  },
  watch: {
    name: function(oldName, newName) {
      // search for resources with this course name
      ResourceService.find(oldName).then(({data}) => {
        this.suggestedResources = data.resources.slice(0,3);
      })
    }
  }
}
</script>

<style lang='scss' scoped>
  @import '@/assets/theme.scss';

  .form {
    border-radius: 8px;

    section {
      margin: 50px 0;
    }

    input {
      background: #F2F2F2;
      border-radius: 4px;
    }
  }

  .coverart {
    height: 300px;
    width: 100%;
    border-radius: 4px;
  }
</style>