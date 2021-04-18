<template lang='pug'>
.result.is-flex
  .votes
    <ion-icon name="chevron-up-outline"></ion-icon>
    p {{votes}}
    <ion-icon name="chevron-down-outline"></ion-icon>
  .content
    a(:href="url" target="_blank")
      h3.is-size-4 {{name}}
    .tags
      span.tag.is-link.is-light(v-for='topic in topics') {{topic.name}}
      span.tag
        <ion-icon name="cloud-offline-outline"></ion-icon>
</template>

<script>
export default {
  props: ['name', 'url', 'topics', 'votes']
}
</script>

<style lang='scss' scoped>
  @import '@/assets/theme.scss';
  .result {
    padding: 15px 0;
  }
  .content {
    h3 {
      text-decoration: underline;
      color: blue;
    }

    .broken {
      font-size: 12px;
      text-decoration: underline;
    }
  }

  .votes {
    padding: 0 10px;
  }
</style>