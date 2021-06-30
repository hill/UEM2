<template lang='pug'>
  div
    <SmallHeader />
    .header
      h1 Resource Search
    .columns.is-centered
      .column.is-6
        input.search-bar(v-model='searchTerm' @change='search()' placeholder='search resources...')
        a(@click='newResourceModal = true') + Add a resource
    .container
      .columns.is-centered
        .column.is-8
          SearchResult(
            v-for='resource in resources'
            :key='resource.id'
            :id='resource.id'
            :name="resource.name",
            :url="resource.url", 
            :topics='resource.topics',
            :votes="resource.votes"
          )
          p.has-text-centered(v-if='!resources') No resources found
    .modal(:class='{"is-active": newResourceModal}')
      .modal-background(@click='newResourceModal = false')
      .modal-content
        .card
          .card-content
            .content
              h3.is-size-3 Add a resource
              .field
                label.label Name
                input.input(v-model='newResource.name' placeholder='name')
                p.help.is-danger(v-if='newResourceErrors.name') {{newResourceErrors.name.join(',')}}
              .field
                label.label URL
                input.input(v-model='newResource.url' placeholder='url')
                p.help.is-danger(v-if='newResourceErrors.url') {{newResourceErrors.url.join(',')}}
              .field
                b-field(label='Enter some tags')
                  b-taginput(
                    v-model='newResource.topics'
                    :data='filteredTopics'
                    autocomplete
                    :allow-new='true'
                    icon='label'
                    placeholder='Add a topic'
                    field="name"
                    @typing='getFilteredTopics'
                  ).
                pre(style='max-height: 400px')
                  b Topics:
                  | {{ newResource.topics }}
              button.button(@click='submitResource()') Add Resource
      button.modal-close.is-large(aria-label='close' @click='newResourceModal = false')
</template>

<script>
import SmallHeader from '../components/SmallHeader'
import SearchResult from '../components/SearchResult'

import _ from 'underscore'
import Fuse from 'fuse.js'
import {ResourceService, TopicService} from '../services/api.service'

const defaultNewResource = {
  name: "",
  url: "",
  topics: []
}

export default {
  components: {SmallHeader, SearchResult},
  data() {
    return {
      topics: [],
      filteredTopics: [],
      resources: [],
      searchTerm: "",
      newResourceModal: false,
      newResource: defaultNewResource,
      newResourceErrors: {}
    }
  },
  mounted() {
    ResourceService.list().then(({data}) => {
      this.resources = data.resources;
    })

    TopicService.list().then(({data}) => {
      this.topics = data.topics;
      this.filteredTopics = data.topics;
    })
  },
  methods: {
    search() {
      ResourceService.find(this.searchTerm).then(({data}) => this.resources = data.resources)
    },
    getFilteredTopics(text) {
      this.filteredTopics = this.topics.filter((topic) => {
          return topic.name
              .toString()
              .toLowerCase()
              .indexOf(text.toLowerCase()) >= 0
      })
    },
    submitResource() {
      ResourceService.create(
        this.newResource.name,
        this.newResource.url,
        this.newResource.topics.map(t => t.name)
      ).then(({data}) => {
        this.newResourceModal = false;
        this.resources.push(data);
        this.newResource = defaultNewResource;
      }).catch(err => {
        console.log(err.response)
        this.newResourceErrors = err.response.data.errors;
      })
    }
  }
}
</script>

<style lang='scss' scoped>
  @import '@/assets/theme.scss';
  .header {
    background: $red;
    height: 150px;
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
    padding: 0 10px;
  }

  .modal-content {
    width: 75%;
  }
</style>