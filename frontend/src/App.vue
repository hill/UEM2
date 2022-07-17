<script>
  import SmallHeader from "./components/SmallHeader.vue";
  export default {
    components: { SmallHeader },
  };
</script>

<template>
  <SmallHeader></SmallHeader>
  <router-view></router-view>
</template>

<style>
  body {
    @apply bg-gray-50;
  }
</style>
