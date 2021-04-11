<template lang='pug'>
  header
    .navbar.is-primary
      .navbar-item.logo-text
        h1.title.is-3.is-light The University of Extrinsic Motivation
    nav.bottom-bar
      a About UEM
      a(@click='showLogin = true') Admission & Enrollment
      a Schools
      router-link(to='transcript') Current Students
    Modal(:show="showLogin", v-on:close="showLogin = false")
      .box
        .form
          h3.title Login
          .field
            .control
              input.input(placeholder='username' v-model='username')
          .field
            .control
              input.input(placeholder='password' v-model='password')
          button.button(@click='login') Login
</template>

<script>
import Modal from '@/components/Modal'

export default {
  name: 'Header',
  components: {Modal},
  props: {
    msg: String
  },
  data() {
    return {
      showLogin: false,
      username: "",
      password: ""
    }
  },
  methods: {
    async login() {
      const credentials = await Auth.signIn({
        username: this.username,
        password: this.password
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
@import '@/assets/theme.scss';
.navbar {
  .logo-text {
    width: 100%;
    text-align: center;
  }
  .title {
    color: white;
    margin: 0 auto;
  }
}
.bottom-bar {
  height: 2em;
  background: $red-tint;
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  a {
    color: white;
    &:hover {
      text-decoration: underline;
    }
  }
}

</style>
