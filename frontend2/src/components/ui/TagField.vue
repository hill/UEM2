<script>
  export default {
    props: ["label", "modelValue"],
    emits: ["update:modelValue"],
    data() {
      return {
        tags: [],
      };
    },
    methods: {
      addTag(event) {
        event.preventDefault();
        let value = event.target.value.trim();
        if (value.length > 0) {
          this.tags.push(value);
          event.target.value = "";
        }
        this.updateValue();
      },
      removeTag(index) {
        this.tags.splice(index, 1);
        this.updateValue();
      },
      removeLastTag(event) {
        if (event.target.value.length === 0) {
          this.removeTag(this.tags.length - 1);
          this.updateValue();
        }
      },
      updateValue() {
        this.$emit("update:modelValue", this.tags);
      },
    },
  };
</script>

<template>
  <div class="flex flex-col">
    <label class="text-gray-700 text-sm" :for="label">{{ label }}</label>
    <div class="tag-input rounded-md bg-gray-200 flex group group-focus:ring-2">
      <div
        v-for="(tag, index) in tags"
        :key="tag"
        class="bg-blue-200 rounded-md m-1 my-2 p-1 text-xs block whitespace-nowrap"
      >
        <span
          class="opacity-75 cursor-pointer whitespace-nowrap"
          @click="removeTag(index)"
          >x</span
        >
        {{ tag }}
      </div>
      <input
        class="px-1 border-0 outline-none bg-gray-200 focus:ring-0 w-full rounded-md text-sm"
        :name="label"
        type="text"
        autocomplete="off"
        placeholder="Enter a tag"
        @keydown.enter="addTag"
        @keydown.,="addTag"
        @keydown.tab="addTag"
        @keydown.delete="removeLastTag"
      />
    </div>
  </div>
</template>

<style lang="scss"></style>
