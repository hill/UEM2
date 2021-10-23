<script>
  export default {
    props: { modelValue: { type: Boolean } },
    methods: {
      toggleShow() {
        this.$emit("update:modelValue", !this.modelValue);
      },
    },
  };
</script>

<template lang="pug">
.modal.is-active(v-if='modelValue')
  .modal-background(@click='toggleShow()')
  .modal-content(class="w-3/4 sm:w-1/2")
    slot
</template>

<style lang="scss" scoped>
  .modal-content {
    z-index: 150;
    position: absolute;
    top: 10vh;
  }

  .modal {
    display: flex;
    align-items: center;
    flex-direction: column;
    overflow: hidden;
    z-index: 100;
    position: fixed;
    top: 0;
    bottom: 0;
    right: 0;
    left: 0;
  }

  .modal-background {
    background-color: rgba(10, 10, 10, 0.86);
    position: absolute;
    top: 0;
    bottom: 0;
    right: 0;
    left: 0;
  }
</style>
