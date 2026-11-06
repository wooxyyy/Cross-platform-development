<script setup>
defineProps({
  search: { type: String, default: '' },
  status: { type: String, default: 'all' },
  priority: { type: String, default: 'all' },
  sort: { type: String, default: 'newest' },
  incomplete: { type: Boolean, default: false },
})
const emit = defineEmits(['update:search', 'update:status', 'update:priority', 'update:sort', 'update:incomplete', 'reset'])
</script>
<template>
<section class="tf5-panel" aria-label="Пошук і фільтри">
  <h2>Пошук і впорядкування</h2>
  <div class="tf5-controls-grid">
    <label class="tf5-search" for="task-search">Пошук за назвою та описом
      <input id="task-search" type="search" :value="search" placeholder="Наприклад: інтерфейс"
        @input="emit('update:search', $event.target.value)" />
    </label>
    <label for="task-status">Статус
      <select id="task-status" :value="status" @change="emit('update:status', $event.target.value)">
        <option value="all">Усі статуси</option><option value="todo">Заплановано</option>
        <option value="progress">У роботі</option><option value="done">Виконано</option>
      </select>
    </label>
    <label for="task-priority">Пріоритет
      <select id="task-priority" :value="priority" @change="emit('update:priority', $event.target.value)">
        <option value="all">Усі пріоритети</option><option value="low">Низький</option>
        <option value="medium">Середній</option><option value="high">Високий</option>
      </select>
    </label>
    <label class="tf5-search" for="task-sort">Сортування
      <select id="task-sort" :value="sort" @change="emit('update:sort', $event.target.value)">
        <option value="newest">Спочатку нові</option><option value="title">За назвою (А–Я)</option>
        <option value="priority">За пріоритетом (високий перший)</option>
        <option value="dueDate">За терміном (найближчий перший)</option>
        <option value="dueDate-desc">За терміном (найпізніший перший)</option>
        <option value="status">За статусом: у роботі → заплановано → виконано</option>
        <option value="low-first">За пріоритетом (низький перший)</option>
        <option value="original">За порядком додавання</option>
      </select>
    </label>
  </div>
  <div class="tf5-actions">
    <button type="button" class="tf5-btn" :class="{ 'is-active': incomplete }" :aria-pressed="incomplete"
      @click="emit('update:incomplete', !incomplete)">Тільки невиконані</button>
    <button v-if="search" type="button" class="tf5-btn" @click="emit('update:search', '')">Очистити пошук</button>
    <button type="button" class="tf5-btn" @click="emit('reset')">Скинути фільтри</button>
  </div>
</section>
</template>
