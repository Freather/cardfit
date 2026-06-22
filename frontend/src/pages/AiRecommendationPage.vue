<template>
  <section class="min-h-screen bg-[#fbf9f8] px-4 py-8 md:px-10 lg:px-20">
    <div class="mx-auto max-w-7xl space-y-8">
      <header>
        <p class="text-sm font-semibold text-[#001278]">AI 카드 추천</p>
        <h1 class="mt-2 text-3xl font-bold text-gray-950">추천 카드 보기</h1>
        <p class="mt-2 text-sm text-gray-500">
          소비 분석 결과를 바탕으로 예상 혜택이 높은 카드를 추천합니다.
        </p>
      </header>

      <section class="grid gap-6 md:grid-cols-3">
        <article
          v-for="card in recommendations"
          :key="card.card_id"
          class="flex min-h-[280px] flex-col rounded-xl border border-[#e0e0e0] bg-white p-6 shadow-[0_4px_12px_rgba(0,0,0,0.05)]"
        >
          <div class="mb-5 flex items-start justify-between gap-4">
            <div>
              <p class="text-sm font-bold text-[#001278]">추천 {{ card.rank }}위</p>
              <h2 class="mt-2 text-xl font-bold text-gray-950">{{ card.card_name }}</h2>
            </div>
            <span class="rounded-full bg-[#dfe0ff] px-3 py-1 text-xs font-bold text-[#001278]">
              {{ card.expected_monthly_benefit }}
            </span>
          </div>

          <p class="text-sm leading-6 text-gray-600">{{ card.reason }}</p>
          <p class="mt-4 rounded-lg bg-[#fbf9f8] p-4 text-sm leading-6 text-gray-700">{{ card.tip }}</p>

          <RouterLink
            :to="{ name: 'card-detail', params: { id: card.card_id } }"
            class="mt-auto inline-flex h-12 items-center justify-center rounded-lg border border-[#001278] px-5 text-sm font-bold text-[#001278] transition hover:bg-[#001278] hover:text-white"
          >
            카드 상세 보기
          </RouterLink>
        </article>
      </section>
    </div>
  </section>
</template>

<script setup>
import { mockAiRecommendations } from '../data/mockReportData'

const recommendations = mockAiRecommendations
</script>
