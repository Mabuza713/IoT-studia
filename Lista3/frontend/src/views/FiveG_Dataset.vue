<template>
  <h1 class="title"> High-Resolution Indoor 5G CSI and Link Metrics Dataset</h1>
  <h2> Źródło danych</h2>
  <p>Domyślne źródło danych to
    <a href="https://bip.uke.gov.pl/download/gfx/bip/pl/defaultaktualnosci/140/5/111/pozwolenia_ntc_h_2026-01-28.csv">
      LINK
    </a>
  </p>
  <input id="data_source" type="text" placeholder="Data source"/>

  <h2> MQTT PART</h2>
  <p>Tutaj mozna wysyłać i modyfikować topici do mqtt</p>
  <input id="topic" type="text" placeholder="Topic"/>
  <button @click="postToMQTT"> POST TO MQTT</button><br/>
  <input id="repeat_mqtt" type="checkbox"><label> Repeat</label><br/>
  <input id="repeat_mqtt_interval" type="number" placeholder="Repeat interval"/>

  <h2> HTTP PART</h2>
  <input id="where_to_send" type="text" placeholder="Address to send"/>
  <button @click="postHTTP"> POST TO HTTP</button><br/>
  <input id="repeat_http" type="checkbox"><label> Repeat</label> <br/>
  <input id="repeat_http_interval" type="number" placeholder="Repeat interval"/>
  <h2>Abstract</h2>
  <p>
    Some gvrnmt dataset
  </p>

  <IoTable id="iotable" :columns="columns" :dataProvider="getDataHTTP" :topic="`5G_Dataset`"></IoTable>
</template>

<script setup>
import IoTable from "../components/IoTable.vue";
const columns = [
  { key: "Lp.", label: "Lp." },
  { key: "identyfikator", label: "identyfikator" },
  { key: "Status", label: "Status" },
  { key: "Numer pozwolenia\/decyzji", label: "Numer pozwolenia/decyzji" },
  { key: "Data pozwolenia\/decyzji", label: "Data pozwolenia/decyzji" },
  { key: "Ważny od", label: "Ważny od" },
  { key: "Ważny do", label: "Ważny do" },
  { key: "Wnioskodawca", label: "Wnioskodawca" },
  { key: "Nazwa multipleksu", label: "Nazwa multipleksu" },
  { key: "Kanał\/blok częstotliwościowy", label: "Kanał/blok częstotliwościowy" },
  { key: "Czestotliwość środkowa [MHz]", label: "Czestotliwość środkowa [MHz]" },
  { key: "Szerokość kanału [MHz]", label: "Szerokość kanału [MHz]" },
  { key: "Nazwa stacji", label: "Nazwa stacji" },
  { key: "Lokalizacja stacji", label: "Lokalizacja stacji" },
  { key: "Województwo", label: "Województwo" },
  { key: "Typ nadajnika", label: "Typ nadajnika" },
  { key: "Producent nadajnika", label: "Producent nadajnika" },
  { key: "Maksymalna dopuszczalna moc wyjściowa nadajnika [kW]", label: "Maksymalna dopuszczalna moc wyjściowa nadajnika [kW]" },
  { key: "Typ anteny", label: "Typ anteny" },
  { key: "Konfiguracja systemu antenowego", label: "Konfiguracja systemu antenowego" },
  { key: "Producent anteny", label: "Producent anteny" },
  { key: "Dł.geogr. (WGS84)", label: "Dł.geogr. (WGS84)" },
  { key: "Sz.geogr. (WGS84)", label: "Sz.geogr. (WGS84)" },
  { key: "Wysokość lokalizacji [m. npm]", label: "Wysokość lokalizacji [m. npm]" },
  { key: "Wysokość anteny [m. npt]", label: "Wysokość anteny [m. npt]" },
  { key: "Polaryzacja", label: "Polaryzacja" },
  { key: "System emisji", label: "System emisji" },
  { key: "ERP[dBW]", label: "ERP[dBW]" },
  { key: "ERP[kW]", label: "ERP[kW]" },
  { key: "Charakterystyka", label: "Charakterystyka" },
  { key: "0°", label: "0°" },
  { key: "10°", label: "10°" },
  { key: "20°", label: "20°" },
  { key: "30°", label: "30°" },
  { key: "40°", label: "40°" },
  { key: "50°", label: "50°" },
  { key: "60°", label: "60°" },
  { key: "70°", label: "70°" },
  { key: "80°", label: "80°" },
  { key: "90°", label: "90°" },
  { key: "100°", label: "100°" },
  { key: "110°", label: "110°" },
  { key: "120°", label: "120°" },
  { key: "130°", label: "130°" },
  { key: "140°", label: "140°" },
  { key: "150°", label: "150°" },
  { key: "160°", label: "160°" },
  { key: "170°", label: "170°" },
  { key: "180°", label: "180°" },
  { key: "190°", label: "190°" },
  { key: "200°", label: "200°" },
  { key: "210°", label: "210°" },
  { key: "220°", label: "220°" },
  { key: "230°", label: "230°" },
  { key: "240°", label: "240°" },
  { key: "250°", label: "250°" },
  { key: "260°", label: "260°" },
  { key: "270°", label: "270°" },
  { key: "280°", label: "280°" },
  { key: "290°", label: "290°" },
  { key: "300°", label: "300°" },
  { key: "310°", label: "310°" },
  { key: "320°", label: "320°" },
  { key: "330°", label: "330°" },
  { key: "340°", label: "340°" },
  { key: "350°", label: "350°" },

]

async function getDataHTTP() {

  return await fetch('http://localhost:8000/5G_Dataset')
    .then(response => response.json())
    .then(data => data)
}

function postToMQTT( ){
  return fetch('http://localhost:8000/5G_Dataset/publish')
}
async function postHTTP() {
  const repeat_http = document.getElementById("repeat_http")
  const interval = document.getElementById("repeat_http_interval")
  const data_source = document.getElementById("data_source")
  const address_to_send = document.getElementById("where_to_send")

  console.log(document.getElementById("iotable"))


  try {
    if (address_to_send.value.trim() === '') {
      const url = data_source.value.trim() !== ''
      ? `http://localhost:8000/5G_Dataset/?data_source=${data_source.value}`
      : 'http://localhost:8000/5G_Dataset/'
      await fetch(url, { method: 'POST'})
    } else {
      try {
        const url = data_source.value.trim() !== ''
        ? `http://${address_to_send.value.trim()}/?data_source=${data_source.value}`
        : `http://${address_to_send.value.trim()}/5G_Dataset/`
        await fetch(url, { method: 'POST'})
      } catch (error) {
        alert(error)
      }

    }


  } catch (error) {
    alert(error)
  }

  if (repeat_http.checked) {
    if (interval.value.trim() === '') {
      alert('Please enter a valid interval')
      return
    }

    const delay = parseInt(interval.value)

    setTimeout(postHTTP, delay)
  }

}




</script>


<style scoped>
.title {
  text-align: center;
  margin-top: -3%;
}
</style>