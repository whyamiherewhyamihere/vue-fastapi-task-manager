<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import LayoutCard from '../../components/LayoutCard.vue'
import TaskForm from '../../components/TaskForm.vue'

import { getTask, updateTask } from '../../api/tasks'

const props = defineProps({
  id: {
    type: [String, Number],
    required: true,
  },
})

const router = useRouter()

const loading = ref(false)
const saving = ref(false)
const error = ref('')

const task = ref(null)

async function load() {
  loading.value = true
  error.value = ''
  try {
    task.value = await getTask(props.id)
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  } finally {
    loading.value = false
  }
}

async function onSubmit(payload) {
  saving.value = true
  error.value = ''
  try {
    await updateTask(props.id, payload)
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

onMounted(() => {
  load()
})
</script>

<template>
  <LayoutCard title="Редактирование задачи">
    <p v-if="error" class="error">Ошибка: {{ error }}</p>
    <p v-if="loading">Загрузка...</p>
    <p v-else-if="saving">Сохранение...</p>

    <TaskForm
      v-else
      :initial-values="task"
      submit-label="Сохранить"
      @submit="onSubmit"
      @cancel="onCancel"
    />
  </LayoutCard>
</template>

<style scoped>
.error {
  color: #ff6b6b;
}
</style>
