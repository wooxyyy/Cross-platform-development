import { defineStore } from 'pinia'
import { useProjectsStore } from './projects.js'
import initialTasks from '../data/tasks.js'

export const allowedStatuses = ['todo', 'progress', 'done']
export const allowedPriorities = ['low', 'medium', 'high']
export const categoryLabels = { study: 'Навчання', work: 'Робота', personal: 'Особисте' }

export function todayDate() {
  const now = new Date()
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`
}
export function validDate(value) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false
  const date = new Date(`${value}T12:00:00`)
  return !Number.isNaN(date.getTime()) &&
    `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}` === value
}
export function validateTaskData(data, original = null, tasks = []) {
  const errors = {}
  const title = typeof data?.title === 'string' ? data.title.trim() : ''
  const description = typeof data?.description === 'string' ? data.description.trim() : ''
  if (!title) errors.title = 'Вкажіть назву завдання.'
  else if (title.length < 3) errors.title = 'Назва має містити щонайменше 3 символи.'
  else if (title.length > 80) errors.title = 'Максимальна довжина - 80 символів.'
  else if (!original && tasks.some((task) => task.title.trim().toLocaleLowerCase('uk') === title.toLocaleLowerCase('uk'))) {
    errors.title = 'Завдання з такою назвою вже існує.'
  }
  if (data?.description != null && typeof data.description !== 'string') errors.description = 'Опис має бути текстом.'
  else if (description.length > 500) errors.description = 'Опис не повинен перевищувати 500 символів.'
  if (!allowedStatuses.includes(data?.status)) errors.status = 'Оберіть коректний статус.'
  if (!allowedPriorities.includes(data?.priority)) errors.priority = 'Оберіть коректний пріоритет.'
  if (!Object.hasOwn(categoryLabels, data?.category ?? 'study')) errors.category = 'Оберіть коректну категорію.'
  if (data?.dueDate !== '' && !validDate(data?.dueDate)) errors.dueDate = 'Укажіть коректну дату завершення.'
  else if (data?.dueDate && data.dueDate < todayDate() && data.dueDate !== original?.dueDate) {
    errors.dueDate = 'Нова дата завершення не може бути минулою.'
  }
  return errors
}
function normalizeTaskData(data, original = null, tasks = []) {
  if (Object.keys(validateTaskData(data, original, tasks)).length) return null
  return { title: data.title.trim(), description: (data.description ?? '').trim(),
    status: data.status, priority: data.priority, dueDate: data.dueDate, category: data.category ?? 'study',
    projectId: useProjectsStore().projects.some(project => project.id === data.projectId)
      ? data.projectId : original?.projectId ?? 'general' }
}
const priorityRank = { low: 0, medium: 1, high: 2 }
const statusRank = { progress: 0, todo: 1, done: 2 }

const initialFilters = () => ({
  searchText: '',
  selectedStatus: 'all',
  selectedPriority: 'all',
  selectedProject: 'all',
  sortOrder: 'newest',
  onlyIncomplete: false,
  onlyWithoutDueDate: false,
})

export const useTasksStore = defineStore('tasks', {
  state: () => ({
    tasks: initialTasks.map(task => ({ ...task, projectId: task.projectId ?? 'general' })),
    ...initialFilters(),
  }),
  getters: {
    totalTasks: state => state.tasks.length,
    completedTasks: state => state.tasks.filter(task => task.status === 'done').length,
    progressTasks: state => state.tasks.filter(task => task.status === 'progress').length,
    plannedTasks: state => state.tasks.filter(task => task.status === 'todo').length,
    completionPercent() {
      return this.totalTasks ? Math.round(this.completedTasks / this.totalTasks * 100) : 0
    },
    activeTasks: state => state.tasks.filter(task => task.status !== 'done')
      .sort((a, b) => priorityRank[b.priority] - priorityRank[a.priority] || b.id - a.id)
      .slice(0, 3),
    visibleTasks: state => {
        const term = state.searchText.trim().toLocaleLowerCase('uk-UA')
        const result = state.tasks.filter(task => (
          `${task.title} ${task.description ?? ''}`.toLocaleLowerCase('uk-UA').includes(term) &&
          (state.selectedStatus === 'all' || task.status === state.selectedStatus) &&
          (state.selectedPriority === 'all' || task.priority === state.selectedPriority) &&
          (state.selectedProject === 'all' || task.projectId === state.selectedProject) &&
          (!state.onlyWithoutDueDate || !task.dueDate) &&
          (!state.onlyIncomplete || task.status !== 'done')
        ))
        return result.sort((a, b) => {
          if (state.sortOrder === 'title') return a.title.localeCompare(b.title, 'uk-UA') || a.id - b.id
          if (state.sortOrder === 'status') return statusRank[a.status] - statusRank[b.status] || b.id - a.id
          if (state.sortOrder === 'priority') return priorityRank[b.priority] - priorityRank[a.priority] || b.id - a.id
          if (state.sortOrder === 'low-first') return priorityRank[a.priority] - priorityRank[b.priority] || a.id - b.id
          if (state.sortOrder === 'original') return a.id - b.id
          if (state.sortOrder === 'dueDate' || state.sortOrder === 'dueDate-desc') {
            if (!a.dueDate || !b.dueDate) return Number(!a.dueDate) - Number(!b.dueDate) || b.id - a.id
            const order = a.dueDate.localeCompare(b.dueDate)
            return (state.sortOrder === 'dueDate-desc' ? -order : order) || b.id - a.id
          }
          return b.id - a.id
        })
    },
  },
  actions: {
    addTask(data) {
      const normalized = normalizeTaskData(data, null, this.tasks)
      if (!normalized) return null
      const id = this.tasks.reduce((maxId, task) => Math.max(maxId, task.id), 0) + 1
      const task = { id, ...normalized }
      this.tasks.unshift(task)
      return task
    },
    updateTask(data) {
      const task = this.tasks.find((item) => item.id === data?.id)
      if (!task) return null
      const normalized = normalizeTaskData(data, task, this.tasks)
      if (!normalized) return null
      Object.assign(task, normalized)
      return task
    },
    setTaskStatus({ id, status }) {
      if (!allowedStatuses.includes(status)) return
      const task = this.tasks.find((item) => item.id === id)
      if (task) task.status = status
    },
    setTaskPriority({ id, priority }) {
      if (!allowedPriorities.includes(priority)) return
      const task = this.tasks.find((item) => item.id === id)
      if (task) task.priority = priority
    },

    deleteTask(id) {
      const index = this.tasks.findIndex((task) => task.id === Number(id))
      if (index === -1) return false
      this.tasks.splice(index, 1)
      return true
    },

    resetFilters() {
      this.$patch(initialFilters())
    },
    startProjectTasks(projectId) {
      if (!useProjectsStore().projects.some(project => project.id === projectId)) return 0
      const tasks = this.tasks.filter(task => task.projectId === projectId && task.status !== 'progress')
      this.$patch(() => {
        for (const task of tasks) task.status = 'progress'
      })
      return tasks.length
    },
  },
})
