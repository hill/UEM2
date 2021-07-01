<template lang='pug'>
  .home
    Header
    section
      .columns.is-centered
        .acceptance-letter.column.is-8
          .is-flex.is-justify-content-center
            img.logo(src='/logo_watermark.png')
          p Dear [enter name here],
          p On behalf of the Admission Committee, it is my pleasure to offer you admission to the University of Extrinsic Motivation, Class of [death year].
          .watermark

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

section {
  background-color: black;
  min-height: 100vh;
}

.acceptance-letter {
  position: relative;
  margin: 4em;
  padding: 2em;
  background-color: #171616;
  color: white;
}

.logo {
  height: 6em;
  margin: 1em;
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