<script setup>
const props = defineProps({
  task: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['delete', 'toggle', 'edit'])

function onDelete() {
  emit('delete', props.task.id)
}

function onToggle() {
  emit('toggle', props.task.id)
}

function onEdit() {
  emit('edit', props.task.id)
}
</script>

<template>
  <article class="task">
    <div class="task__main">
      <div class="task__title-row">
        <strong class="task__title" :class="{ done: task.completed }">{{ task.title }}</strong>
        <span v-if="task.important" class="task__badge">Важно</span>
      </div>

      <div class="task__meta">
        <span>Приоритет: {{ task.priority }}</span>
        <span>Категория: {{ task.category }}</span>
        <span>Статус: {{ task.completed ? 'выполнено' : 'не выполнено' }}</span>
      </div>

      <p v-if="task.description" class="task__desc">{{ task.description }}</p>
    </div>

    <div class="task__actions">
      <button type="button" @click="onEdit">Редактировать</button>
      <button type="button" @click="onToggle">Изменить статус</button>
      <button type="button" class="danger" @click="onDelete">Удалить</button>
    </div>
  </article>
</template>

<style scoped>
.task {
  display: flex;
  gap: 16px;
  justify-content: space-between;
  border: 1px solid rgba(128, 128, 128, 0.25);
  border-radius: 12px;
  padding: 12px;
}
.task__title-row {
  display: flex;
  gap: 10px;
  align-items: center;
}
.task__title.done {
  text-decoration: line-through;
  opacity: 0.7;
}
.task__meta {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  opacity: 0.9;
  font-size: 0.92rem;
  margin-top: 6px;
}
.task__desc {
  margin: 8px 0 0;
  opacity: 0.9;
}
.task__actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  align-items: start;
}
.danger {
  border-color: rgba(255, 0, 0, 0.35);
}
.task__badge {
  font-size: 0.8rem;
  border: 1px solid rgba(128, 128, 128, 0.25);
  padding: 2px 8px;
  border-radius: 999px;
}
</style>
