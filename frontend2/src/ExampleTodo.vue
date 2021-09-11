<script>
  import { ref } from "vue";

  export default {
    setup() {
      const newTodo = ref("");
      const todos = ref([]);

      function addNewTodo() {
        todos.value.push({
          id: Date.now(),
          done: false,
          content: newTodo.value,
        });
        newTodo.value = "";
      }

      function toggleDone(todo) {
        todo.done = !todo.done;
      }

      function removeTodo(idx) {
        todos.value.splice(idx, 1);
      }

      function markAllDone() {
        todos.value.forEach((todo) => (todo.done = true));
      }

      return {
        addNewTodo,
        newTodo,
        todos,
        toggleDone,
        removeTodo,
        markAllDone,
      };
    },
  };
</script>

<template>
  <div class="p-6 m-5 shadow-md bg-white rounded-lg flex items-center flex-col">
    <h1 class="text-3xl mb-3">Vue 3 Todo App</h1>
    <form class="shadow-lg bg-gray-50" @submit.prevent="addNewTodo">
      <input
        class="p-2 bg-gray-50 focus:outline-none"
        v-model="newTodo"
        name="newTodo"
        autocomplete="off"
      />
      <button
        class="p-2 font-semibold text-white bg-green-500 hover:bg-green-700"
      >
        Add new todo
      </button>
    </form>
    <div class="my-5 p-3 w-1/2">
      <ul>
        <li
          class="flex items-center space-x-3 border-b-2 py-1 border-dashed"
          v-for="(todo, idx) in todos"
          :key="todo.id"
        >
          <input type="checkbox" v-model="todo.done" />
          <h3 @click="toggleDone(todo)" :class="{ 'line-through': todo.done }">
            {{ todo.content }}
          </h3>
          <button
            class="
              bg-gray-200
              text-black text-xs
              hover:bg-red-600 hover:text-white
              rounded-md
              p-0.5
              px-1.5
            "
            @click="removeTodo(idx)"
          >
            x
          </button>
        </li>
      </ul>
    </div>

    <button @click="markAllDone">Complete all</button>
  </div>
</template>

<style>
  html {
    background-color: rgb(218, 235, 238);
  }
</style>
