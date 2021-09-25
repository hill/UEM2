<script>
  import { ResourceService } from "../services/api.service";
  import {
    ChevronUpIcon,
    ChevronDownIcon,
    EmojiSadIcon,
  } from "@heroicons/vue/outline";

  export default {
    props: ["name", "url", "topics", "votes", "id"],
    components: { ChevronUpIcon, ChevronDownIcon, EmojiSadIcon },
    data() {
      return {
        currVotes: this.votes,
        vote: 0,
      };
    },
    methods: {
      upvote() {
        if (this.vote <= 0) {
          ResourceService.upvote(this.id).then(() => {
            this.currVotes += 1;
          });
          this.vote = this.vote == 0 ? 1 : 0;
        }
      },
      downvote() {
        if (this.vote >= 0) {
          ResourceService.downvote(this.id).then(() => {
            this.currVotes -= 1;
          });
          this.vote = this.vote == 0 ? -1 : 0;
        }
      },
      markBroken() {
        ResourceService.broken(this.id);
        this.$buefy.snackbar.open({
          duration: 3000,
          message: `Thanks - we've flagged that link and will review it`,
        });
      },
    },
  };
</script>

<template>
  <div class="result flex">
    <div class="votes">
      <a
        @click="upvote()"
        class="cursor-pointer hover:text-gray-500"
        :class="{ 'text-gray-300': vote == 1 }"
      >
        <ChevronUpIcon class="h-6 hover:scale-125" />
      </a>
      <p class="text-xl font-serif -mt-1">{{ currVotes }}</p>
      <a
        @click="downvote()"
        class="cursor-pointer hover:text-gray-500 hover:scale-105"
        :class="{ 'text-gray-300': vote == -1 }"
      >
        <ChevronDownIcon class="h-6" />
      </a>
    </div>
    <div class="content mt-3">
      <a :href="url" target="_blank">
        <h3 class="text-xl font-serif cursor-pointer">{{ name }}</h3>
      </a>
      <div class="tags">
        <span
          class="text-xs mr-2 px-2 py-1 bg-gray-200 rounded-md"
          v-for="topic in topics"
          >{{ topic.name }}</span
        >
        <a
          class="cursor-pointer"
          data-tooltip="mark link as broken"
          @click="markBroken()"
        >
          <EmojiSadIcon
            class="h-5 text-gray-300 hover:text-gray-500 inline-block pointer"
          />
        </a>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
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

  .disabled {
    color: gray;
  }
</style>
