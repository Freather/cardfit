<script setup>
defineProps({
  benefits: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <ul>
    <slot :benefits="benefits" />
  </ul>
</template>
