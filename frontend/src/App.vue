<script setup>
import { RouterView } from 'vue-router'

import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
</script>

<template>
  <div class="app">
    <AppHeader />

    <main class="app__main">
      <RouterView />
    </main>

    <AppFooter />
  </div>
</template>

<style scoped>
.app {
  display: grid;
  gap: 18px;
}
.app__main {
  min-height: 60vh;
}
</style>
