<template lang='pug'>
  header
    nav
      .container
        .logo.is-flex
          img.crest(src='/logo_crest.svg')
          p
            router-link(:to='user ? "/transcript" : "/"') The University of Extrinsic Motivation
        .items(v-if='user')
          router-link(to='/new') + New Course
          router-link(:to='"/student/" + user.id') {{user.name}}
          a(@click='signOut') Sign Out
</template>

<script>
import {mapState} from 'vuex'
export default {
  name: 'Header',
  props: {
    msg: String
  },
  methods: {
    signOut() {
      this.$store.dispatch('logout').then(res => {
        this.$router.push('/')
      })
    }
  },
  computed: {
    ...mapState(['user'])
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
@import '@/assets/theme.scss';

nav {
  height: 2em;
  background: $red-tint;
  .container {
    padding-top: 0.2em;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: white;
    a {
      color: white;
      &:hover {
        text-decoration: underline;
      }
    }

    .items {
      a {
        font-family: $family-monospace;
        display: inline-block;
        padding: 0 0 0 20px;
      }
    }
  }
  .crest {
    height: 1.5em;
    margin-right: 1em;
  }
}

</style>
