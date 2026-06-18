<script setup>
defineProps({
  modelValue: {
    type: [String, Number],
    default: '',
  },
  options: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['update:modelValue'])
</script>

<template>
  <select :value="modelValue" @change="emit('update:modelValue', $event.target.value)">
    <option v-for="option in options" :key="option.value ?? option.key" :value="option.value ?? option.key">
      {{ option.label }}
    </option>
  </select>
</template>
