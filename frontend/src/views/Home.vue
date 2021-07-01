<template lang='pug'>
  .home
    Header
    section
      .columns.is-centered
        .acceptance-letter.column.is-8
          .is-flex.is-justify-content-center
            img.logo(src='/logo_watermark.png')
          h2.letter-title Welcome, class of <span class='interactive' contenteditable>{{deathYear}}</span>
          p Dear <span class='interactive' contenteditable>[name]</span>,
          p On behalf of the Admission Committee, it is my pleasure to offer you admission to the University of Extrinsic Motivation, Class of <span class='interactive' contenteditable>{{deathYear}}</span>.
          .is-flex.is-justify-content-center.mt-3
            router-link.button(to='/login?signup=true') Begin Here
          .watermark

</template>

<script>
import Header from '@/components/Header'

export default {
  name: 'Home',
  components: {
    Header,
  },
  data() {
    return {
      deathYear: "[death year]"
    }
  }
  
}
</script>

<style lang='scss' scoped>

.home {
  background-color: black;
  min-height: 100vh;
}

.columns {
  margin-top: 0; // odd. for some reason margin-top here is -12px? ... invesitgate further
}

.acceptance-letter {
  position: relative;
  margin: 8rem 4rem;
  padding: 2rem;
  background-color: #171616;
  color: white;
}

.letter-title {
  font-size: 3em;
  text-align: center;
}

.interactive {
  background-color: white;
  color: black;
}

.logo {
  height: 6rem;
  margin: 1rem;
}

.watermark {
  width: 300px;
  height: 300px;
  position: absolute;
  bottom: 0;
  right: 0;
  background: url('/logo_watermark.png');
  background-repeat: no-repeat;
  background-size: 340px;
  opacity: 0.05;
}

</style>