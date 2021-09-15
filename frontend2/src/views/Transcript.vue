<script>
  import CourseCard from "../components/CourseCard.vue";
  import API, { CourseService } from "../services/api.service";
  export default {
    components: { CourseCard },
    data() {
      return { courses: [] };
    },
    mounted() {
      CourseService.list().then(({ data }) => {
        this.courses = data;
      });
    },
  };
</script>

<template>
  <div class="flex justify-center">
    <div
      class="transcript sm:w-4/5 p-5 my-10 sm:m-10 justify-self-center min-h-screen"
    >
      <div class="watermark"></div>
      <h1 class="light-text text-lg font-serif italic mt-3 mb-8 text-center">
        Official Academic Transcript of Tom Hill
      </h1>
      <h1 class="text-3xl font-bold my-3">Current Semester</h1>
      <div
        class="grid grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-4"
      >
        <CourseCard
          v-for="course in courses"
          :code="course.code"
          :name="course.name"
          :status="course.status"
        />
        <router-link to="/new" class="new-item">
          <p class="text-gray-300 self-center">+ New Course</p>
        </router-link>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  $paper-color: #f3f3f3;

  .new-item {
    &:hover {
      background: $paper-color;
    }
    @apply flex
      p-3 
      border-dashed
      border-2
      border-gray-300
      rounded-lg
      h-72
      cursor-pointer
      transform
      hover:shadow-lg
      duration-150;
  }

  .light-text {
    color: rgba(0, 0, 0, 0.2);
  }

  .transcript {
    position: relative;
    background: $paper-color;
    box-shadow:
    /* The top layer shadow */ 0 1px 2px rgba(0, 0, 0, 0.5),
      /* The second layer */ 0 10px 0 -5px #eee,
      /* The second layer shadow */ 0 10px 1px -4px rgba(0, 0, 0, 0.15),
      /* The third layer */ 0 20px 0 -10px #eee,
      /* The third layer shadow */ 0 20px 1px -9px rgba(0, 0, 0, 0.15);
  }

  .watermark {
    width: 20rem;
    height: 20rem;
    position: absolute;
    bottom: 0;
    right: 0;
    background: url("/logo_watermark.png");
    background-repeat: no-repeat;
    background-size: 22rem;
    opacity: 0.5;
  }
</style>
