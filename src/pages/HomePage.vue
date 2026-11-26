<script setup>
import { ref, computed } from 'vue'
import AppTabbar from '../components/AppTabbar.vue'
import TaskCard from '../components/TaskCard.vue'
import TaskCounter from '../components/TaskCounter.vue'
import TaskSelection from '../components/TaskSelection.vue'
import { storeToRefs } from 'pinia'
import { useTasksStore } from '../store/tasks'
import { useProjectsStore } from '../store/projects'
import '../css/task-components.css'
import '../css/task-list.css'
const taskStore = useTasksStore()
const projectStore = useProjectsStore()
const { tasks, totalTasks, completedTasks, progressTasks, plannedTasks, completionPercent, activeTasks } = storeToRefs(taskStore)
const { projects, projectStats } = storeToRefs(projectStore)
const selectedTaskId = ref(null)
const selectedTask = computed(() => tasks.value.find((task) => task.id === selectedTaskId.value) || null)
function handleTaskSelect({ id }) { selectedTaskId.value = id }
function handleStatusChange(payload) { taskStore.setTaskStatus(payload) }
function handlePriorityChange(payload) { taskStore.setTaskPriority(payload) }
</script>
<template>
<f7-page name="home" class="tf3-page">
<f7-navbar title="TaskFlow">
<f7-nav-right><f7-link href="/about/">Про застосунок</f7-link></f7-nav-right>
</f7-navbar>
<div class="tf3-container">
<section class="tf3-hero">
<div class="tf3-eyebrow">TASKFLOW / DASHBOARD</div>
<h1>Панель керування</h1>
<p>Контролюйте виконання завдань та їхні пріоритети.</p>
</section>
<section class="tf3-stat-grid">
<div class="tf3-stat"><span class="tf3-stat-label">Усього завдань</span>
<strong>{{ totalTasks }}</strong></div>
<div class="tf3-stat"><span class="tf3-stat-label">У роботі</span>
<strong>{{ progressTasks }}</strong></div>
<div class="tf3-stat"><span class="tf3-stat-label">Виконано</span>
<strong>{{ completedTasks }}</strong></div>
<div class="tf3-stat"><span class="tf3-stat-label">Заплановано</span>
<strong>{{ plannedTasks }}</strong></div>
</section>
<section class="tf3-completion" aria-label="Прогрес виконання">
<TaskCounter :count="totalTasks" label="Усього завдань" />
<p>Виконано: <strong>{{ completionPercent }}%</strong></p>
<progress :value="completedTasks" :max="totalTasks || 1" :aria-label="`Виконано ${completionPercent}% завдань`" />
</section>
<section class="tf5-panel" aria-label="Статистика за проєктами">
<h2>Мої проєкти</h2>
<ul class="tf6-project-list">
<li v-for="project in projects" :key="project.id" class="tf6-project-pill">
{{ project.title }} · Невиконано: {{ projectStats[project.id].incomplete }} · Виконано: {{ projectStats[project.id].percent }} %
</li>
</ul>
</section>
<TaskSelection :task="selectedTask" @close="selectedTaskId = null" />
<section class="tf3-section">
<div class="tf3-section-heading">
<div><div class="tf3-eyebrow">PRIORITY TASKS</div>
<h2>Актуальні завдання</h2></div>
<f7-button href="/tasks/" outline small>Переглянути всі</f7-button>
</div>
<div v-if="activeTasks.length" class="tf3-task-grid">
<TaskCard v-for="task in activeTasks" :key="task.id" :task="task" :project-title="projectStore.projectTitle(task.projectId)"
@status-change="handleStatusChange"
@priority-change="handlePriorityChange"
@task-select="handleTaskSelect" />
</div>

<div v-else class="tf3-empty">Наразі всі завдання виконані.</div>
</section>
</div>
<template #fixed><AppTabbar active="home" /></template>
</f7-page>
</template>