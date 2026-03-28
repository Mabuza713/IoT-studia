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
  { path: '/RT_Dataset',   label: 'RT-IoT2022' },
  { path: '/5G_Dataset',   label: 'Indoor 5G CSI' },
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