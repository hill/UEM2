<script>
  export default {
    props: { label: { type: String }, modelValue: { type: Boolean } },
    emits: ["update:modelValue"],
    methods: {
      updateValue() {
        this.$emit("update:modelValue", !this.modelValue);
      },
    },
  };
</script>

<template>
  <div>
    <input
      :name="label"
      :checked="modelValue"
      @change="updateValue()"
      type="checkbox"
      class="rounded border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-300 focus:ring focus:ring-offset-0 focus:ring-indigo-200 focus:ring-opacity-50"
    />
    <label class="ml-3 text-sm" :for="label">{{ label }}</label>
  </div>
</template>
