<script setup>
  import { computed } from "vue";
  import { useStore } from "vuex";

  const store = useStore();
  const user = computed(() => store.state.user);
</script>
<template>
  <div
    class="small-header-color w-full p-0.5 px-3 text-white h-8 font-mono flex justify-between"
  >
    <router-link to="/transcript">Motivation University</router-link>
    <p v-if="user">{{ user.name }}</p>
  </div>
</template>

<style scoped>
  .small-header-color {
    background-color: #222; /* TODO(TOM): add to pallette */
    border-top: #7e0a0c 4px solid;
  }
</style>
