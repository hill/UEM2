<template lang='pug'>
  .home
    Header
    .landing.hero.is-large
      .landing-image.hero-body
        .overlay
        .container
          .columns
            .column.is-6
              h2.title.has-text-white.is-1 Unleash your redefintion of possible.
              p.subtitle.has-text-white ...or something vague like that
              router-link(to='/login').button.is-white begin your journey
    section.container
      .columns
        .column.is-8
          h3.title.is-3 Ranked #1 in the world
          p Lorem ipsum dolor sit amet consectetur, adipisicing elit. Dolorem officia earum velit dolorum porro nihil facilis natus, rerum eum sit! Labore odio reiciendis delectus, magni cumque reprehenderit architecto deserunt veniam?
      .columns.is-centered.has-text-centered
        .column.is-6
          h3.title.is-3 FAQs
          p 
            b Are you serious?
          p yes.
          p 
            b What happens if I fail?
          p You loose what you put down.
          p 
            b What happens if I succeed?
          p You get your money back.
          p 
            b What if you think I have failed, but I think I have succeeded?
          p I am right. You are wrong.
    footer.footer
      p Authorized by Vice-Chancellor of Everything <a href="hill.xyz" target="_blank">Tom Hill</a>

</template>

<script>
import Header from '@/components/Header'

export default {
  name: 'Home',
  components: {
    Header,
  },
  
}
</script>

<style lang='scss' scoped>

.landing-image {
  position: relative;
  width: 100%;
  height: 70vh;
  background: url('/cover-image.png');
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;

  .overlay {
    position: absolute;
    top: 0;
    bottom: 0;
    right: 0;
    left: 0;
    background-image: linear-gradient(90deg, rgba(8,8,8,0.84) 0%, rgba(216,216,216,0.00) 100%);
  }
}

</style>