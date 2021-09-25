<script>
  import { ResourceService, TopicService } from "../services/api.service";
  import SearchResult from "../components/SearchResult.vue";

  export default {
    components: { SearchResult },
    data() {
      return {
        name: "",
        topics: [],
        filteredTopics: [],
        resources: [],
        searchTerm: "",
      };
    },
    async mounted() {
      const resources = await ResourceService.list();
      this.resources = resources.data;
      const topics = await TopicService.list();
      this.topics = topics.data;
    },
    methods: {
      search() {
        ResourceService.find(this.searchTerm).then(
          ({ data }) => (this.resources = data)
        );
      },
      getFilteredTopics(text) {
        this.filteredTopics = this.topics.filter((topic) => {
          return (
            topic.name.toString().toLowerCase().indexOf(text.toLowerCase()) >= 0
          );
        });
      },
      submitResource() {
        ResourceService.create(
          this.newResource.name,
          this.newResource.url,
          this.newResource.topics.map((t) => t.name)
        )
          .then(({ data }) => {
            this.newResourceModal = false;
            this.resources.push(data);
            this.newResource = JSON.parse(JSON.stringify(defaultNewResource));
          })
          .catch((err) => {
            console.log(err.response);
            this.newResourceErrors = err.response.data.errors;
          });
      },
      // showNewTopic() {
      //   this.$buefy.dialog.prompt({
      //     message: `Create New Topic`,
      //     inputAttrs: {
      //       placeholder: 'e.g. Mathematics',
      //       value: this.$refs.autocomplete.newTag,
      //     },
      //     confirmText: 'Add',
      //     onConfirm: async (value) => {
      //       const response = await TopicService.create(value)
      //       this.topics.push(response.data)
      //       this.newResource.topics.push(response.data)
      //       this.$refs.autocomplete.newTag = null;
      //     }
      //   })
    },
  };
</script>
<template>
  <header class="h-32 bg-red-800 p-5">
    <h1 class="text-3xl text-white font-serif text-center">Resources</h1>
  </header>
  <div class="container mx-auto">
    <SearchResult
      v-for="resource in resources"
      :name="resource.name"
      :url="resource.url"
      :votes="resource.votes"
      :topics="resource.topics"
      :id="resource.id"
    />
  </div>
</template>
