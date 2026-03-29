<template>
  <h1 class="title"> ETDataset</h1>
  <h2> Źródło danych</h2>
  <p>Domyślne źródło danych to
    <a href="https://raw.githubusercontent.com/zhouhaoyi/ETDataset/refs/heads/main/ETT-small/ETTh1.csv">
      LINK
    </a>
  </p>
  <input id="data_source" type="text" placeholder="Data source"/>
  <input id="separator" type="text" placeholder="Separator">


  <h2> MQTT PART</h2>
  <p>Tutaj mozna wysyłać i modyfikować topici do mqtt</p>

  <input id="topic" type="text" placeholder="Topic"/><button @click="postMQTT"> POST TO MQTT</button><br/>
  <input id="repeat_mqtt_interval" type="number" placeholder="Repeat interval"/>




  <h2> HTTP PART</h2>
  <input id="where_to_send" type="text" placeholder="Address to send"/>
  <button @click="postHTTP"> POST TO HTTP</button><br/>
  <input id="repeat_http_interval" type="number" placeholder="Repeat interval"/>
  <h2>Abstract</h2>
  <p>
    Some gvrnmt dataset
  </p>

  <IoTable :dataProvider="getData" :columns-provider="getColumns"></IoTable>
</template>

<script setup>
import IoTable from "../components/IoTable.vue";

// https://bip.uke.gov.pl/download/gfx/bip/pl/defaultaktualnosci/140/5/111/pozwolenia_ntc_h_2026-01-28.csv
let columns = []


async function postHTTP() {
  const send_address = document.getElementById("where_to_send").value === "" ? "http://iot-reciever:8001/" : document.getElementById("where_to_send").value;
  const data_source = document.getElementById("data_source").value === "" ? "https://raw.githubusercontent.com/zhouhaoyi/ETDataset/refs/heads/main/ETT-small/ETTh1.csv" : document.getElementById("data_source").value;
  const repeat_interval = document.getElementById("repeat_http_interval").value === "" ? 0.5 : document.getElementById("repeat_http_interval").value;
  const separator = document.getElementById("separator").value === "" ? "," : document.getElementById("separator").value;

  const response = fetch('http://localhost:8000/ETDataset', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(
        {
          data_source: data_source,
          address: send_address,
          repeat_interval: repeat_interval,
          separator: separator
        })
  })
  return {"status": "OK"}
}

async function postMQTT() {
  const data_source = document.getElementById("data_source").value === "" ? "https://raw.githubusercontent.com/zhouhaoyi/ETDataset/refs/heads/main/ETT-small/ETTh1.csv" : document.getElementById("data_source").value;
  const repeat_interval = document.getElementById("repeat_mqtt_interval").value === "" ? 0.5 : document.getElementById("repeat_mqtt_interval").value;
  const topic = document.getElementById("topic").value === "" ? "ETDataset" : document.getElementById("topic").value;
  const separator = document.getElementById("separator").value === "" ? "," : document.getElementById("separator").value;


  const response = fetch('http://localhost:8000/ETDataset/publish', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(
        {
          topic: topic,
          data_source: data_source,
          repeat_interval: repeat_interval,
          separator: separator
        })
  })
  return {"status": "OK"}
}

async function getData() {
  const data_source = document.getElementById("data_source").value === "" ? "https://raw.githubusercontent.com/zhouhaoyi/ETDataset/refs/heads/main/ETT-small/ETTh1.csv" : document.getElementById("data_source").value;
  const separator = document.getElementById("separator").value === "" ? "," : document.getElementById("separator").value;
  return await fetch(`http://localhost:8000/ETDataset?data_source=${data_source}&separator=${separator}`).then(response => response.json()).then(data => data)
}

async function getColumns() {
    const data_source = document.getElementById("data_source").value === "" ? "https://raw.githubusercontent.com/zhouhaoyi/ETDataset/refs/heads/main/ETT-small/ETTh1.csv" : document.getElementById("data_source").value;
    const separator = document.getElementById("separator").value === "" ? "," : document.getElementById("separator").value;

    const columns_temp = await fetch(`http://localhost:8000/ETDataset/columns?data_source=${data_source}&separator=${separator}`).then(response => response.json())
    return columns_temp.map(columnName => ({ key: columnName, label: columnName }))
}
</script>


<style scoped>
.title {
  text-align: center;
  margin-top: -3%;
}
</style>