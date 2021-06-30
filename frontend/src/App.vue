<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
import Header from './components/Header'

export default {
  components: {Header},
  data() {
    return {
      signedIn: false
    }
  },
}
</script>

<style lang="scss">
@import '~buefy/dist/buefy.css';
@import './assets/main.scss';
</style>
