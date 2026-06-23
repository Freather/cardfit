<template>
  <section class="mx-auto mt-10 max-w-3xl rounded-xl border border-[#e0e0e0] bg-white/85 p-8 shadow-[0_18px_60px_rgba(0,18,120,0.08)] backdrop-blur md:mt-12">
    <div class="rounded-lg bg-[#f0f3ff] px-4 py-3 text-center text-sm font-bold text-[#4254b8]">
      사용자의 최근 3개월 소비 데이터를 바탕으로 분석되었습니다.
    </div>

    <div class="mt-8">
      <h2 class="text-3xl font-extrabold text-[#001278]">AI 맞춤 분석</h2>
    </div>

    <div class="mt-8 grid gap-5 sm:grid-cols-2">
      <article
        v-for="item in analysisItems"
        :key="item.key"
        class="flex items-center justify-between rounded-lg bg-[#f6f7fb] px-5 py-4"
      >
        <div class="flex items-center gap-3">
          <span class="text-xl">{{ item.icon }}</span>
          <span class="text-base font-bold text-[#001278]">{{ item.label }}</span>
        </div>
        <span class="text-lg font-extrabold text-[#001278]">{{ formatCompactWon(item.amount) }}</span>
      </article>
    </div>

    <div class="mt-12 flex justify-center">
      <RouterLink
        :to="{ name: 'ai-recommendations-result' }"
        class="inline-flex h-16 min-w-80 items-center justify-center rounded-lg bg-[#001278] px-8 text-base font-extrabold text-white shadow-[0_14px_32px_rgba(0,18,120,0.24)] transition hover:bg-[#1428a0]"
      >
        맞춤 카드 추천 시작
      </RouterLink>
    </div>
  </section>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  analysisItems: {
    type: Array,
    default: () => [],
  },
})

function formatCompactWon(value) {
  return `${Math.round(Number(value || 0) / 10000)}만원`
}
</script>
