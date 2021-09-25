<script>
  import { PaletteService } from "../services/palette.service";
  import Background from "./Background.vue";
  export default {
    components: { Background },
    props: {
      code: String,
      name: String,
      status: String,
    },
    data() {
      return {
        color: "#ffffff",
        textColor: "#000000",
      };
    },
    mounted() {
      this.color = PaletteService.chooseRandomColor();
      this.textColor = PaletteService.getContrastYIQ(this.color);
    },
  };
</script>

<template>
  <div
    class="shadow-md rounded-lg overflow-hidden h-56 sm:h-72 cursor-pointer transform hover:shadow-xl hover:-translate-y-1 duration-150"
  >
    <!-- <Background :color="color" class="bg absolute w-full h-full" /> -->
    <!-- If its just gonna be simple colors, there are easier ways to do this than canvas! -->
    <div :style="{ background: color }" class="bg absolute w-full h-full"></div>
    <div :style="{ color: textColor }" class="flex flex-col-reverse p-3 h-full">
      <h1 class="text-lg sm:text-xl md:text-2xl mlgd:text-3xl font-bold">
        {{ code }}
      </h1>
      <h4 class="text-xs sm:text-sm">{{ name }}</h4>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .bg {
    z-index: -1;
  }
</style>
