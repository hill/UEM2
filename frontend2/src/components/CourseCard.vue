<script>
  import Background from "./Background.vue";
  export default {
    components: { Background },
    props: {
      code: String,
      name: String,
      status: String,
    },
  };
</script>

<template>
  <div
    class="shadow-md rounded-lg overflow-hidden h-72 cursor-pointer transform hover:shadow-xl hover:-translate-y-1 duration-150"
  >
    <Background class="bg absolute w-full h-full" />
    <!-- If its just gonna be simple colors, there are easier ways to do this than canvas! -->
    <div class="flex flex-col-reverse p-3 h-full">
      <h1 class="text-xl sm:text-2xl md:text-3xl font-bold">{{ code }}</h1>
      <h4 class="text-sm">{{ name }}</h4>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .bg {
    z-index: -1;
  }
</style>
