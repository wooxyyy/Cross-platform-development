import { reactive } from 'vue'
import { useTasksStore } from '../store/tasks.js'
import { useProjectsStore } from '../store/projects.js'
import { readSnapshot, writeSnapshot } from './database.js'
import { validateBackup } from './backup.js'

export const persistenceState = reactive({ status: 'loading', error: '', canRetry: false, lastSavedAt: null })
let tasks, projects, enabled = false, writing = false, scheduled = false
let revision = 0, savedRevision = 0, fingerprint = ''

function makeSnapshot() {
  return JSON.parse(JSON.stringify({ tasks: tasks.tasks, projects: projects.projects, nextProjectId: projects.nextProjectId }))
}

async function flushChanges() {
  if (!enabled || writing) return
  writing = true
  try {
    while (savedRevision < revision) {
      const target = revision, snapshot = makeSnapshot()
      try {
        const lastSavedAt = await writeSnapshot(snapshot)
        savedRevision = target
        persistenceState.lastSavedAt = lastSavedAt
      } catch (error) {
        console.error('TaskFlow: запис IndexedDB не завершено.', error)
        Object.assign(persistenceState, { status: 'error', error: 'Зміни залишилися лише в пам’яті. Повторіть збереження.', canRetry: true })
        return
      }
    }
    Object.assign(persistenceState, { status: 'saved', error: '', canRetry: false })
  } finally { writing = false }
}

function requestSave(force = false) {
  if (!enabled) return
  const current = JSON.stringify(makeSnapshot())
  if (!force && current === fingerprint) return
  fingerprint = current
  revision++
  Object.assign(persistenceState, { status: 'saving', error: '', canRetry: false })
  void flushChanges()
}
function onChanged() {
  if (scheduled) return
  scheduled = true
  queueMicrotask(() => { scheduled = false; requestSave() })
}
export function retrySave() {
  if (enabled && persistenceState.status === 'error') requestSave(true)
}

export async function initializePersistence(pinia) {
  tasks = useTasksStore(pinia); projects = useProjectsStore(pinia)
  try {
    const snapshot = await readSnapshot()
    if (snapshot.initialized) {
      const restored = validateBackup(snapshot)
      projects.$patch({ projects: restored.projects, nextProjectId: restored.nextProjectId })
      tasks.$patch({ tasks: restored.tasks })
      persistenceState.lastSavedAt = snapshot.lastSavedAt ?? null
    } else {
      persistenceState.lastSavedAt = await writeSnapshot(makeSnapshot())
    }
    enabled = true
    fingerprint = JSON.stringify(makeSnapshot())
    persistenceState.status = 'saved'
    tasks.$subscribe(onChanged, { detached: true, flush: 'sync' })
    projects.$subscribe(onChanged, { detached: true, flush: 'sync' })
  } catch (error) {
    console.error('TaskFlow: локальні дані не відновлено.', error)
    Object.assign(persistenceState, { status: 'error', canRetry: false,
      error: 'Не вдалося відновити локальні дані. Працює тимчасовий стан; наявну базу не перезаписано.' })
  }
}
