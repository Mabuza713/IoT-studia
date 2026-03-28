<template>
  <div class="table-container">
    <button @click="loadData"> FECZ DATA WITH HTTP</button>
    <button @click=""> FECZ DATA USING MQTT</button>
    <table>
      <thead>
        <tr>
          <th v-for="col in columns" :key="col.key">
            {{ col.label }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="items.length === 0">
          <td :colspan="columns.length">Brak danych do wyświetlenia.</td>
        </tr>

        <tr v-for="(item, index) in items" :key="item.id || index">
          <td v-for="col in columns" :key="col.key">
            {{ item[col.key] }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import mqtt from 'mqtt'

const props = defineProps({
  columns: {
    type: Array,
    required: true
  },
  dataProvider: {
    type: Function,
    required: true
  },
  topic: {
    type: String,
    required: true
  }
})

const items = ref([])

const loadData = async () => {
  const result = await props.dataProvider()
  items.value = typeof result === 'string' ? JSON.parse(result) : result

}
const client = mqtt.connect('ws://localhost:9001')
client.on('connect', () => {
  console.log('Connected to MQTT broker')
  client.subscribe(props.topic)
})
client.on('message', (topic, message) => {
  const result = message.toString()
  items.value = typeof result === 'string' ? JSON.parse(result) : result
})

</script>

<style scoped>
.table-container {
  width: 100%;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}

th {
  background-color: #f4f4f4;
}

.empty-state {
  text-align: center;
}
</style>