<script setup>
import TaskItem from './TaskItem.vue'

defineProps({
  tasks: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['delete', 'toggle', 'edit'])
</script>

<template>
  <div>
    <p v-if="tasks.length === 0">Список пуст. Создайте первую задачу.</p>

    <ul v-else class="task-list">
      <li v-for="task in tasks" :key="task.id" class="task-list__item">
        <slot name="item" :task="task">
          <TaskItem
            :task="task"
            @delete="(id) => emit('delete', id)"
            @toggle="(id) => emit('toggle', id)"
            @edit="(id) => emit('edit', id)"
          />
        </slot>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.task-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 12px;
}
.task-list__item {
  margin: 0;
}
</style>
