<template>
  <h1 class="title"> GOV data</h1>
  <h2> Źródło danych</h2>
  <p>Domyślne źródło danych to
    <a href="https://bip.uke.gov.pl/download/gfx/bip/pl/defaultaktualnosci/140/5/111/pozwolenia_ntc_h_2026-01-28.csv">
      LINK
    </a>
  </p>

  <input id="data_source" type="text" placeholder="Data source"/>
  <input id="separator" type="text" placeholder="Separator"><br/>

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
// https://data.open-power-system-data.org/time_series/2020-10-06/time_series_30min_singleindex.csv
// https://archive.ics.uci.edu/ml/machine-learning-databases/00374/energydata_complete.csv
// https://data.cityofnewyork.us/api/views/c3uy-2p5r/rows.csv?accessType=DOWNLOAD
let columns = []


async function postHTTP() {
  const send_address = document.getElementById("where_to_send").value === "" ? "http://iot-reciever:8001/" : document.getElementById("where_to_send").value;
  const data_source = document.getElementById("data_source").value === "" ? "https://bip.uke.gov.pl/download/gfx/bip/pl/defaultaktualnosci/140/5/111/pozwolenia_ntc_h_2026-01-28.csv" : document.getElementById("data_source").value;
  const repeat_interval = document.getElementById("repeat_http_interval").value === "" ? 0.5 : document.getElementById("repeat_http_interval").value;
  const separator = document.getElementById("separator").value === "" ? ";" : document.getElementById("separator").value;

  const response = fetch('http://localhost:8002/gov_dataset', {
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
  const data_source = document.getElementById("data_source").value === "" ? "https://bip.uke.gov.pl/download/gfx/bip/pl/defaultaktualnosci/140/5/111/pozwolenia_ntc_h_2026-01-28.csv" : document.getElementById("data_source").value;
  const repeat_interval = document.getElementById("repeat_mqtt_interval").value === "" ? 0.5 : document.getElementById("repeat_mqtt_interval").value;
  const topic = document.getElementById("topic").value === "" ? "GOV" : document.getElementById("topic").value;
  const separator = document.getElementById("separator").value === "" ? ";" : document.getElementById("separator").value;


  const response = fetch('http://localhost:8002/gov_dataset/publish', {
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
  const data_source = document.getElementById("data_source").value === "" ? "https://bip.uke.gov.pl/download/gfx/bip/pl/defaultaktualnosci/140/5/111/pozwolenia_ntc_h_2026-01-28.csv" : document.getElementById("data_source").value;
  const separator = document.getElementById("separator").value === "" ? ";" : document.getElementById("separator").value;
  return await fetch(`http://localhost:8002/gov_dataset?data_source=${data_source}&separator=${separator}`).then(response => response.json()).then(data => data)
}

async function getColumns() {
  const data_source = document.getElementById("data_source").value === "" ? "https://bip.uke.gov.pl/download/gfx/bip/pl/defaultaktualnosci/140/5/111/pozwolenia_ntc_h_2026-01-28.csv" : document.getElementById("data_source").value;
  const separator = document.getElementById("separator").value === "" ? ";" : document.getElementById("separator").value;

  const columns_temp = await fetch(`http://localhost:8002/gov_dataset/columns?data_source=${data_source}&separator=${separator}`).then(response => response.json())
  return columns_temp.map(columnName => ({ key: columnName, label: columnName }))
}
</script>


<style scoped>
.title {
  text-align: center;
  margin-top: -3%;
}
</style>