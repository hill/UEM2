<script>
  import { CourseService } from "../services/api.service";
  import CourseCard from "../components/CourseCard.vue";
  import { ExternalLinkIcon } from "@heroicons/vue/outline";

  export default {
    components: { CourseCard, ExternalLinkIcon },
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
    <header class="bg-gray-300 py-3">
      <div
        class="grid grid-cols-4 lg:grid-cols-5 2xl:grid-cols-8 container mx-auto p-3"
      >
        <CourseCard
          :code="course.code"
          :name="course.name"
          :status="course.status"
          :color="course.cover.color"
        />
        <div class="p-4 col-span-3">
          <h1 class="text-3xl font-bold">{{ course.name }}</h1>
          <div class="my-2 space-x-2">
            <span class="tag">
              {{ course.due }}
            </span>
            <a
              v-if="course.primary_resource"
              :href="course.primary_resource"
              class="tag hover:bg-black hover:text-white"
              target="_blank"
            >
              Primary Resource <ExternalLinkIcon class="h-4 inline-block" />
            </a>
          </div>
        </div>
      </div>
    </header>
    <main class="container mx-auto mt-4 p-3 md:grid md:grid-cols-3">
      <div class="col-span-2">
        <h3 class="text-lg font-bold">Syllabus ({{ syllabusComplete }}%)</h3>
        <ul>
          <li v-for="point in course.syllabus">
            <Checkbox
              class="mb-1"
              :label="point.name"
              v-model="point.completed"
            />
          </li>
        </ul>
      </div>
      <div class="mt-8 md:mt-0">
        <h3 class="text-lg font-bold">Assessment</h3>
        <div class="space-y-2">
          <div
            v-for="assessment in course.assignments"
            class="rounded-md shadow-md p-2 border-2"
          >
            <h3>{{ assessment.name }}</h3>
            <p>{{ assessment.due }}</p>
            <p>{{ assessment.complete }}</p>
            <p>{{ assessment.weight }}%</p>
            <Button label="Submit" />
          </div>
        </div>
      </div>
    </main>
  </div>
  <div v-else>
    <p>Loading...</p>
  </div>
</template>

<style scoped>
  .tag {
    @apply px-2 py-1 text-sm inline-block border border-gray-600 rounded-lg;
  }
</style>
