<template>
  <AnalysisRequirementNotice
    v-if="!isCheckingAccess && !isPreparingAccess && !canUseAnalysis"
    eyebrow="AI 카드 추천 준비 필요"
    title="AI 추천을 받으려면 CSV 업로드와 소비 설문이 필요합니다."
    :missing-requirements="missingRequirements"
  />
  <AnalysisAccessSkeleton
    v-else-if="isCheckingAccess"
    message="AI 추천 이용 가능 여부를 확인하는 중입니다..."
  />
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

      <p
        v-if="analysisError"
        class="mx-auto mt-8 max-w-3xl rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm font-bold text-red-700"
      >
        {{ analysisError }}
      </p>

      <AiRecommendationStartPanel
        :analysis-items="analysisItems"
        :loading="isPreparingAccess || isLoadingAnalysis"
      />
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

import AnalysisRequirementNotice from '../components/common/AnalysisRequirementNotice.vue'
import AnalysisAccessSkeleton from '../components/common/AnalysisAccessSkeleton.vue'
import AiRecommendationStartPanel from '../components/recommendation/AiRecommendationStartPanel.vue'
import { useAnalysisAccess } from '../composables/useAnalysisAccess'
import { mockAiReport } from '../data/mockReportData'
import { spendingCategories } from '../data/spendingCategoryData'
import { getApiErrorMessage } from '../services/api'
import { spendingService } from '../services/spendingService'

const { authStore, spendingStore, canUseAnalysis, missingRequirements } = useAnalysisAccess()
const isCheckingAccess = ref(true)
const isPreparingAccess = ref(false)
const isLoadingAnalysis = ref(false)
const analysisError = ref('')
const analysisBreakdown = ref([])

const categoryMetaMap = {
  food: { label: '식비', icon: '🍽️', field: 'food_monthly' },
  transport: { label: '교통', icon: '🚌', field: 'transport_monthly' },
  fuel: { label: '주유', icon: '⛽', field: 'fuel_monthly' },
  shopping: { label: '쇼핑', icon: '🛒', field: 'shopping_monthly' },
  communication: { label: '통신비', icon: '💳', field: 'communication_monthly' },
  entertainment: { label: '문화/여가', icon: '🎬', field: 'entertainment_monthly' },
  health: { label: '의료/건강', icon: '💊', field: 'health_monthly' },
  other: { label: '기타', icon: '📌', field: 'other_monthly' },
}

const analysisItems = computed(() => {
  const items = analysisBreakdown.value.length
    ? analysisBreakdown.value
    : buildItemsFromSurvey(spendingStore.latestSurvey)

  if (items.length) return items.slice(0, 4)

  return [
    { key: 'food', label: '식비', icon: '🍽️', amount: mockAiReport.based_on.food_monthly },
    { key: 'transport', label: '교통', icon: '🚌', amount: mockAiReport.based_on.transport_monthly },
    { key: 'shopping', label: '쇼핑', icon: '🛒', amount: mockAiReport.based_on.shopping_monthly },
    {
      key: 'communication',
      label: '통신/기타',
      icon: '💳',
      amount: mockAiReport.based_on.communication_monthly + mockAiReport.based_on.other_monthly,
    },
  ]
})

async function loadAnalysisData() {
  isLoadingAnalysis.value = true
  analysisError.value = ''

  try {
    const summaryResponse = await spendingService.fetchSpendingSummary()
    const summary = summaryResponse?.data || {}
    const surveyId = summary.survey_id || spendingStore.latestSurvey?.id
    const breakdownResponse = await spendingService.fetchCategoryBreakdown(
      surveyId ? { survey_id: surveyId } : {},
    )
    const breakdown = breakdownResponse?.data?.breakdown || []

    analysisBreakdown.value = breakdown.length
      ? buildItemsFromBreakdown(breakdown)
      : buildItemsFromSummary(summary)
  } catch (error) {
    if (import.meta.env.DEV && authStore.accessToken === 'mock-dev-access-token') {
      analysisBreakdown.value = []
      return
    }

    analysisError.value = getApiErrorMessage(
      error,
      '소비 분석 데이터를 불러오지 못했습니다. 설문 데이터 기준으로 표시합니다.',
    )
    analysisBreakdown.value = buildItemsFromSurvey(spendingStore.latestSurvey)
  } finally {
    isLoadingAnalysis.value = false
  }
}

function buildItemsFromBreakdown(breakdown) {
  return breakdown
    .filter((item) => Number(item.total || 0) > 0)
    .sort((a, b) => Number(b.total || 0) - Number(a.total || 0))
    .map((item) => {
      const meta = categoryMetaMap[item.category] || categoryMetaMap.other
      return {
        key: item.category,
        label: meta.label,
        icon: meta.icon,
        amount: Number(item.total || 0),
      }
    })
}

function buildItemsFromSummary(summary = {}) {
  const categories = summary.categories || {}
  const surveyLike = spendingCategories.reduce((acc, category) => {
    acc[category.key] = summary[category.key] ?? categories[category.category] ?? 0
    return acc
  }, {})

  return buildItemsFromSurvey(surveyLike)
}

function buildItemsFromSurvey(survey = {}) {
  return spendingCategories
    .map((category) => {
      const meta = categoryMetaMap[category.category] || categoryMetaMap.other
      return {
        key: category.category,
        label: meta.label,
        icon: meta.icon,
        amount: Number(survey?.[category.key] || 0),
      }
    })
    .filter((item) => item.amount > 0)
    .sort((a, b) => b.amount - a.amount)
}

onMounted(async () => {
  isCheckingAccess.value = false

  if (authStore.isAuthenticated) {
    isPreparingAccess.value = true
    await spendingStore.fetchLatestSurvey().catch(() => null)
    isPreparingAccess.value = false
  }

  if (canUseAnalysis.value) {
    await loadAnalysisData()
  }
})
</script>
