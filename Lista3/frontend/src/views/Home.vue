<template>
  <navbar></navbar>
  <main class="main-content">
    <router-view />
  </main>
</template>

<script setup>
import Navbar from "../components/navbar.vue";

</script>

<style>
  .main-content {
    margin-left: 200px;
    padding: 40px;
    min-height: 100vh;
    background-color: #f4f4f4;
  }
</style>