import { validateTaskData } from '../store/tasks.js'

export function nextProjectId(projects, candidate) {
  const calculated = projects.reduce((max, project) => {
    const match = /^project-(\d+)$/.exec(project.id)
    const value = match ? Number(match[1]) : 0
    if (!Number.isSafeInteger(value) || value >= Number.MAX_SAFE_INTEGER - 1) throw new Error('Некоректний ID проєкту.')
    return Math.max(max, value)
  }, 0) + 1
  return Number.isSafeInteger(candidate) && candidate >= calculated && candidate < Number.MAX_SAFE_INTEGER
    ? candidate : calculated
}

export function validateBackup(value) {
  const fail = message => { throw new Error(message) }
  if (!value || typeof value !== 'object' || !Array.isArray(value.tasks) || !Array.isArray(value.projects)) {
    fail('Файл має містити масиви tasks і projects.')
  }
  if (value.schemaVersion != null && value.schemaVersion !== 1) fail('Непідтримувана версія JSON.')
  const ids = new Set(), names = new Set()
  const projects = value.projects.map(project => {
    if (!project || typeof project.id !== 'string' || !/^[a-zA-Z0-9_-]{1,80}$/.test(project.id) ||
      typeof project.title !== 'string' || project.title.trim().length < 3 || project.title.trim().length > 40) fail('Некоректні поля проєкту.')
    const title = project.title.trim(), name = title.toLocaleLowerCase('uk-UA')
    if (ids.has(project.id) || names.has(name)) fail('ID і назви проєктів мають бути унікальними.')
    ids.add(project.id); names.add(name)
    return { id: project.id, title }
  })
  if (!ids.has('general')) fail('Відсутній обов’язковий проєкт general.')
  const taskIds = new Set()
  const tasks = value.tasks.map(task => {
    if (!task || !Number.isSafeInteger(task.id) || task.id < 1 || task.id >= Number.MAX_SAFE_INTEGER ||
      typeof task.title !== 'string' || typeof task.description !== 'string' || typeof task.dueDate !== 'string' ||
      typeof task.projectId !== 'string' || !ids.has(task.projectId)) fail('Некоректні поля завдання або невідомий projectId.')
    // Existing backups may contain historic due dates; validate them as existing records.
    if (Object.keys(validateTaskData(task, task)).length) fail('Завдання містить некоректні значення полів.')
    if (taskIds.has(task.id)) fail('ID завдань мають бути унікальними.')
    taskIds.add(task.id)
    return { id: task.id, title: task.title.trim(), description: task.description.trim(), status: task.status,
      priority: task.priority, dueDate: task.dueDate, projectId: task.projectId, category: task.category ?? 'study' }
  })
  return { tasks, projects, nextProjectId: nextProjectId(projects, value.nextProjectId) }
}

export function serializeBackup(tasks, projects, counter) {
  return JSON.stringify({ schemaVersion: 1, exportedAt: new Date().toISOString(), tasks, projects, nextProjectId: counter }, null, 2)
}
