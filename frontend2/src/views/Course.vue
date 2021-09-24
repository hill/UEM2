<script>
  import { CourseService } from "../services/api.service";
  import CourseCard from "../components/CourseCard.vue";

  export default {
    components: { CourseCard },
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
    <header class="bg-gray-300">
      <div class="grid grid-cols-4 lg:grid-cols-5 container mx-auto p-3">
        <CourseCard
          :code="course.code"
          :name="course.name"
          :status="course.status"
        />
        <div class="p-4 col-span-3">
          <h1 class="text-3xl font-bold">{{ course.name }}</h1>
          <p
            class="px-2 py-1 text-sm inline-block border border-gray-600 rounded-lg"
          >
            {{ course.due }}
          </p>
        </div>
      </div>
    </header>
    <main class="container mx-auto mt-4 p-3">
      <h3 class="text-lg font-bold">Syllabus ({{ syllabusComplete }}%)</h3>
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
    </main>
  </div>
  <div v-else>
    <p>Loading...</p>
  </div>
</template>
