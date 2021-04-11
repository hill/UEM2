<template lang="pug">
.modal.is-active(v-if='show')
  .modal-background(@click='toggleModal()')
  .modal-content
    slot
  button.modal-close.is-large(@click='toggleModal()')
</template>

<script>
  export default {
    props: ["show"],
    methods: {
      toggleModal() {
        this.$emit("close");
      },
    },
  };
</script>

<style lang="scss" scoped>
  .modal-content {
    width: 75%;
  }
</style>
