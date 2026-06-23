<template>
  <AnalysisRequirementNotice
    v-if="!isCheckingAccess && !canUseAnalysis"
    eyebrow="카드 비교 준비 필요"
    title="카드 비교를 이용하려면 CSV 업로드와 소비 설문이 필요합니다."
    :missing-requirements="missingRequirements"
  />
  <section
    v-else-if="isCheckingAccess"
    class="min-h-screen bg-[#fbf9f8] px-4 py-20 text-center text-sm font-bold text-gray-500 md:px-10 lg:px-20"
  >
    이용 가능 여부를 확인하는 중...
  </section>
  <section v-else class="min-h-screen bg-[#fbf9f8] px-4 py-8 md:px-10 lg:px-20">
    <div class="mx-auto max-w-7xl space-y-8">
      <header class="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <p class="text-sm font-semibold text-[#001278]">카드 비교</p>
          <h1 class="mt-2 text-3xl font-bold text-gray-950">카드 비교하기</h1>
          <p class="mt-2 text-sm text-gray-500">선택한 카드들의 혜택과 조건을 한눈에 비교해보세요.</p>
        </div>

        <RouterLink
          :to="{ name: 'cards' }"
          class="inline-flex items-center justify-center rounded-lg border border-[#001278] px-5 py-3 text-sm font-bold text-[#001278] transition hover:bg-[#001278] hover:text-white"
        >
          + 카드 추가
        </RouterLink>
      </header>

      <CompareTable
        v-if="compareCards.length"
        :cards="compareCards"
        :rows="rows"
        :recommended-card-id="recommendedCardId"
        @remove-card="removeCard"
      />

      <CompareEmptyState v-else />

      <CompareNotice />
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

import AnalysisRequirementNotice from '../components/common/AnalysisRequirementNotice.vue'
import CompareEmptyState from '../components/compare/CompareEmptyState.vue'
import CompareNotice from '../components/compare/CompareNotice.vue'
import CompareTable from '../components/compare/CompareTable.vue'
import { useAnalysisAccess } from '../composables/useAnalysisAccess'
import { useCardStore } from '../stores/cardStore'
import { useCompareStore } from '../stores/compareStore'

const { authStore, spendingStore, canUseAnalysis, missingRequirements } = useAnalysisAccess()
const cardStore = useCardStore()
const compareStore = useCompareStore()
const isCheckingAccess = ref(true)

const rows = [
  { key: 'benefits', label: '주요 혜택' },
  { key: 'monthlyBenefit', label: '예상 월 혜택' },
  { key: 'annualFee', label: '연회비' },
  { key: 'prevSpending', label: '전월 이용금액' },
  { key: 'tags', label: '특징' },
]

const compareCards = computed(() => compareStore.compareCards.slice(0, 3))
const recommendedCardId = computed(() => {
  return compareCards.value.reduce((best, card) => {
    if (!best) return card.id
    const bestCard = compareCards.value.find((item) => item.id === best)
    return estimateMonthlyBenefit(card) > estimateMonthlyBenefit(bestCard) ? card.id : best
  }, null)
})

function removeCard(cardId) {
  compareStore.removeCard(cardId)
}

function estimateMonthlyBenefit(card) {
  return (card?.benefits || []).reduce((total, benefit) => {
    const limit = Number(benefit.monthly_limit || 0)
    if (limit) return total + limit
    return total + Math.round(Number(benefit.discount_rate || 0) * 1000)
  }, 0)
}

onMounted(async () => {
  if (authStore.isAuthenticated) {
    await spendingStore.fetchLatestSurvey().catch(() => null)
  }

  if (!cardStore.cards.length) {
    await cardStore.fetchCards()
  }

  isCheckingAccess.value = false
})
</script>
