<template>
  <svg
    viewBox="0 0 24 24"
    class="h-5 w-5"
    fill="none"
    stroke="currentColor"
    stroke-width="2"
    stroke-linecap="round"
    stroke-linejoin="round"
    aria-hidden="true"
  >
    <g v-if="type === 'food'">
      <path d="M7 3v8" />
      <path d="M4 3v8" />
      <path d="M10 3v8" />
      <path d="M4 11h6" />
      <path d="M7 11v10" />
      <path d="M17 3v18" />
      <path d="M17 3c2 1.5 3 3.5 3 6v2h-3" />
    </g>
    <g v-else-if="type === 'fuel'">
      <path d="M5 4h9v17H5z" />
      <path d="M8 8h3" />
      <path d="M14 7h2l3 3v8a2 2 0 0 1-4 0v-3h-1" />
    </g>
    <g v-else-if="type === 'transport'">
      <path d="M6 4h12a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2Z" />
      <path d="M4 10h16" />
      <path d="M8 17v2" />
      <path d="M16 17v2" />
      <path d="M7 14h.01" />
      <path d="M17 14h.01" />
    </g>
    <g v-else-if="type === 'shopping'">
      <path d="M6 8h12l-1 12H7L6 8Z" />
      <path d="M9 8a3 3 0 0 1 6 0" />
    </g>
    <g v-else-if="type === 'communication'">
      <path d="M8 2h8a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2Z" />
      <path d="M11 18h2" />
    </g>
    <g v-else-if="type === 'entertainment'">
      <path d="M4 7h16v10H4z" />
      <path d="m9 10 4 2-4 2v-4Z" />
    </g>
    <g v-else-if="type === 'travel'">
      <path d="M3 16 21 8" />
      <path d="m15 5 6 3-4 2" />
      <path d="m7 14-2 5 5-3" />
    </g>
    <g v-else-if="type === 'health'">
      <path d="M12 21s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 5.6-7 10-7 10Z" />
      <path d="M12 8v6" />
      <path d="M9 11h6" />
    </g>
    <g v-else>
      <path d="M4 7h16" />
      <path d="M4 12h16" />
      <path d="M4 17h16" />
    </g>
  </svg>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    default: 'other',
  },
})
</script>
