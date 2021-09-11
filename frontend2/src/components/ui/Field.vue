<script>
  import { ref } from "@vue/reactivity";
  export default {
    props: ["label", "type", "value"],
    emits: ["input"],
    methods: {
      updateValue() {
        this.$emit("input", this.$refs.inputField.value);
      },
    },
  };
</script>

<template>
  <div class="flex flex-col">
    <label class="text-gray-700 text-sm" :for="label">{{ label }}</label>
    <input
      class="p-2 rounded-md bg-gray-200"
      :name="label"
      :type="type"
      @input="updateValue()"
      :value="value"
      ref="inputField"
    />
  </div>
</template>
