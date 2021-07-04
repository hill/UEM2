<template lang='pug'>
  div
    <SmallHeader />
    .header
      h1 Resource Search
    .columns.is-centered
      .column.is-6
        input.search-bar(v-model='searchTerm' @change='search()' placeholder='search resources...')
        a(v-if='user' @click='newResourceModal = true') + Add a resource
        router-link(v-else to='/login?next=/resources') + Add a resource (log in)
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
                    ref="autocomplete"
                    :allow-new='false'
                    icon='label'
                    placeholder='Add a topic'
                    field="name"
                    @typing='getFilteredTopics'
                  )
                    <template #header>
                      <a @click="showNewTopic">
                        <span> Add new... </span>
                      </a>
                    </template>
              button.button(@click='submitResource()') Add Resource
      button.modal-close.is-large(aria-label='close' @click='newResourceModal = false')
</template>

<script>
import SmallHeader from '../components/SmallHeader'
import SearchResult from '../components/SearchResult'

import _ from 'underscore'
import {mapState} from 'vuex'
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
      name: '',
      topics: [],
      filteredTopics: [],
      resources: [],
      searchTerm: "",
      newResourceModal: false,
      newResource: JSON.parse(JSON.stringify(defaultNewResource)),
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
        this.newResource = JSON.parse(JSON.stringify(defaultNewResource));
      }).catch(err => {
        console.log(err.response)
        this.newResourceErrors = err.response.data.errors;
      })
    },
    showNewTopic() {
      this.$buefy.dialog.prompt({
        message: `Create New Topic`,
        inputAttrs: {
          placeholder: 'e.g. Mathematics',
          value: this.$refs.autocomplete.newTag,
        },
        confirmText: 'Add',
        onConfirm: async (value) => {
          const response = await TopicService.create(value)
          this.topics.push(response.data)
          this.newResource.topics.push(response.data)
          this.$refs.autocomplete.newTag = null;
        }
      })
    }
  },
  computed: mapState(['user'])
  
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
    .card {
      min-height: 80vh;
    }
  }
</style>