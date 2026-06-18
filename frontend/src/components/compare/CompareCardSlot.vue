<script setup>
defineProps({
  card: {
    type: Object,
    default: null,
  },
})
</script>

<template>
  <div>
    <slot :card="card" />
  </div>
</template>
