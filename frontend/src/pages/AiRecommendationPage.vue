<template>
  <section class="min-h-screen bg-gradient-to-b from-[#fbf9f8] to-white px-4 py-12 md:px-10 lg:px-20">
    <div class="mx-auto max-w-5xl">
      <header class="text-center">
        <h1 class="text-4xl font-extrabold leading-tight text-[#001278] md:text-5xl">
          당신의 소비 패턴에<br />
          딱 맞는 카드를 찾아보세요
        </h1>
        <p class="mt-6 text-sm text-gray-500">
          AI가 분석하여 가장 혜택이 큰 카드를 추천해 드립니다. 지금 바로 분석을 시작해보세요.
        </p>
      </header>

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
            to="/ai-recommendations/result"
            class="inline-flex h-16 min-w-80 items-center justify-center rounded-lg bg-[#001278] px-8 text-base font-extrabold text-white shadow-[0_14px_32px_rgba(0,18,120,0.24)] transition hover:bg-[#1428a0]"
          >
            맞춤 카드 추천 시작
          </RouterLink>
        </div>
      </section>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { mockAiReport } from '../data/mockReportData'

const analysisItems = computed(() => [
  { key: 'food', label: '식비', icon: '🍽️', amount: mockAiReport.based_on.food_monthly },
  { key: 'transport', label: '대중교통', icon: '🚌', amount: mockAiReport.based_on.transport_monthly },
  { key: 'shopping', label: '온라인 쇼핑', icon: '🛒', amount: mockAiReport.based_on.shopping_monthly },
  { key: 'communication', label: '관리비/통신비', icon: '💳', amount: mockAiReport.based_on.communication_monthly + mockAiReport.based_on.other_monthly },
])

function formatCompactWon(value) {
  return `${Math.round(Number(value || 0) / 10000)}만원`
}
</script>
