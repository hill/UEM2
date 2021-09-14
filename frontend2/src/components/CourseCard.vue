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
    class="container bg-green-300 p-3 shadow-md hover:shadow-lg rounded-lg h-72 flex flex-col-reverse cursor-pointer transform hover:-translate-y-2 duration-150"
  >
    <h4 class="text-sm">{{ name }}</h4>
    <h1 class="text-xl sm:text-2xl md:text-3xl font-bold">{{ code }}</h1>
  </div>
</template>

<style lang="scss" scoped></style>
