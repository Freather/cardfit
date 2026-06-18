<script setup>
defineProps({
  cards: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <div>
    <slot :cards="cards" />
  </div>
</template>
