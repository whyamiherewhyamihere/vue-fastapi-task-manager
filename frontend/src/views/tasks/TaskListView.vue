<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import LayoutCard from '../../components/LayoutCard.vue'
import TaskList from '../../components/TaskList.vue'
import TaskItem from '../../components/TaskItem.vue'

import { deleteTask, getTasks, updateTask } from '../../api/tasks'

const route = useRoute()
const router = useRouter()

const tasks = ref([])
const loading = ref(false)
const error = ref('')

const statusFilter = ref('all')
const sortBy = ref('created_at')

function parseQuery() {
  const qStatus = route.query.status
  const qSort = route.query.sort

  if (qStatus === 'completed' || qStatus === 'active' || qStatus === 'all') {
    statusFilter.value = qStatus
  }
  if (qSort === 'created_at' || qSort === 'alpha') {
    sortBy.value = qSort
  }
}

watch(
  () => route.query,
  () => parseQuery(),
  { immediate: true }
)

watch(
  [statusFilter, sortBy],
  ([s, so]) => {
    const nextQuery = { ...route.query, status: s, sort: so }
    const sameStatus = String(route.query.status ?? '') === String(s)
    const sameSort = String(route.query.sort ?? '') === String(so)
    if (sameStatus && sameSort) return
    router.replace({ query: nextQuery })
  },
  { flush: 'post' }
)

const filteredTasks = computed(() => {
  if (statusFilter.value === 'completed') return tasks.value.filter((t) => t.completed)
  if (statusFilter.value === 'active') return tasks.value.filter((t) => !t.completed)
  return tasks.value
})

const sortedTasks = computed(() => {
  const copy = [...filteredTasks.value]
  if (sortBy.value === 'alpha') {
    copy.sort((a, b) => String(a.title).localeCompare(String(b.title)))
    return copy
  }

  copy.sort((a, b) => {
    const da = new Date(a.created_at).getTime()
    const db = new Date(b.created_at).getTime()
    return db - da
  })
  return copy
})

async function load() {
  loading.value = true
  error.value = ''
  try {
    tasks.value = await getTasks()
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  } finally {
    loading.value = false
  }
}

async function onDelete(id) {
  if (!confirm('Удалить задачу?')) return
  try {
    await deleteTask(id)
    await load()
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  }
}

async function onToggle(id) {
  const current = tasks.value.find((t) => t.id === id)
  if (!current) return

  try {
    await updateTask(id, { ...current, completed: !current.completed })
    await load()
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  }
}

function onEdit(id) {
  router.push({ name: 'task-edit', params: { id } })
}

onMounted(() => {
  load()
})
</script>

<template>
  <LayoutCard title="Список задач">
    <template #header>
      <div class="header-row">
        <h2 style="margin: 0">Список задач</h2>
        <RouterLink :to="{ name: 'task-new' }">Создать задачу</RouterLink>
      </div>

      <div class="controls">
        <label>
          Статус
          <select v-model="statusFilter" class="select">
            <option value="all">Все</option>
            <option value="completed">Выполненные</option>
            <option value="active">Невыполненные</option>
          </select>
        </label>

        <label>
          Сортировка
          <select v-model="sortBy" class="select">
            <option value="created_at">По дате добавления</option>
            <option value="alpha">По алфавиту</option>
          </select>
        </label>
      </div>
    </template>

    <p v-if="loading">Загрузка...</p>
    <p v-else-if="error" class="error">Ошибка: {{ error }}</p>

    <TaskList
      v-else
      :tasks="sortedTasks"
      @delete="onDelete"
      @toggle="onToggle"
      @edit="onEdit"
    >
      <template #item="{ task }">
        <TaskItem :task="task" @delete="onDelete" @toggle="onToggle" @edit="onEdit" />
      </template>
    </TaskList>

    <template #footer>
      <button type="button" class="secondary" @click="load">Обновить</button>
    </template>
  </LayoutCard>
</template>

<style scoped>
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 12px;
}
.controls {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 12px;
}
.select {
  margin-left: 8px;
}
.error {
  color: #ff6b6b;
}
.secondary {
  opacity: 0.9;
}
</style>
