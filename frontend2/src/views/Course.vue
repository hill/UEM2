<script>
  import { CourseService } from "../services/api.service";
  import Background from "../components/Background.vue";

  export default {
    components: { Background },
    data() {
      return {
        course: null,
      };
    },
    mounted() {
      CourseService.get(this.$route.params.id).then(({ data }) => {
        this.course = data;
      });
    },
    computed: {
      syllabusComplete() {
        const sum = this.course.syllabus
          .map((point) => (point.completed ? 1 : 0))
          .reduce((acc, curr) => acc + curr, 0);
        return Math.round((sum * 100) / this.course.syllabus.length);
      },
    },
    watch: {
      course: {
        deep: true,
        handler: (oldCourse, newCourse) => {
          if (newCourse) {
            CourseService.update(
              newCourse.id,
              newCourse.name,
              newCourse.description,
              newCourse.due,
              newCourse.syllabus
            );
          }
        },
      },
    },
  };
</script>

<template>
  <div v-if="course">
    <h1>{{ course.name }}</h1>
    <h3>Syllabus ({{ syllabusComplete }}% complete)</h3>
    <ul>
      <li v-for="point in course.syllabus">
        <input
          type="checkbox"
          :id="point.name"
          :name="point.name"
          v-model="point.completed"
        />
        <label :for="point.name">&nbsp;{{ point.name }}</label>
      </li>
    </ul>
  </div>
  <div v-else>
    <p>Loading...</p>
  </div>
</template>
