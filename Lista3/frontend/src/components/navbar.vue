<template>
  <div class="nav-container">
    <h1>IoT-studia</h1>
    <nav class="navbar">
        <ul class="navbar-nav">
          <div class="navbar-button">
            <li v-for="item in navItems" :key="item.path" class="nav-links">
              <router-link :to="item.path" >{{ item.label }}</router-link>
            </li>
          </div>

        </ul>

    </nav>
  </div>

</template>

<script setup>

const navItems = [
    { path: '/GOV',   label: 'GOV DATASET' },
    { path: '/ETDataset',   label: 'ETDataset' },
    { path: '/SOLAR',   label: 'Solar' },
    { path: '/ENERGY',   label: 'Energy' },
    { path: '/NEWYORK',   label: 'New York' },
    { path: '/Reciever',   label: 'Reciever' },


]

</script>

<style scoped>
ul{
  list-style-type: none;
}
.nav-container {
  position: fixed;
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
  align-items: start;

  padding: 20px;
  background-color: #b1acac;
  color: #fff;

  height: 100vh;
  width: 200px;
}

</style>