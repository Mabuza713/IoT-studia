<template>
  <h1 class="title"> Reciever </h1>
  <h2> Topic tab</h2>
  <input id="topic" type="text" placeholder="Topic"/>
  <button @click="AddTopic"> Add topic</button>
  <button @click="getTopics"> Get topics</button>/
  <p>
    {{ topics }}
  </p>
  <br/>
  <h2 style="display: inline;"> Logi z reciever kontenera</h2><br/>
  <span> {{ isStreaming ? 'Stream trwa': 'Stream nie trwa'}}</span>
  <br/>

  <button @click="startStream">start Stream</button>
  <button @click="stopStream">stop Stream</button>
  <button @click="clear_logs">clear logs</button>
  <div class="console">
    <pre>{{ logs }}</pre>
  </div>
</template>

<script setup>
const logs = ref('')
const isStreaming = ref(false)
let topics = ref([])
import {ref} from "vue";
function AddTopic() {
  const topic = document.getElementById("topic").value;
  const response =  fetch(`http://localhost:8001/add_topic?topic=${topic}`, {method: 'POST'})
  getTopics()
  return response
}
let abortController = null
const startStream = async () => {
  isStreaming.value = true
  try {
    abortController = new AbortController();
    const response = await fetch('http://localhost:8001/logs', {
      signal: abortController.signal,
    })

    if (!response.body) throw new Error('No response body')

    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8')

    while (true) {
      const { done, value } = await reader.read()

      if (done){
        break
      }

      logs.value += decoder.decode(value, { stream: true })

    }
  } catch (error) {
    if (error.name === 'AbortError') {console.log('Stream aborted')} else {console.error('Error fetching data:', error)}

  }

}
const getTopics = async () => {
  console.log("get topics")
  const response = await fetch('http://localhost:8001/topics').then(response => response.json())
  topics.value = response.topics
}
const stopStream = () => {
  isStreaming.value = false
  abortController.abort()
  logs.value = ''
}
const clear_logs = () => {logs.value = ''}

</script>
<style scoped>
.title {
  text-align: center;
  margin-top: -3%;
}
</style>