<template lang='pug'>
  div
    <SmallHeader />
    .header
      h1 Resource Search
    .columns.is-centered
      .column.is-6
        input.search-bar
        a + Add a resource
    .container
      .columns.is-centered
        .column.is-8
          SearchResult(
            v-for='resource in resources'
            :key='resource.id'
            :name="resource.name",
            :url="resource.url", 
            :topics='[{name: "mathematics", id:"1"}, {name: "textbooks", id:"2"}]',
            :votes="resource.votes"
          )
          p.has-text-centered(v-if='!resources') No resources found
</template>

<script>
import SmallHeader from '../components/SmallHeader'
import SearchResult from '../components/SearchResult'

import {ResourceService} from '../services/api.service'

export default {
  components: {SmallHeader, SearchResult},
  data() {
    return {
      resources: []
    }
  },
  mounted() {
    ResourceService.list().then(({data}) => {
      this.resources = data.resources;
    })
  }
}
</script>

<style lang='scss' scoped>
  @import '@/assets/theme.scss';
  .header {
    background: $red;
    height: 170px;
    h1 {
      text-align: center;
      font-size: 4em;
      font-weight: 700;
      color: white;
    }
  }

  .search-bar {
    transform: translateY(-20px);
    width: 100%;
    height: 40px;
    background: #F6F6F6;
    box-shadow: 0 2px 4px 0 rgba(0,0,0,0.50);
    border-radius: 8px;
    border-color: transparent;
    outline: none;
    font-family: $family-monospace;
  }
</style>