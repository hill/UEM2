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
      async search() {
        const resources = await ResourceService.find(this.searchTerm);
        this.resources = resources.data;
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
  <header class="h-32 bg-red-800">
    <h1 class="text-4xl pt-9 text-white font-serif text-center">Resources</h1>
    <div class="mt-8 w-3/4 sm:w-1/2 xl:w-1/3 mx-auto">
      <input
        placeholder="Search Learning Resources"
        class="font-serif text-sm rounded-md border-gray-300 shadow-md p-2 w-full"
        v-model="searchTerm"
      />
      <button @click="search()">Search</button>
      <div class="text-right mt-2">
        <p class="font-serif text-sm text-gray-500">+ Add Resource</p>
      </div>
    </div>
  </header>
  <div class="mt-6 container mx-auto">
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
