<template lang='pug'>
  router-link(:to="!newCourse ? '/course/' + id : '/new'").course(:class='{"new" : newCourse, "failed" : status == "failed", "passed" : status == "passed"}')
    h4 {{title}}
    .info
      p.status {{status}}
      p.price {{price}}
</template>

<script>
export default {
  props: ['title', 'status', 'price', 'newCourse', 'id'],
    
}
</script>

<style lang='scss' scoped>
@import '@/assets/main.scss';

.course {
  color: black;
  height: 100%;
  background-color: #b8c8ff;
  border: 1px solid #554eff;
  border-radius: 4px;
  padding: 5px 10px;
  display: flex;
  flex-direction: column;
  transition: all 0.2s ease;

  p {
    display: inline-block;
    font-size: 12px;
  }

  .info {
      margin-top: auto;
      width: 100%;
      display: flex;
      justify-content: space-between;
  }

  &:hover {
    transform: scale(1.05);
  }
}

.new {
  background-color: #eee;
  border: 1px solid #ccc;
}

.failed {
  background-color: #ff38429c;
  border: 1px solid #9e192f;
}

.passed {
  background-color: #bae2bf;
  border: 1px solid #157736;
}
</style>