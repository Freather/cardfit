<template>
  <section>
    <h3 class="text-lg font-extrabold text-gray-950">다른 추천 카드</h3>
    <div class="mt-5 space-y-5">
      <RouterLink
        v-for="card in cards"
        :key="card.card_id"
        :to="{ name: 'card-detail', params: { id: card.detail.id || card.card_id } }"
        class="grid grid-cols-[88px_1fr_auto] items-center gap-4 rounded-lg border border-[#ebe5e0] bg-white p-4 shadow-[0_8px_24px_rgba(0,18,120,0.04)] transition hover:-translate-y-0.5 hover:border-[#001278]/30"
      >
        <div class="flex h-16 items-center justify-center rounded bg-[#eef2f5] px-2">
          <img
            v-if="card.detail.image_url && !failedImages.has(getCardKey(card))"
            :src="card.detail.image_url"
            :alt="card.detail.card_name"
            class="max-h-12 max-w-full object-contain"
            @error="markImageFailed(card)"
          />
          <span
            v-else
            class="text-xs font-extrabold text-[#001278]"
          >
            {{ getCardInitial(card) }}
          </span>
        </div>
        <div class="min-w-0">
          <p class="truncate text-sm font-extrabold text-gray-950">{{ card.detail.card_name || card.card_name }}</p>
          <p class="mt-1 line-clamp-2 text-[11px] font-semibold leading-4 text-gray-500">
            {{ card.scoreReason }}
          </p>
          <p class="mt-1 truncate text-xs text-[#001278]">{{ card.benefitText }}</p>
          <p class="mt-1 text-xs font-extrabold text-[#001278]">{{ card.expected_monthly_benefit }} 절약</p>
        </div>
        <span class="rounded bg-[#eef1ff] px-2 py-1 text-right text-[11px] font-extrabold leading-4 text-[#001278]">
          적합도<br />{{ card.score }}%
        </span>
      </RouterLink>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

defineProps({
  cards: {
    type: Array,
    default: () => [],
  },
})

const failedImages = ref(new Set())

function getCardKey(card) {
  return String(card.detail?.id || card.card_id || card.card_name || '')
}

function markImageFailed(card) {
  failedImages.value = new Set([...failedImages.value, getCardKey(card)])
}

function getCardInitial(card) {
  return String(card.detail?.card_name || card.card_name || 'Card').slice(0, 1)
}
</script>
