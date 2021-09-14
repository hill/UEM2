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
        "border border-gray-300 rounded-lg font-regular bg-white hover:bg-gray-300 hover:text-gray-800 " +
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
