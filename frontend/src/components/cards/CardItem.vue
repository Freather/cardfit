<script setup>
defineProps({
  card: {
    type: Object,
    default: null,
  },
})
</script>

<template>
  <article>
    <slot :card="card" />
  </article>
</template>
