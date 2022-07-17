<script>
  export default {
    props: ["label", "type", "autocomplete", "modelValue"],
    emits: ["update:modelValue"],
    methods: {
      updateValue() {
        this.$emit("update:modelValue", this.$refs.inputField.value);
      },
    },
  };
</script>

<template>
  <div class="flex flex-col">
    <label class="text-gray-700 text-sm" :for="label">{{ label }}</label>
    <input
      class="p-2 rounded-md bg-gray-200 border-0"
      :name="label"
      :type="type"
      :autocomplete="autocomplete ? autocomplete : 'on'"
      :value="modelValue"
      @input="updateValue()"
      ref="inputField"
    />
  </div>
</template>
