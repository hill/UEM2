<script>
  import AuthForm from "../components/AuthForm.vue";
  export default {
    components: { AuthForm },
    setup() {},
  };
</script>
<template>
  <div
    class="flex justify-center items-center h-screen auth-container bg-gray-50"
  >
    <AuthForm class="w-3/4 sm:w-1/3 lg:w-1/4" />
  </div>
</template>

<style scoped>
  .auth-container {
    background-image: url("/bg_pattern.png");
    background-repeat: no-repeat;
    background-position: 60vw 100px;
  }
</style>
