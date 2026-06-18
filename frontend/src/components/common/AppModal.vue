<script setup>
defineProps({
  open: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['close'])
</script>

<template>
  <div v-if="open" role="dialog" aria-modal="true">
    <button type="button" @click="emit('close')">Close</button>
    <slot />
  </div>
</template>
