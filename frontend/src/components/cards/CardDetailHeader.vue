<script setup>
defineProps({
  card: {
    type: Object,
    default: null,
  },
})
</script>

<template>
  <header>
    <slot :card="card" />
  </header>
</template>
