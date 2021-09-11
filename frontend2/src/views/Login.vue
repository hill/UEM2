<script setup>
  import { ref } from "@vue/reactivity";
  import { useStore } from "vuex";
  import { useRouter, useRoute } from "vue-router";

  const store = useStore();
  const router = useRouter();
  const route = useRoute();

  const email = ref("");
  const password = ref("");
  const loading = ref(false);
  const error = ref({});

  function login() {
    loading.value = true;

    store
      .dispatch("login", { email: email.value, password: password.value })
      .then(() => {
        console.log("logged in!");
        if (route.query.next) {
          router.push(route.query.next);
        } else {
          router.push("/transcript");
        }
      })
      .catch((err) => {
        error.value.login = "Email or password is incorrect";
      });

    loading.value = false;
  }
</script>
<template>
  <div class="auth-container">
    <h1>Login</h1>
    <label>Email</label>
    <input type="text" v-model="email" />
    <label>Password</label>
    <input type="password" v-model="password" />
    <button @click="login">Login</button>
    <p class="text-red-400" v-if="error.login">{{ error.login }}</p>
  </div>
</template>
