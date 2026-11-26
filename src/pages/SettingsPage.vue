<script setup>
import { onMounted, ref } from 'vue'
import { readDatabaseStats } from '../services/database.js'
import '../css/task-components.css'
import '../css/task-list.css'
import '../css/persistence.css'
const stats = ref(null), error = ref(''), loading = ref(false)
async function refreshStats() {
  loading.value = true
  error.value = ''
  try { stats.value = await readDatabaseStats() }
  catch { error.value = 'Не вдалося прочитати локальну базу.'; stats.value = null }
  finally { loading.value = false }
}
function formatTime(value) {
  return value ? new Intl.DateTimeFormat('uk-UA', { dateStyle: 'short', timeStyle: 'medium' }).format(new Date(value)) : 'Ще не збережено'
}
onMounted(refreshStats)
</script>
<template>
<f7-page name="settings" class="tf3-page">
<f7-navbar title="Налаштування"><f7-nav-left><f7-link back>Назад</f7-link></f7-nav-left></f7-navbar>
<div class="tf3-container">
<section class="tf3-hero"><h1>Локальні дані</h1><p>Дані зберігаються в цьому браузері для поточної адреси застосунку.</p></section>
<p v-if="loading" role="status">Читання бази…</p>
<p v-if="error" class="tf4-error" role="alert">{{ error }}</p>
<dl v-if="stats" class="tf7-stats" aria-label="Збережено в IndexedDB">
<dt>Збережено завдань</dt><dd data-testid="saved-tasks">{{ stats.tasks }}</dd>
<dt>Збережено проєктів</dt><dd data-testid="saved-projects">{{ stats.projects }}</dd>
<dt>Останнє збереження</dt><dd>{{ formatTime(stats.lastSavedAt) }}</dd>
</dl>
<button type="button" class="tf5-btn" :disabled="loading" @click="refreshStats">Оновити дані</button>
<p>Перед закриттям вкладки дочекайтеся повідомлення про збереження. Якщо відкрити дві вкладки, останнє збереження може перезаписати зміни іншої вкладки. Працюйте із завданнями в одній вкладці.</p>
</div>
</f7-page>
</template>
