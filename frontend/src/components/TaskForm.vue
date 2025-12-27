<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'

const props = defineProps({
  initialValues: {
    type: Object,
    default: () => ({
      title: '',
      description: '',
      priority: 'medium',
      category: 'other',
      important: false,
      completed: false,
    }),
  },
  submitLabel: {
    type: String,
    default: 'Сохранить',
  },
})

const emit = defineEmits(['submit', 'cancel'])

const form = reactive({
  title: '',
  description: '',
  priority: 'medium',
  category: 'other',
  important: false,
  completed: false,
})

const touched = reactive({
  title: false,
})

watch(
  () => props.initialValues,
  (next) => {
    form.title = next?.title ?? ''
    form.description = next?.description ?? ''
    form.priority = next?.priority ?? 'medium'
    form.category = next?.category ?? 'other'
    form.important = Boolean(next?.important)
    form.completed = Boolean(next?.completed)
  },
  { immediate: true }
)

const errors = computed(() => {
  const e = {}
  if (!form.title || form.title.trim().length === 0) e.title = 'Введите заголовок'
  if (form.title && form.title.length > 120) e.title = 'Слишком длинный заголовок'
  return e
})

const isValid = computed(() => Object.keys(errors.value).length === 0)

function submit() {
  touched.title = true
  if (!isValid.value) return
  emit('submit', {
    title: form.title,
    description: form.description,
    priority: form.priority,
    category: form.category,
    important: form.important,
    completed: form.completed,
  })
}

function cancel() {
  emit('cancel')
}

const titleInput = ref(null)

onMounted(() => {
  titleInput.value?.focus?.()
})
</script>

<template>
  <form class="form" @submit.prevent="submit">
    <div class="field">
      <label class="label">Заголовок</label>
      <input
        ref="titleInput"
        v-model.trim="form.title"
        type="text"
        class="input"
        placeholder="Например: Сделать практическую"
        @blur="touched.title = true"
      />
      <p v-if="touched.title && errors.title" class="error">{{ errors.title }}</p>
    </div>

    <div class="field">
      <label class="label">Описание</label>
      <textarea
        v-model.lazy.trim="form.description"
        class="textarea"
        rows="4"
        placeholder="Что нужно сделать?"
      />
    </div>

    <div class="field">
      <label class="label">Приоритет</label>
      <select v-model="form.priority" class="select">
        <option value="low">Низкий</option>
        <option value="medium">Средний</option>
        <option value="high">Высокий</option>
      </select>
    </div>

    <div class="field">
      <label class="label">Категория</label>
      <div class="radio-row">
        <label><input v-model="form.category" type="radio" value="work" /> Работа</label>
        <label><input v-model="form.category" type="radio" value="study" /> Учёба</label>
        <label><input v-model="form.category" type="radio" value="home" /> Дом</label>
        <label><input v-model="form.category" type="radio" value="other" /> Другое</label>
      </div>
    </div>

    <div class="field">
      <label><input v-model="form.important" type="checkbox" /> Важно</label>
    </div>

    <div class="field">
      <label><input v-model="form.completed" type="checkbox" /> Выполнено</label>
    </div>

    <div class="actions">
      <button type="submit" :disabled="!isValid">{{ submitLabel }}</button>
      <button type="button" class="secondary" @click="cancel">Отмена</button>
    </div>
  </form>
</template>

<style scoped>
.form {
  display: grid;
  gap: 14px;
}
.field {
  display: grid;
  gap: 6px;
}
.label {
  font-weight: 600;
}
.input,
.textarea,
.select {
  width: 100%;
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid rgba(128, 128, 128, 0.25);
  background: transparent;
  color: inherit;
}
.radio-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  align-items: center;
}
.secondary {
  opacity: 0.9;
}
.error {
  color: #ff6b6b;
  margin: 0;
}
</style>
