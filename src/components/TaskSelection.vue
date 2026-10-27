<script setup>
import StatusBadge from './StatusBadge.vue'
import PriorityBadge from './PriorityBadge.vue'
defineProps({ task: { type: Object, default: null } })
defineEmits(['close'])
</script>
<template>
  <aside v-if="task" class="tf3-selection" aria-label="Обране завдання" aria-live="polite">
    <div class="tf3-section-heading">
      <h2>Обране завдання: {{ task.title }}</h2>
      <button class="tf3-action" type="button" @click="$emit('close')">Закрити деталі</button>
    </div>
    <p>{{ task.description }}</p>
    <StatusBadge :status="task.status" />
    <PriorityBadge :priority="task.priority" />
  </aside>
</template>
