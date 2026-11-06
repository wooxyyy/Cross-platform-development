<script setup>
import { computed, nextTick, reactive, ref } from 'vue'
import { categoryLabels, validateTaskData } from '../store/tasks'
const props = defineProps({ task: { type: Object, default: null } })
const emit = defineEmits(['save', 'cancel'])
const defaults = () => ({ title: '', description: '', status: 'todo', priority: 'medium', dueDate: '', category: 'study' })
const form = reactive({ ...defaults(), ...props.task })
const showErrors = ref(false)
const formElement = ref(null)
const isEditing = computed(() => props.task !== null)
const errors = computed(() => validateTaskData(form, props.task))
const statusLabels = { todo: 'Заплановано', progress: 'У роботі', done: 'Виконано' }
const priorityLabels = { low: 'Низький', medium: 'Середній', high: 'Високий' }
async function submitForm() {
  showErrors.value = true
  if (Object.keys(errors.value).length) {
    await nextTick()
    formElement.value?.querySelector('[aria-invalid="true"]')?.focus()
    return
  }
  emit('save', { title: form.title.trim(), description: form.description.trim(),
    status: form.status, priority: form.priority, dueDate: form.dueDate, category: form.category })
}
function clearForm() {
  Object.assign(form, defaults())
  showErrors.value = false
  formElement.value?.querySelector('input')?.focus()
}
</script>
<template>
<div class="tf4-form-panel">
  <div class="tf4-form-heading">
    <div><div class="tf3-eyebrow">TASKFLOW / FORM</div>
    <h2>{{ isEditing ? 'Редагування завдання' : 'Нове завдання' }}</h2></div>
    <button type="button" class="tf4-cancel" @click="emit('cancel')">Закрити</button>
  </div>
  <p class="tf4-hint">Поля з <span class="tf4-required">*</span> обов’язкові.</p>
  <form ref="formElement" class="tf4-form" novalidate @submit.prevent="submitForm">
    <div class="tf4-field tf4-field--wide">
      <label for="tf4-title">Назва завдання <span class="tf4-required">*</span></label>
      <input id="tf4-title" v-model.trim="form.title" type="text" maxlength="80" required
        placeholder="Наприклад: Підготувати звіт" :aria-invalid="showErrors && !!errors.title"
        :aria-describedby="`tf4-title-hint${showErrors && errors.title ? ' tf4-title-error' : ''}`" />
      <small id="tf4-title-hint">Від 3 до 80 символів. Залишилося: {{ 80 - form.title.length }}</small>
      <p v-if="showErrors && errors.title" id="tf4-title-error" class="tf4-error">{{ errors.title }}</p>
    </div>
    <div class="tf4-field tf4-field--wide">
      <label for="tf4-description">Опис</label>
      <textarea id="tf4-description" v-model.trim="form.description" rows="3" maxlength="300"
        placeholder="Що потрібно зробити?" :aria-invalid="showErrors && !!errors.description"
        :aria-describedby="`tf4-description-hint${showErrors && errors.description ? ' tf4-description-error' : ''}`"></textarea>
      <small id="tf4-description-hint">Необов’язкове поле. Залишилося: {{ 300 - form.description.length }}</small>
      <p v-if="showErrors && errors.description" id="tf4-description-error" class="tf4-error">{{ errors.description }}</p>
    </div>
    <div v-for="field in ['status', 'priority', 'category']" :key="field" class="tf4-field">
      <label :for="`tf4-${field}`">{{ { status: 'Статус', priority: 'Пріоритет', category: 'Категорія' }[field] }} <span class="tf4-required">*</span></label>
      <select :id="`tf4-${field}`" v-model="form[field]" required :aria-invalid="showErrors && !!errors[field]"
        :aria-describedby="showErrors && errors[field] ? `tf4-${field}-error` : undefined">
        <option v-for="(label, value) in ({ status: statusLabels, priority: priorityLabels, category: categoryLabels }[field])" :key="value" :value="value">{{ label }}</option>
      </select>
      <p v-if="showErrors && errors[field]" :id="`tf4-${field}-error`" class="tf4-error">{{ errors[field] }}</p>
    </div>
    <div class="tf4-field">
      <label for="tf4-date">Дата завершення <span class="tf4-required">*</span></label>
      <input id="tf4-date" v-model="form.dueDate" type="date" required :aria-invalid="showErrors && !!errors.dueDate"
        :aria-describedby="`tf4-date-hint${showErrors && errors.dueDate ? ' tf4-date-error' : ''}`" />
      <small id="tf4-date-hint">{{ isEditing ? 'Можна залишити попередню дату. Нова дата має бути сьогоднішньою або майбутньою.' : 'Сьогоднішня або майбутня дата.' }}</small>
      <p v-if="showErrors && errors.dueDate" id="tf4-date-error" class="tf4-error">{{ errors.dueDate }}</p>
    </div>
    <div class="tf4-preview tf4-field--wide" aria-live="polite">
      <strong>Попередній перегляд</strong>
      <h3>{{ form.title || 'Назва нового завдання' }}</h3>
      <p>{{ form.description || 'Опис завдання' }}</p>
      <span>{{ statusLabels[form.status] }} · {{ priorityLabels[form.priority] }} · {{ categoryLabels[form.category] }}</span>
      <p>Термін: {{ form.dueDate || 'Не вказано' }}</p>
    </div>
    <div class="tf4-actions tf4-field--wide">
      <button type="submit" class="tf4-save">{{ isEditing ? 'Зберегти зміни' : 'Створити завдання' }}</button>
      <button type="button" class="tf4-cancel" @click="emit('cancel')">Скасувати</button>
      <button v-if="!isEditing" type="button" class="tf4-cancel" @click="clearForm">Очистити форму</button>
    </div>
  </form>
</div>
</template>
