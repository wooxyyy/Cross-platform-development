<template>
<f7-toolbar bottom tabbar icons class="app-tabbar" role="navigation" aria-label="Основна навігація">
<f7-link class="link" href="/" aria-label="Головна" :aria-current="active === 'home' ? 'page' : undefined" :class="{ 'app-link-active': active === 'home' }">

<f7-icon aria-hidden="true" f7="house_fill" />
<span class="tabbar-label app-tab-label">Головна</span>
</f7-link>
<f7-link class="link" href="/tasks/" aria-label="Завдання" :aria-current="active === 'tasks' ? 'page' : undefined" :class="{ 'app-link-active': active === 'tasks' }">
<f7-icon aria-hidden="true" f7="square_list_fill" />
<span class="tabbar-label app-tab-label">Завдання</span>
</f7-link>
<f7-link class="link" href="/about/" aria-label="Про застосунок" :aria-current="active === 'about' ? 'page' : undefined" :class="{ 'app-link-active': active === 'about' }">
<f7-icon aria-hidden="true" f7="info_circle_fill" />
<span class="tabbar-label app-tab-label">Про застосунок</span>
</f7-link>
</f7-toolbar>
</template>
<script setup>
defineProps({ active: { type: String, required: true } });
</script>