<script setup>
defineProps({
  count: { type: Number, required: true },
  label: { type: String, default: 'Знайдено' },
})
</script>
<template>
  <span class="tf3-counter" role="status">{{ label }}: {{ count }}</span>
</template>
