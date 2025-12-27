<script setup>
import { useRouter } from 'vue-router'

import LayoutCard from '../components/LayoutCard.vue'

const router = useRouter()

function goToTasks() {
  router.push({ name: 'tasks' })
}
</script>

<template>
  <LayoutCard title="Dashboard">
    <p>Мини-приложение «Менеджер задач» на Vue 3 + FastAPI.</p>

    <template #footer>
      <button type="button" @click="goToTasks">Перейти к задачам</button>
    </template>
  </LayoutCard>
</template>
