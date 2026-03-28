<template>
  <input id="topic" type="text" placeholder="Topic"/>
  <button @click="AddTopic"> Add topic</button>
</template>

<script setup>

function AddTopic() {
  const topic = document.getElementById("topic").value;
  return fetch(`http://localhost:8001/add_topic?topic=${topic}`, {method: 'POST'})
}


</script>

<style scoped>

</style>