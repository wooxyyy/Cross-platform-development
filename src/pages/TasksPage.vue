<script setup>
import { ref, computed, nextTick } from 'vue'
import AppTabbar from '../components/AppTabbar.vue'
import TaskForm from '../components/TaskForm.vue'
import TaskCard from '../components/TaskCard.vue'
import TaskListControls from '../components/TaskListControls.vue'
import TaskCounter from '../components/TaskCounter.vue'
import TaskSelection from '../components/TaskSelection.vue'
import { storeToRefs } from 'pinia'
import { useTasksStore } from '../store/tasks'
import { useProjectsStore } from '../store/projects'
import '../css/task-components.css'
import '../css/task-form.css'
import '../css/task-list.css'
const taskStore = useTasksStore()
const projectStore = useProjectsStore()
const {
  tasks, totalTasks, searchText, selectedStatus, selectedPriority, selectedProject,
  sortOrder, onlyIncomplete, onlyWithoutDueDate, visibleTasks: filteredTasks,
} = storeToRefs(taskStore)
const { projects, projectStats } = storeToRefs(projectStore)
const projectName = ref('')
const projectError = ref('')
function addProject() {
  const project = projectStore.addProject(projectName.value)
  projectError.value = project ? '' : 'Введіть унікальну назву від 3 до 40 символів.'
  if (project) projectName.value = ''
}

const bulkDialog = ref(null)
const bulkProjectId = ref(null)
function openBulkDialog() {
  if (selectedProject.value === 'all') return
  bulkProjectId.value = selectedProject.value
  bulkDialog.value?.showModal()
}
function closeBulkDialog() {
  bulkDialog.value?.close()
  bulkProjectId.value = null
}
function confirmBulk() {
  const changed = taskStore.startProjectTasks(bulkProjectId.value)
  feedback.value = `Переведено в роботу завдань: ${changed}.`
  closeBulkDialog()
}
const formVisible = ref(false)
const editingId = ref(null)
const formAnchor = ref(null)
const feedback = ref('')
const editingTask = computed(() => tasks.value.find(task => task.id === editingId.value) ?? null)
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
  const saved = isEditing ? taskStore.updateTask({ id: editingId.value, ...data }) : taskStore.addTask(data)
  if (!saved) { feedback.value = 'Не вдалося зберегти завдання. Перевірте дані форми.'; return }
  feedback.value = `Завдання «${saved.title}» ${isEditing ? 'оновлено' : 'створено'}.`
  cancelForm()
  taskStore.resetFilters()
}
const completionPercent = computed(() => filteredTasks.value.length
  ? Math.round(filteredTasks.value.filter(task => task.status === 'done').length / filteredTasks.value.length * 100) : 0)
const deleteDialog = ref(null)
const deletingId = ref(null)
const deletingTask = computed(() => tasks.value.find(task => task.id === deletingId.value) ?? null)
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
  if (task && taskStore.deleteTask(task.id)) {
    if (editingId.value === task.id) cancelForm()
    if (selectedTaskId.value === task.id) selectedTaskId.value = null
    feedback.value = `Завдання «${task.title}» видалено.`
  }
  cancelDelete()
}
const selectedTaskId = ref(null)
const selectedTask = computed(() => tasks.value.find((task) => task.id === selectedTaskId.value) || null)
function handleTaskSelect({ id }) { selectedTaskId.value = id }
function handleStatusChange(payload) { taskStore.setTaskStatus(payload) }
function handlePriorityChange(payload) { taskStore.setTaskPriority(payload) }
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
<TaskForm :tasks="tasks" :projects="projects" :key="editingId ?? 'new'" :task="editingTask" @save="saveTask" @cancel="cancelForm" />
</section>
<section class="tf5-panel" aria-label="Мої проєкти">
<h2>Мої проєкти</h2>
<ul class="tf6-project-list">
<li v-for="project in projects" :key="project.id" class="tf6-project-pill">
{{ project.title }} <strong>{{ projectStats[project.id].total }}</strong> · Виконано: {{ projectStats[project.id].percent }} %
</li>
</ul>
<form class="tf6-project-form" @submit.prevent="addProject">
<label for="project-name">Назва нового проєкту
<input id="project-name" v-model="projectName" maxlength="40" />
</label>
<button type="submit" class="tf5-btn tf5-btn--primary">Додати проєкт</button>
</form>
<p v-if="projectError" class="tf5-error" role="alert">{{ projectError }}</p>
</section>
<TaskListControls :projects="projects" v-model:project="selectedProject"
  v-model:without-due-date="onlyWithoutDueDate" v-model:search="searchText" v-model:status="selectedStatus"
  v-model:priority="selectedPriority" v-model:sort="sortOrder" v-model:incomplete="onlyIncomplete"
  @reset="taskStore.resetFilters()" />
<button v-if="selectedProject !== 'all'" type="button" class="tf5-btn" @click="openBulkDialog">
  Взяти в роботу всі завдання проєкту
</button>
<TaskSelection :task="selectedTask" @close="selectedTaskId = null" />
<section class="tf3-section">
<div class="tf3-section-heading">
<div><div class="tf3-eyebrow">TASK LIST</div><h2>Список завдань</h2></div>
<div class="tf5-summary" aria-live="polite"><TaskCounter :count="filteredTasks.length" label="Показано" />
<span>із {{ totalTasks }} · Виконано у вибірці: {{ completionPercent }}%</span></div>
</div>
<div v-if="filteredTasks.length" class="tf3-task-grid">
<TaskCard v-for="task in filteredTasks" :key="task.id" :task="task" :project-title="projectStore.projectTitle(task.projectId)" :editable="true" @edit="openForm" @delete="handleDelete"
@status-change="handleStatusChange"
@priority-change="handlePriorityChange"
@task-select="handleTaskSelect" />
</div>
<div v-else-if="!totalTasks" class="tf5-empty">
<h3>Список завдань порожній</h3><p>Усі завдання видалено. Створіть нове завдання, щоб продовжити.</p>
<button type="button" class="tf5-btn" @click="openForm()">Створити перше завдання</button>
</div>
<div v-else class="tf5-empty"><p>За поточними умовами завдань не знайдено.</p>
<button type="button" class="tf5-btn" @click="taskStore.resetFilters()">Показати всі завдання</button></div>
</section>
</div>
<dialog ref="bulkDialog" class="tf5-dialog" aria-labelledby="bulk-heading" @cancel.prevent="closeBulkDialog">
<h2 id="bulk-heading">Взяти проєкт у роботу?</h2>
<p>Усі завдання проєкту «{{ projectStore.projectTitle(bulkProjectId) }}» матимуть статус «У роботі».</p>
<div class="tf5-actions">
<button type="button" class="tf5-btn" autofocus @click="closeBulkDialog">Скасувати</button>
<button type="button" class="tf5-btn tf5-btn--primary" @click="confirmBulk">Підтвердити</button>
</div>
</dialog>
<dialog ref="deleteDialog" class="tf5-dialog" aria-labelledby="delete-heading" aria-describedby="delete-description" @cancel.prevent="cancelDelete">
<h2 id="delete-heading">Видалити завдання?</h2>
<p id="delete-description">Видалити «{{ deletingTask?.title }}»? Завдання буде вилучено з поточного списку.</p>
<div class="tf5-actions"><button type="button" class="tf5-btn" autofocus @click="cancelDelete">Скасувати</button>
<button type="button" class="tf5-btn tf5-danger" @click="confirmDelete">Видалити завдання</button></div>
</dialog>
<template #fixed><AppTabbar active="tasks" /></template>
</f7-page>
</template>