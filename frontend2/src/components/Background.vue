<script>
  import VueP5 from "./p5.vue";
  import { PaletteService } from "../services/palette.service";
  export default {
    components: { VueP5 },
    props: ["color"],
    data() {
      return {
        canvas: null,
      };
    },
    methods: {
      setup(sk) {
        this.canvas = sk.createCanvas(
          this.$refs.p5Container.clientWidth,
          this.$refs.p5Container.clientHeight
        );
        window.addEventListener("resize", () => {
          if (this.$refs.p5Container) {
            sk.resizeCanvas(
              this.$refs.p5Container?.clientWidth ?? 0,
              this.$refs.p5Container?.clientHeight ?? 0
            );
          }
          // this.drawElements(sk);
        });
      },
      draw(sk) {
        this.drawElements(sk);
      },
      drawElements(sk) {
        sk.background(this.color);
      },
    },
  };
</script>
<template>
  <div ref="p5Container">
    <VueP5 v-on="this" />
  </div>
</template>
