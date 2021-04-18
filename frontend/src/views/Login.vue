<template lang='pug'>
.auth-container
  .auth
    .box
      div(v-if='state == "login"')
        h1.title.is-2 Login
        .field
          label.label Email
          .control
            input.input(v-model='email')
        .field
          label.label Password
          .control
            input.input(v-model='password' type='password')
        p(v-if='error.login') {{error.login}}
        .field.is-grouped
          .control
            button.button.is-primary(@click='login' :class='{"is-loading": loading}') Login
          .control
            p.help-text Don't have an account? <a @click='state = "signup"'>sign up</a>
        
      div(v-if='state == "signup"')
        h1.title.is-2 Sign Up
        .field
          label.label Name
          .control
            input.input(v-model='name')
        .field
          label.label Email
          .control
            input.input(v-model='email')
        .field
          label.label Password
          .control
            input.input(v-model='password' type='password')
        p(v-if='error.signup') {{error.signup}}
        .field.is-grouped
          .control
            button.button.is-primary(@click='signup' :class='{"is-loading": loading}') Sign Up
          .control
            p.help-text Have an account? <a @click='state = "login"'>log in</a>
        
        
      div(v-if='state == "confirm"')
        h1.title.is-2 Confirm Account
        .field
          label.label Email
          .control
            input.input(v-model='email' disabled)
        .field
          label.label Confirmation Code
          .control
            input.input(v-model='code')
        .field.is-grouped
          .control
            button.button.is-primary(@click='confirm' :class='{"is-loading": loading}') Confirm
          .control
            p.help-text Didn't get a code? <a @click='state = "resendConfirm"'>Resend</a>
</template>

<script>

import API from '../services/api.service'

export default {
  name: 'Login',
  data() {
    return {
      state: 'login',
      email: '',
      name: '',
      password: '',
      code: '',
      loading: false,
      error: {
        login: '',
        signup: ''
      }
    }
  },
  async created() {
    // if you are already logged in, go straight to the transcript
    // TODO
    
  },
  methods: {
    async signup() {
      this.loading = true
      this.$store.dispatch('signup', {email: this.email, password: this.password, name: this.name}).then(() => {
        console.log(this.$store.state.user)
        this.$router.push('/transcript')
      }).catch(err => {
        console.log(err)
        this.error.signup = err;
      })
      this.loading = false
    },
    async login() {
      this.loading = true

      this.$store.dispatch('login', {email: this.email, password: this.password}).then(() => {
        this.$router.push('/transcript')
      }).catch(err => {
        this.error.login = 'Email or password is incorrect';
      })

      this.loading = false
    },
    async confirm() {
      this.loading = true
      try {
        await Auth.confirmSignUp(this.email, this.code);
      } catch (error) {
        console.log('error confirming sign up', error);
      }
    },
    async resendConfirm() {
      // try {
      //   await Auth.resendSignUp(this.email);
      //   console.log('code resent successfully');
      // } catch (err) {
      //   console.log('error resending code: ', err);
      // }
    },
    async forgot() {

    }
  }
}
</script>

<style lang='scss'>
@import '@/assets/theme.scss';

.auth {
  margin: 0 auto;
  width: 460px;
}

.box {
  position: absolute;
  width: 460px;
  top: 30vh;
}

.help-text {
  font-size: 14px;
  margin-top: 10px;
}

:root {
  --amplify-primary-color: #b20000; // can't mix scss vars for some reason?
  --amplify-primary-tint: #b20000;
  --amplify-primary-shade: #890000;
}

.auth-container {
  position: relative;
  min-height: 100vh;
  background-image: url("/bg_pattern.png");
  background-repeat: no-repeat;
  background-position: 60vw 100px;
}

</style>