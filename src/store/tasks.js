import { reactive } from 'vue'
import initialTasks from '../data/tasks'

export const allowedStatuses = ['todo', 'progress', 'done']
export const allowedPriorities = ['low', 'medium', 'high']
export const categoryLabels = { study: 'Навчання', work: 'Робота', personal: 'Особисте' }
export const taskState = reactive({ tasks: initialTasks.map((task) => ({ ...task })) })

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
export function validateTaskData(data, original = null) {
  const errors = {}
  const title = typeof data?.title === 'string' ? data.title.trim() : ''
  const description = typeof data?.description === 'string' ? data.description.trim() : ''
  if (!title) errors.title = 'Вкажіть назву завдання.'
  else if (title.length < 3) errors.title = 'Назва має містити щонайменше 3 символи.'
  else if (title.length > 80) errors.title = 'Максимальна довжина - 80 символів.'
  else if (!original && taskState.tasks.some((task) => task.title.trim().toLocaleLowerCase('uk') === title.toLocaleLowerCase('uk'))) {
    errors.title = 'Завдання з такою назвою вже існує.'
  }
  if (data?.description != null && typeof data.description !== 'string') errors.description = 'Опис має бути текстом.'
  else if (description.length > 300) errors.description = 'Опис не повинен перевищувати 300 символів.'
  if (!allowedStatuses.includes(data?.status)) errors.status = 'Оберіть коректний статус.'
  if (!allowedPriorities.includes(data?.priority)) errors.priority = 'Оберіть коректний пріоритет.'
  if (!Object.hasOwn(categoryLabels, data?.category ?? 'study')) errors.category = 'Оберіть коректну категорію.'
  if (!validDate(data?.dueDate)) errors.dueDate = 'Укажіть коректну дату завершення.'
  else if (data.dueDate < todayDate() && data.dueDate !== original?.dueDate) {
    errors.dueDate = 'Нова дата завершення не може бути минулою.'
  }
  return errors
}
function normalizeTaskData(data, original = null) {
  if (Object.keys(validateTaskData(data, original)).length) return null
  return { title: data.title.trim(), description: (data.description ?? '').trim(),
    status: data.status, priority: data.priority, dueDate: data.dueDate, category: data.category ?? 'study' }
}
export function addTask(data) {
  const normalized = normalizeTaskData(data)
  if (!normalized) return null
  const id = taskState.tasks.reduce((maxId, task) => Math.max(maxId, task.id), 0) + 1
  const task = { id, ...normalized }
  taskState.tasks.push(task)
  return task
}
export function updateTask(data) {
  const task = taskState.tasks.find((item) => item.id === data?.id)
  if (!task) return null
  const normalized = normalizeTaskData(data, task)
  if (!normalized) return null
  Object.assign(task, normalized)
  return task
}
export function setTaskStatus({ id, status }) {
  if (!allowedStatuses.includes(status)) return
  const task = taskState.tasks.find((item) => item.id === id)
  if (task) task.status = status
}
export function setTaskPriority({ id, priority }) {
  if (!allowedPriorities.includes(priority)) return
  const task = taskState.tasks.find((item) => item.id === id)
  if (task) task.priority = priority
}
