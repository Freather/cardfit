<template>
  <AnalysisRequirementNotice
    v-if="!isCheckingAccess && !canUseAnalysis"
    eyebrow="AI 카드 추천 준비 필요"
    title="AI 추천 결과를 보려면 CSV 업로드와 소비 설문이 필요합니다."
    :missing-requirements="missingRequirements"
  />
  <section
    v-else-if="isCheckingAccess"
    class="min-h-screen bg-[#fbf9f8] px-4 py-20 text-center text-sm font-bold text-gray-500 md:px-10 lg:px-20"
  >
    이용 가능 여부를 확인하는 중...
  </section>
  <section v-else class="min-h-screen bg-[#fbf9f8] px-4 py-10 md:px-10 lg:px-20">
    <div class="mx-auto max-w-6xl">
      <header class="max-w-3xl">
        <h1 class="text-3xl font-extrabold text-gray-950 md:text-4xl">AI가 분석한 최적의 카드입니다</h1>
        <p class="mt-4 text-sm leading-6 text-gray-600">
          최근 3개월간의 소비 패턴을 분석한 결과,
          <strong class="font-extrabold text-[#001278]">{{ strongestCategoryLabel }}</strong>
          비중이 가장 높았습니다. 당신의 소비 습관과 가장 잘 맞는 혜택의 카드를 확인해보세요.
        </p>
      </header>

      <div class="mt-12 grid gap-8 lg:grid-cols-[1.35fr_0.9fr]">
        <PrimaryRecommendationCard
          :recommendation="primaryRecommendation"
          :card="primaryCard"
          :benefits="primaryBenefits"
        />

        <aside class="space-y-7">
          <SecondaryRecommendationList :cards="secondaryCards" />
          <RecommendationAnalysisBars :items="analysisBars" />
        </aside>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

import AnalysisRequirementNotice from '../components/common/AnalysisRequirementNotice.vue'
import PrimaryRecommendationCard from '../components/recommendation/PrimaryRecommendationCard.vue'
import RecommendationAnalysisBars from '../components/recommendation/RecommendationAnalysisBars.vue'
import SecondaryRecommendationList from '../components/recommendation/SecondaryRecommendationList.vue'
import { useAnalysisAccess } from '../composables/useAnalysisAccess'
import { cardData } from '../data/cardData'
import { mockAiRecommendations, mockAiReport } from '../data/mockReportData'

const { authStore, spendingStore, canUseAnalysis, missingRequirements } = useAnalysisAccess()
const isCheckingAccess = ref(true)
const recommendations = mockAiRecommendations

const resolvedRecommendations = computed(() =>
  recommendations.map((recommendation, index) => {
    const detail = findCardDetail(recommendation)
    return {
      ...recommendation,
      detail,
      score: index === 0 ? 98 : index === 1 ? 92 : 85,
      benefitText: getBenefitText(detail),
    }
  }),
)

const primaryRecommendation = computed(() => resolvedRecommendations.value[0])
const primaryCard = computed(() => primaryRecommendation.value.detail)
const secondaryCards = computed(() => resolvedRecommendations.value.slice(1, 3))
const strongestCategoryLabel = computed(() => analysisBars.value[0]?.label || '주요 소비')
const analysisBars = computed(() =>
  [...(mockAiReport.category_breakdown || [])]
    .sort((a, b) => Number(b.ratio) - Number(a.ratio))
    .slice(0, 3)
    .map((item) => ({
      ...item,
      ratio: Math.round(Number(item.ratio || 0)),
    })),
)
const primaryBenefits = computed(() => {
  const benefits = primaryCard.value?.benefits || []

  return benefits.slice(0, 3).map((benefit) => ({
    title: benefitTitleMap[benefit.benefit_category] || '생활 혜택',
    initial: benefitInitialMap[benefit.benefit_category] || 'C',
    rate: `${Number(benefit.discount_rate || 0)}% ${benefitTypeMap[benefit.benefit_type] || '할인'}`,
    description: benefit.condition_description || '소비 패턴에 맞춘 혜택',
  }))
})

const benefitTitleMap = {
  food: 'Food & Beverage',
  transport: 'Transport',
  shopping: 'Shopping',
  communication: 'Communication',
  fuel: 'Fuel',
  travel: 'Travel',
  entertainment: 'Culture',
  health: 'Health',
  other: 'Life',
}

const benefitInitialMap = {
  food: 'F',
  transport: 'T',
  shopping: 'S',
  communication: 'C',
  fuel: 'G',
  travel: 'M',
  entertainment: 'C',
  health: 'H',
  other: 'L',
}

const benefitTypeMap = {
  point: '적립',
  mileage: '마일리지',
  cashback: '캐시백',
  discount: '할인',
}

function findCardDetail(recommendation) {
  const normalizedName = normalizeCardName(recommendation.card_name)
  const byName = cardData.find((card) => normalizeCardName(card.card_name) === normalizedName)
  const byId = cardData.find((card) => card.id === recommendation.card_id)

  return byName || byId || {
    id: recommendation.card_id,
    card_company: '삼성카드',
    card_name: recommendation.card_name,
    image_url: '',
    apply_url: '',
    benefits: [],
  }
}

function normalizeCardName(value) {
  return String(value || '')
    .toLowerCase()
    .replace(/삼성카드|삼성/g, '')
    .replace(/카드/g, '')
    .replace(/\s+/g, '')
}

function getBenefitText(card) {
  const benefit = card?.benefits?.[0]
  if (!benefit) return '맞춤 생활 혜택'

  const title = benefitTitleMap[benefit.benefit_category] || '생활'
  return `${title} ${Number(benefit.discount_rate || 0)}% 혜택`
}

onMounted(async () => {
  if (authStore.isAuthenticated) {
    await spendingStore.fetchLatestSurvey().catch(() => null)
  }

  isCheckingAccess.value = false
})
</script>
