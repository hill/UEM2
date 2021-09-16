<script setup>
  import { ref } from "@vue/reactivity";
  import { useStore } from "vuex";
  import { useRouter, useRoute } from "vue-router";

  const store = useStore();
  const router = useRouter();
  const route = useRoute();

  const name = ref("");
  const email = ref("");
  const password = ref("");
  const loading = ref(false);
  const error = ref({});
  const state = ref("login");

  function login() {
    loading.value = true;
    store
      .dispatch("login", { email: email.value, password: password.value })
      .then(() => {
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

  function signup() {
    loading.value = true;
    store
      .dispatch("signup", {
        email: email.value,
        password: password.value,
        name: name.value,
      })
      .then(() => {
        if (route.query.next) {
          router.push(route.query.next);
        } else {
          router.push("/transcript");
        }
      })
      .catch((err) => {
        error.value.signup = err;
      });
    loading.value = false;
  }
</script>
<template>
  <div class="auth-container flex flex-col rounded-md shadow-lg p-4 bg-white">
    <img src="/logo.png" class="w-1/2 self-center" />
    <div class="space-y-2" v-if="state == 'login'">
      <h1 class="text-xl font-bold">Login</h1>
      <Field v-model="email" label="email" type="email" />
      <Field
        v-model="password"
        label="password"
        type="password"
        v-on:keyup.enter="login"
      />
      <Button @click="login" label="Log In" />
      <p class="text-red-400" v-if="error.login">{{ error.login }}</p>
      <p class="text-sm">
        Don't have an account?
        <a class="cursor-pointer underline" @click="state = 'signup'"
          >sign up</a
        >
      </p>
    </div>
    <div class="space-y-2" v-if="state == 'signup'">
      <h1 class="text-xl font-bold">Signup</h1>
      <Field v-model="name" label="name" type="name" />
      <Field v-model="email" label="email" type="email" />
      <Field
        v-model="password"
        label="password"
        type="password"
        v-on:keyup.enter="signup"
      />
      <Button @click="signup" label="Sign Up" />
      <p class="text-sm">
        Already have an account?
        <a class="cursor-pointer underline" @click="state = 'login'">log in</a>
      </p>
    </div>
  </div>
</template>
