<template lang='pug'>
.result.is-flex
  .votes
    a(@click='upvote()')
      <ion-icon name="chevron-up-outline"></ion-icon>
    p {{currVotes}}
    a(@click='downvote()')
      <ion-icon name="chevron-down-outline"></ion-icon>
  .content
    a(:href="url" target="_blank")
      h3.is-size-4 {{name}}
    .tags
      span.tag.is-link.is-light(v-for='topic in topics') {{topic.name}}
      a.tag(data-tooltip="mark link as broken" @click='markBroken()')
        <ion-icon name="unlink-outline"></ion-icon>
</template>

<script>
import { ResourceService } from '../services/api.service'

export default {
  props: ['name', 'url', 'topics', 'votes', 'id'],
  data() {
    return {
      currVotes: this.votes
    }
  },
  methods: {
    upvote() {
      ResourceService.upvote(this.id).then(() => {
        this.currVotes += 1
      })
    },
    downvote() {
      ResourceService.downvote(this.id).then(() => {
        this.currVotes -= 1
      })
    },
    markBroken() {
      ResourceService.broken(this.id)
      this.$buefy.snackbar.open({
        duration: 3000,
        message:`Thanks - we've flagged that link and will review it`
      })
    }
  }
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
    text-align: center;
  }
</style>