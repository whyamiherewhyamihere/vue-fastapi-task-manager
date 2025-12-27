<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import LayoutCard from '../../components/LayoutCard.vue'
import TaskForm from '../../components/TaskForm.vue'

import { createTask } from '../../api/tasks'

const router = useRouter()

const saving = ref(false)
const error = ref('')

async function onSubmit(payload) {
  saving.value = true
  error.value = ''
  try {
    await createTask(payload)
    router.push({ name: 'tasks' })
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  } finally {
    saving.value = false
  }
}

function onCancel() {
  router.push({ name: 'tasks' })
}
</script>

<template>
  <LayoutCard title="Создание задачи">
    <p v-if="error" class="error">Ошибка: {{ error }}</p>
    <p v-if="saving">Сохранение...</p>

    <TaskForm v-else submit-label="Создать" @submit="onSubmit" @cancel="onCancel" />
  </LayoutCard>
</template>

<style scoped>
.error {
  color: #ff6b6b;
}
</style>
