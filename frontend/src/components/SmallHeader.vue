<template lang='pug'>
  header
    nav
      .container
        .logo.is-flex
          img.crest(src='/logo_crest.svg')
          p
            router-link(to='/transcript') The University of Extrinsic Motivation
        .items
          router-link(to='/new') + New Course
          a Tom Hill
          a(@click='signOut') Sign Out
</template>

<script>

export default {
  name: 'Header',
  props: {
    msg: String
  },
  methods: {
    async signOut() {
      // try {
      //   await Auth.signOut();
      // } catch (error) {
      //   console.log('error signing out: ', error);
      // }
    }
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
