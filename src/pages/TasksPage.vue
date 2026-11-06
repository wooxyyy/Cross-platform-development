<script setup>
import { ref, computed, nextTick } from 'vue'
import AppTabbar from '../components/AppTabbar.vue'
import TaskForm from '../components/TaskForm.vue'
import TaskCard from '../components/TaskCard.vue'
import TaskListControls from '../components/TaskListControls.vue'
import TaskCounter from '../components/TaskCounter.vue'
import TaskSelection from '../components/TaskSelection.vue'
import { taskState, setTaskStatus, setTaskPriority, addTask, updateTask, deleteTask } from '../store/tasks'
import '../css/task-components.css'
import '../css/task-form.css'
import '../css/task-list.css'
const searchQuery = ref('')
const formVisible = ref(false)
const editingId = ref(null)
const formAnchor = ref(null)
const feedback = ref('')
const editingTask = computed(() => taskState.tasks.find(task => task.id === editingId.value) ?? null)
async function openForm(id = null) {
  editingId.value = id
  formVisible.value = true
  feedback.value = ''
  await nextTick()
  formAnchor.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  formAnchor.value?.querySelector('input')?.focus({ preventScroll: true })
}
function cancelForm() { formVisible.value = false; editingId.value = null }
function saveTask(data) {
  const isEditing = editingId.value !== null
  const saved = isEditing ? updateTask({ id: editingId.value, ...data }) : addTask(data)
  if (!saved) { feedback.value = 'Не вдалося зберегти завдання. Перевірте дані форми.'; return }
  feedback.value = `Завдання «${saved.title}» ${isEditing ? 'оновлено' : 'створено'}.`
  cancelForm()
  resetFilters()
}
const sortOrder = ref('newest')
const selectedStatus = ref('all')
const selectedPriority = ref('all')
const onlyIncomplete = ref(false)
const priorityRank = { low: 0, medium: 1, high: 2 }
const statusRank = { progress: 0, todo: 1, done: 2 }
const filteredTasks = computed(() => {
  const term = searchQuery.value.trim().toLocaleLowerCase('uk-UA')
  const result = taskState.tasks.filter(task => (
    `${task.title} ${task.description ?? ''}`.toLocaleLowerCase('uk-UA').includes(term) &&
    (selectedStatus.value === 'all' || task.status === selectedStatus.value) &&
    (selectedPriority.value === 'all' || task.priority === selectedPriority.value) &&
    (!onlyIncomplete.value || task.status !== 'done')
  ))
  return result.sort((a, b) => {
    if (sortOrder.value === 'title') return a.title.localeCompare(b.title, 'uk-UA') || a.id - b.id
    if (sortOrder.value === 'status') return statusRank[a.status] - statusRank[b.status] || b.id - a.id
    if (sortOrder.value === 'priority') return priorityRank[b.priority] - priorityRank[a.priority] || b.id - a.id
    if (sortOrder.value === 'low-first') return priorityRank[a.priority] - priorityRank[b.priority] || a.id - b.id
    if (sortOrder.value === 'original') return a.id - b.id
    if (sortOrder.value === 'dueDate' || sortOrder.value === 'dueDate-desc') {
      if (!a.dueDate || !b.dueDate) return Number(!a.dueDate) - Number(!b.dueDate) || b.id - a.id
      const order = a.dueDate.localeCompare(b.dueDate)
      return (sortOrder.value === 'dueDate-desc' ? -order : order) || b.id - a.id
    }
    return b.id - a.id
  })
})
const completionPercent = computed(() => filteredTasks.value.length
  ? Math.round(filteredTasks.value.filter(task => task.status === 'done').length / filteredTasks.value.length * 100) : 0)
function resetFilters() {
  searchQuery.value = ''
  selectedStatus.value = 'all'
  selectedPriority.value = 'all'
  sortOrder.value = 'newest'
  onlyIncomplete.value = false
}
const deleteDialog = ref(null)
const deletingId = ref(null)
const deletingTask = computed(() => taskState.tasks.find(task => task.id === deletingId.value) ?? null)
async function handleDelete(id) {
  deletingId.value = id
  if (!deletingTask.value) return
  await nextTick()
  deleteDialog.value?.showModal()
}
function cancelDelete() {
  deleteDialog.value?.close()
  deletingId.value = null
}
function confirmDelete() {
  const task = deletingTask.value
  if (task && deleteTask(task.id)) {
    if (editingId.value === task.id) cancelForm()
    if (selectedTaskId.value === task.id) selectedTaskId.value = null
    feedback.value = `Завдання «${task.title}» видалено.`
  }
  cancelDelete()
}
const selectedTaskId = ref(null)
const selectedTask = computed(() => taskState.tasks.find((task) => task.id === selectedTaskId.value) || null)
function handleTaskSelect({ id }) { selectedTaskId.value = id }
function handleStatusChange(payload) { setTaskStatus(payload) }
function handlePriorityChange(payload) { setTaskPriority(payload) }
</script>
<template>
<f7-page name="tasks" class="tf3-page">
<f7-navbar title="Мої завдання" />
<div class="tf3-container">
<section class="tf3-hero">
<div class="tf3-eyebrow">TASKFLOW / TASK MANAGER</div>
<h1>Мої завдання</h1>
<p>Створюйте, редагуйте, знаходьте, сортуйте та видаляйте завдання.</p>
<button type="button" class="tf4-new-task" @click="openForm()">+ Додати завдання</button>
</section>
<p v-if="feedback" class="tf4-feedback" role="status">{{ feedback }}</p>
<section v-if="formVisible" ref="formAnchor" class="tf4-form-section">
<TaskForm :key="editingId ?? 'new'" :task="editingTask" @save="saveTask" @cancel="cancelForm" />
</section>
<TaskListControls v-model:search="searchQuery" v-model:status="selectedStatus"
  v-model:priority="selectedPriority" v-model:sort="sortOrder" v-model:incomplete="onlyIncomplete"
  @reset="resetFilters" />
<TaskSelection :task="selectedTask" @close="selectedTaskId = null" />
<section class="tf3-section">
<div class="tf3-section-heading">
<div><div class="tf3-eyebrow">TASK LIST</div><h2>Список завдань</h2></div>
<div class="tf5-summary" aria-live="polite"><TaskCounter :count="filteredTasks.length" label="Показано" />
<span>із {{ taskState.tasks.length }} · Виконано у вибірці: {{ completionPercent }}%</span></div>
</div>
<div v-if="filteredTasks.length" class="tf3-task-grid">
<TaskCard v-for="task in filteredTasks" :key="task.id" :task="task" :editable="true" @edit="openForm" @delete="handleDelete"
@status-change="handleStatusChange"
@priority-change="handlePriorityChange"
@task-select="handleTaskSelect" />
</div>
<div v-else-if="!taskState.tasks.length" class="tf5-empty">
<h3>Список завдань порожній</h3><p>Усі завдання видалено. Створіть нове завдання, щоб продовжити.</p>
<button type="button" class="tf5-btn" @click="openForm()">Створити перше завдання</button>
</div>
<div v-else class="tf5-empty"><p>За поточними умовами завдань не знайдено.</p>
<button type="button" class="tf5-btn" @click="resetFilters">Показати всі завдання</button></div>
</section>
</div>
<dialog ref="deleteDialog" class="tf5-dialog" aria-labelledby="delete-heading" aria-describedby="delete-description" @cancel.prevent="cancelDelete">
<h2 id="delete-heading">Видалити завдання?</h2>
<p id="delete-description">Видалити «{{ deletingTask?.title }}»? Завдання буде вилучено з поточного списку.</p>
<div class="tf5-actions"><button type="button" class="tf5-btn" autofocus @click="cancelDelete">Скасувати</button>
<button type="button" class="tf5-btn tf5-danger" @click="confirmDelete">Видалити завдання</button></div>
</dialog>
<template #fixed><AppTabbar active="tasks" /></template>
</f7-page>
</template>