<script>
  import draggable from "vuedraggable";
  import { MenuAlt4Icon, XIcon } from "@heroicons/vue/solid";
  import { v4 as uuidv4 } from "uuid";
  export default {
    props: {
      modelValue: Array,
      displayProperty: {
        type: String,
        default: "name",
      },
    },
    emits: ["update:modelValue"],
    components: { draggable, MenuAlt4Icon, XIcon },
    data() {
      return {
        newItemName: null,
      };
    },
    methods: {
      addNewItem() {
        if (this.newItemName) {
          this.modelValue.push({
            id: uuidv4(),
            name: this.newItemName,
            completed: false,
          });
          this.$emit("update:modelValue", this.modelValue);
          this.newItemName = null;
        }
      },
      remove(id) {
        this.$emit(
          "update:modelValue",
          this.modelValue.filter((item) => item.id != id)
        );
      },
    },
    computed: {
      dragOptions() {
        return {
          animation: 200,
          ghostClass: "ghost",
          dragClass: "drag",
          handle: ".handle",
        };
      },
    },
  };
</script>
<template>
  <ul>
    <draggable
      v-model="modelValue"
      v-bind="dragOptions"
      @start="drag = true"
      @end="drag = false"
      item-key="id"
    >
      <template #item="{ element }">
        <div class="group p-1 flex align-middle">
          <MenuAlt4Icon
            class="handle cursor-grab h-4 w-4 mr-2 mt-1 text-gray-400"
          />
          <p>{{ element[displayProperty] }}</p>
          <XIcon
            class="h-3 w-3 ml-2 mt-1.5 text-gray-400 hover:text-red-700 cursor-pointer transition-opacity opacity-0 group-hover:opacity-100"
            @click="remove(element.id)"
          />
        </div>
      </template>
    </draggable>
  </ul>
  <!-- TODO(TOM): make field with button a thing -->
  <div class="mt-4 grid grid-flow-col gap-2">
    <Field
      v-on:keyup.enter="addNewItem()"
      v-model="newItemName"
      class="col-span-10"
      label="Add New"
      autocomplete="off"
    />
    <Button
      class="col-span-2 h-2/3 mt-5"
      size="md"
      label="Add"
      @click="addNewItem()"
    />
  </div>
</template>

<style lang="scss" scoped>
  .ghost {
    opacity: 0;
  }

  .drag {
    z-index: 1000;
  }

  .cursor-grab {
    cursor: grab;
    &:active {
      cursor: grabbing;
    }
  }
</style>
