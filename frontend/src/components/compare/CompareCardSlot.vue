<template>
  <article
    class="relative border-b border-l border-[#e0e0e0] p-6 text-center"
    :class="recommended ? 'bg-[#001278]/5' : ''"
  >
    <span
      v-if="recommended"
      class="absolute left-1/2 top-0 -translate-x-1/2 rounded-b-md bg-[#001278] px-3 py-1 text-xs font-bold text-white"
    >
      추천
    </span>
    <button
      type="button"
      class="absolute right-3 top-3 flex h-7 w-7 items-center justify-center rounded-full text-gray-400 transition hover:bg-[#f0eded] hover:text-[#001278]"
      aria-label="비교 카드 제거"
      @click="$emit('remove', card.id)"
    >
      <span class="relative block h-3.5 w-3.5">
        <span class="absolute left-1/2 top-1/2 h-0.5 w-4 -translate-x-1/2 -translate-y-1/2 rotate-45 rounded-full bg-current"></span>
        <span class="absolute left-1/2 top-1/2 h-0.5 w-4 -translate-x-1/2 -translate-y-1/2 -rotate-45 rounded-full bg-current"></span>
      </span>
    </button>
    <div class="mx-auto mt-4 flex h-24 items-center justify-center">
      <img
        v-if="card.image_url"
        :src="card.image_url"
        :alt="card.card_name"
        class="max-h-20 max-w-32 object-contain drop-shadow-md"
      />
      <div v-else class="flex h-20 w-32 items-center justify-center rounded-lg bg-[#f0eded] text-xs text-gray-400">
        카드 이미지
      </div>
    </div>
    <h2 class="mt-4 text-base font-bold text-[#001278]">{{ card.card_name }}</h2>
  </article>
</template>

<script setup>
defineProps({
  card: {
    type: Object,
    required: true,
  },
  recommended: Boolean,
})

defineEmits(['remove'])
</script>
