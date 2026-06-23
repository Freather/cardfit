<template>
  <section class="rounded-lg bg-[#1f30ad] p-6 text-white">
    <div class="flex items-center gap-2 text-base font-extrabold text-white/80">
      <svg class="h-5 w-5" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
        <path d="M10 16.5s-6.5-3.9-6.5-8.3A3.7 3.7 0 0 1 10 5.7a3.7 3.7 0 0 1 6.5 2.5c0 4.4-6.5 8.3-6.5 8.3Z" />
      </svg>
      찜한 카드 목록
    </div>

    <div class="mt-5 grid gap-3">
      <RouterLink
        v-for="card in cards"
        :key="card.id"
        :to="{ name: 'card-detail', params: { id: card.id } }"
        class="flex items-center gap-4 rounded-md bg-white/12 px-4 py-3 transition hover:bg-white/18"
      >
        <div class="flex h-9 w-12 shrink-0 items-center justify-center overflow-hidden rounded bg-white/12">
          <img
            v-if="card.image_url && !failedImageIds.has(card.id)"
            :src="card.image_url"
            :alt="card.card_name"
            class="h-full w-full object-contain p-1"
            @error="$emit('image-error', card.id)"
          />
          <svg v-else class="h-5 w-5 text-white/50" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">
            <rect x="3" y="5" width="14" height="10" rx="1.5" />
            <path d="M6 12h4" />
          </svg>
        </div>
        <div class="min-w-0">
          <p class="truncate text-sm font-extrabold text-white/80">{{ card.card_name }}</p>
          <p class="mt-0.5 text-xs font-semibold text-white/50">상세보기</p>
        </div>
      </RouterLink>

      <div
        v-if="!cards.length"
        class="rounded-md bg-white/12 px-4 py-8 text-center text-sm font-semibold text-white/60"
      >
        찜한 카드가 없습니다.
      </div>
    </div>
  </section>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  cards: {
    type: Array,
    default: () => [],
  },
  failedImageIds: {
    type: Object,
    default: () => new Set(),
  },
})

defineEmits(['image-error'])
</script>
