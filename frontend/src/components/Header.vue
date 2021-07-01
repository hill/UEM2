<template lang='pug'>
  header
    .navbar.is-primary
      .navbar-item.logo-text
        router-link(to="/").title.is-3.is-light.is-hidden-tablet The University of Extrinsic Motivation
        router-link(to="/").banner.is-hidden-mobile
    nav.bottom-bar
      router-link(to='about') About UEM
      a Admission
      .spacer.is-hidden-mobile
      .spacer.is-hidden-mobile
      .spacer.is-hidden-mobile
      router-link(to='resources') Resources
      router-link(to='transcript') Current Students
</template>

<script>

export default {
  name: 'Header',
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
@import '@/assets/theme.scss';

$banner-width: 260px;
.banner {
  background: url('/banner.png');
  background-repeat: no-repeat;
  background-size: contain;
  width: $banner-width;
  height: 300px;
  position: absolute;
  top: -5px;
  left: calc(50% - 0.5 * #{$banner-width});
}

@media only screen and (max-width: 1050px) {
  $banner-width: 200px;
  .banner {
    width: $banner-width;
    left: calc(50% - 0.5 * #{$banner-width});
  }
}

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
