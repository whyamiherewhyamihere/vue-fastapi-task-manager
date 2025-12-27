<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <header class="app-header">
    <nav class="nav">
      <RouterLink class="nav-link" :to="{ name: 'home' }">Главная</RouterLink>
      <RouterLink class="nav-link" :to="{ name: 'tasks' }">Задачи</RouterLink>
      <RouterLink class="nav-link" :to="{ name: 'task-new' }">Создать</RouterLink>
    </nav>
  </header>
</template>

<style scoped>
.app-header {
  padding: 12px 0;
  border-bottom: 1px solid rgba(128, 128, 128, 0.25);
}
.nav {
  display: flex;
  gap: 12px;
}
.nav-link {
  padding: 6px 10px;
  border-radius: 8px;
}
.nav-link.router-link-active {
  font-weight: 700;
  text-decoration: underline;
}
</style>
