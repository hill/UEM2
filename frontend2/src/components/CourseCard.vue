<script>
  export default {
    props: {
      code: String,
      name: String,
      status: String,
    },
  };
</script>

<template>
  <div
    class="bg-green-300 p-3 shadow-md rounded-lg h-72 flex flex-col-reverse cursor-pointer transform hover:shadow-xl hover:-translate-y-1 duration-150"
  >
    <h1 class="text-xl sm:text-2xl md:text-3xl font-bold">{{ code }}</h1>
    <h4 class="text-sm">{{ name }}</h4>
  </div>
</template>

<style lang="scss" scoped></style>
