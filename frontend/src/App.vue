<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
import Header from './components/Header'
import {Auth, Hub} from 'aws-amplify'

export default {
  components: {Header},
  data() {
    return {
      signedIn: false
    }
  },
  beforeCreate() {
    Hub.listen('auth', data => {
      console.log('data: ', data)
      const { payload } = data
      if (payload.event === 'signIn') {
        this.signedIn = true
        this.$router.push('/transcript')
      }
      if (payload.event === 'signOut') {
        this.$router.push('/login')
        this.signedIn = false
      }
    })

    // Check if the user is currently signed in
    Auth.currentAuthenticatedUser()
      .then(() => {
        this.signedIn = true
      })
      .catch(() => this.signedIn = false)
  }
}
</script>

<style lang="scss">
@import './assets/main.scss';
</style>
