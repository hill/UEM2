<script>
  import { ref } from "@vue/reactivity";
  export default {
    props: {
      label: String,
      style: String,
      size: {
        type: String,
        default: "sm",
        validator: (value) => ["sm", "md", "lg"].indexOf(value) !== -1,
      },
    },
    setup(props) {
      const btnSize = {
        sm: "px-3 py-1 text-sm",
        md: "px-4 py-2 text-md",
      };

      const base =
        "button border border-gray-300 rounded-lg font-regular bg-white hover:bg-gray-300 hover:text-gray-800 " +
        (props.size in btnSize ? btnSize[props.size] : btnSize.sm);

      const styles = {
        default: base,
        primary:
          base + " bg-red-800 text-white border-red-900 hover:bg-red-700",
      };

      const styleString = ref(
        props.style in styles ? styles[props.style] : styles.default
      );
      return { styleString };
    },
  };
</script>

<template>
  <button :class="styleString">
    {{ label }}
  </button>
</template>

<style lang="scss" scoped>
  .button {
    transition: all 0.125s ease 0s;
    &:hover {
      transform: scale(1.05);
    }
    &:active {
      transform: scale(0.975);
    }
  }
</style>
