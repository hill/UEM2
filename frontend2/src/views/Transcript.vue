<script>
  import CourseCard from "../components/CourseCard.vue";
  export default {
    components: { CourseCard },
  };
</script>

<template>
  <div class="flex justify-center">
    <div class="bg-white sm:w-4/5 p-2 justify-self-center">
      <h1 class="text-xl font-bold">Transcript</h1>
      <div class="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <CourseCard
          code="STAT101"
          name="Intro to Statistics"
          status="in progress"
        />
        <CourseCard
          code="STAT101"
          name="Intro to Statistics"
          status="in progress"
        />
        <CourseCard
          code="STAT101"
          name="Intro to Statistics"
          status="in progress"
        />
        <CourseCard
          code="STAT101"
          name="Intro to Statistics"
          status="in progress"
        />
      </div>
      <div class="watermark"></div>
    </div>
  </div>
</template>

<style lang="scss">
  .watermark {
    width: 300px;
    height: 300px;
    position: absolute;
    bottom: 0;
    right: 0;
    background: url("/logo_watermark.png");
    background-repeat: no-repeat;
    background-size: 340px;
    opacity: 0.5;
  }
</style>
