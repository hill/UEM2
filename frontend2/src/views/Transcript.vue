<script>
  import CourseCard from "../components/CourseCard.vue";
  export default {
    components: { CourseCard },
  };
</script>

<template>
  <div class="flex justify-center">
    <div class="transcript sm:w-4/5 p-5 m-10 justify-self-center min-h-screen">
      <h1 class="text-xl font-bold">Current Semester</h1>
      <div class="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
        <CourseCard
          code="STAT101"
          name="Intro to Statistics"
          status="in progress"
        />
        <CourseCard
          code="RL179"
          name="Reinforcement Learning Fundementals"
          status="in progress"
        />
        <CourseCard code="NN222" name="Neural Networks" status="in progress" />
        <CourseCard
          code="FLP243"
          name="The Feynman Lectures in Physics"
          status="in progress"
        />
        <div
          class="flex p-3 border-dashed border-2 border-gray-300 rounded-lg h-72 cursor-pointer transform hover:shadow-lg duration-150"
        >
          <p class="text-gray-300 self-center">New Course</p>
        </div>
      </div>
      <div class="watermark"></div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .transcript {
    position: relative;
    background: #f3f3f3;
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
