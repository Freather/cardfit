<template>
  <AnalysisRequirementNotice
    v-if="!isCheckingAccess && !canUseAnalysis"
    eyebrow="AI 카드 추천 준비 필요"
    title="AI 추천을 받으려면 CSV 업로드와 소비 설문이 필요합니다."
    :missing-requirements="missingRequirements"
  />
  <section
    v-else-if="isCheckingAccess"
    class="min-h-screen bg-[#fbf9f8] px-4 py-20 text-center text-sm font-bold text-gray-500 md:px-10 lg:px-20"
  >
    이용 가능 여부를 확인하는 중...
  </section>
  <section v-else class="min-h-screen bg-gradient-to-b from-[#fbf9f8] to-white px-4 py-12 md:px-10 lg:px-20">
    <div class="mx-auto max-w-5xl">
      <header class="text-center">
        <h1 class="text-4xl font-extrabold leading-tight text-[#001278] md:text-5xl">
          당신의 소비 패턴에<br />
          꼭 맞는 카드를 찾아보세요
        </h1>
        <p class="mt-6 text-sm text-gray-500">
          AI가 분석하여 가장 혜택이 큰 카드를 추천해 드립니다. 지금 바로 분석을 시작해보세요.
        </p>
      </header>

      <AiRecommendationStartPanel :analysis-items="analysisItems" />
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

import AnalysisRequirementNotice from '../components/common/AnalysisRequirementNotice.vue'
import AiRecommendationStartPanel from '../components/recommendation/AiRecommendationStartPanel.vue'
import { useAnalysisAccess } from '../composables/useAnalysisAccess'
import { mockAiReport } from '../data/mockReportData'

const { authStore, spendingStore, canUseAnalysis, missingRequirements } = useAnalysisAccess()
const isCheckingAccess = ref(true)

const analysisItems = computed(() => [
  { key: 'food', label: '식비', icon: '🍽️', amount: mockAiReport.based_on.food_monthly },
  { key: 'transport', label: '대중교통', icon: '🚌', amount: mockAiReport.based_on.transport_monthly },
  { key: 'shopping', label: '온라인 쇼핑', icon: '🛒', amount: mockAiReport.based_on.shopping_monthly },
  {
    key: 'communication',
    label: '관리비/통신비',
    icon: '💳',
    amount: mockAiReport.based_on.communication_monthly + mockAiReport.based_on.other_monthly,
  },
])

onMounted(async () => {
  if (authStore.isAuthenticated) {
    await spendingStore.fetchLatestSurvey().catch(() => null)
  }

  isCheckingAccess.value = false
})
</script>
