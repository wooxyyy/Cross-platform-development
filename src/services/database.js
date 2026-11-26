import { openDB } from 'idb'

let databasePromise = null
const stores = ['tasks', 'projects', 'metadata']

export function getDatabase() {
  if (typeof indexedDB === 'undefined') return Promise.reject(new Error('IndexedDB недоступна.'))
  if (!databasePromise) {
    databasePromise = openDB('taskflow-db', 1, {
      upgrade(db) {
        db.createObjectStore('tasks', { keyPath: 'id' })
        db.createObjectStore('projects', { keyPath: 'id' })
        db.createObjectStore('metadata')
      },
      blocking() {
        databasePromise?.then(db => db.close())
        databasePromise = null
      },
      terminated() { databasePromise = null },
    }).catch(error => { databasePromise = null; throw error })
  }
  return databasePromise
}

export async function readSnapshot() {
  const db = await getDatabase()
  const tx = db.transaction(stores, 'readonly')
  const [tasks, projects, initialized, nextProjectId, lastSavedAt] = await Promise.all([
    tx.objectStore('tasks').getAll(), tx.objectStore('projects').getAll(),
    tx.objectStore('metadata').get('initialized'), tx.objectStore('metadata').get('nextProjectId'),
    tx.objectStore('metadata').get('lastSavedAt'), tx.done,
  ])
  return { tasks, projects, initialized: initialized === true, nextProjectId, lastSavedAt }
}

export async function writeSnapshot(snapshot) {
  const db = await getDatabase()
  const tx = db.transaction(stores, 'readwrite')
  const tasks = tx.objectStore('tasks'), projects = tx.objectStore('projects'), metadata = tx.objectStore('metadata')
  const lastSavedAt = new Date().toISOString()
  // All three stores commit together. Only IndexedDB promises are awaited inside this transaction.
  const operations = [tx.done]
  try {
    operations.push(tasks.clear(), projects.clear())
    for (const task of snapshot.tasks) operations.push(tasks.put(task))
    for (const project of snapshot.projects) operations.push(projects.put(project))
    operations.push(metadata.put(true, 'initialized'), metadata.put(snapshot.nextProjectId, 'nextProjectId'),
      metadata.put(lastSavedAt, 'lastSavedAt'))
    await Promise.all(operations)
  } catch (error) {
    try { tx.abort() } catch { /* It may already be aborted. */ }
    // Also observe already queued requests if a later put() throws synchronously.
    await Promise.allSettled(operations)
    throw error
  }
  return lastSavedAt
}

// Low-level alternative to a full snapshot. Callers must keep Pinia consistent themselves.
export async function deleteTaskRecord(id) {
  if (!Number.isSafeInteger(id) || id < 1) throw new Error('Некоректний ID завдання.')
  const db = await getDatabase()
  const tx = db.transaction(['tasks', 'metadata'], 'readwrite')
  await Promise.all([
    tx.objectStore('tasks').delete(id),
    tx.objectStore('metadata').put(new Date().toISOString(), 'lastSavedAt'), tx.done,
  ])
}

export async function readDatabaseStats() {
  const db = await getDatabase()
  const tx = db.transaction(stores, 'readonly')
  const [tasks, projects, lastSavedAt] = await Promise.all([
    tx.objectStore('tasks').count(), tx.objectStore('projects').count(),
    tx.objectStore('metadata').get('lastSavedAt'), tx.done,
  ])
  return { tasks, projects, lastSavedAt }
}
