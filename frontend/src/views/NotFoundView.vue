<script setup>
import LayoutCard from '../components/LayoutCard.vue'
</script>

<template>
  <LayoutCard>
    <template #header>
      <h2>404 — Страница не найдена</h2>
    </template>

    <p>Проверьте адрес или перейдите на главную.</p>

    <template #footer>
      <RouterLink :to="{ name: 'home' }">На главную</RouterLink>
    </template>
  </LayoutCard>
</template>
