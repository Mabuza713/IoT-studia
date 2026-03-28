<template>
  <button @click="getData">Pobierz dane</button>
  <div class="table-container">
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

const props = defineProps({
  dataProvider: { type: Function, required: true },
  columnsProvider: { type: Function, required: true },
})

const columns = ref([])
const items = ref([])

const getData = async () => {
  columns.value = await props.columnsProvider()
  const result = await props.dataProvider()
  items.value = typeof result === 'string' ? JSON.parse(result) : result

}
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

</style>