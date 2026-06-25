<template>
  <AnalysisRequirementNotice
    v-if="!isCheckingAccess && !canUseAnalysis"
    eyebrow="AI 추천 준비"
    title="CSV와 소비 설문을 준비해주세요."
    :missing-requirements="missingRequirements"
  />
  <AnalysisAccessSkeleton
    v-else-if="isCheckingAccess"
    message="추천 결과 이용 가능 여부를 확인하는 중입니다..."
  />
  <RecommendationResultSkeleton
    v-else-if="isPreparingAccess || isLoadingRecommendations"
    message="AI가 소비 데이터와 카드 혜택을 맞춰보는 중입니다..."
  />
  <section v-else class="min-h-screen bg-[#fbf9f8] px-4 py-10 md:px-10 lg:px-20">
    <div class="mx-auto max-w-6xl">
      <header class="max-w-3xl">
        <h1 class="text-3xl font-extrabold text-gray-950 md:text-4xl">AI가 분석한 최적의 카드입니다</h1>
        <p class="mt-4 text-sm leading-6 text-gray-600">
          최근 소비 패턴을 분석한 결과,
          <strong class="font-extrabold text-[#001278]">{{ strongestCategoryLabel }}</strong>
          비중이 가장 높았습니다. 소비 습관과 가장 잘 맞는 혜택의 카드를 확인해보세요.
        </p>
        <p
          v-if="recommendationError"
          class="mt-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm font-bold text-red-700"
        >
          {{ recommendationError }}
        </p>
      </header>

      <div class="mt-12 grid gap-8 lg:grid-cols-[1.35fr_0.9fr]">
        <PrimaryRecommendationCard
          v-if="primaryRecommendation"
          :recommendation="primaryRecommendation"
          :card="primaryCard"
          :benefits="primaryBenefits"
          :has-higher-score-alternative="hasHigherScoreAlternative"
        />
        <div
          v-else
          class="rounded-xl border border-[#e5e0dd] bg-white p-8 text-sm font-bold text-gray-500 shadow-[0_18px_52px_rgba(0,18,120,0.08)]"
        >
          추천 결과를 만들지 못했어요. 입력 상태를 확인해보세요.
        </div>

        <aside class="space-y-7">
          <SecondaryRecommendationList :cards="secondaryCards" />
          <RecommendationAnalysisBars :items="analysisBars" :period-label="analysisPeriodLabel" />
        </aside>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

import AnalysisRequirementNotice from '../components/common/AnalysisRequirementNotice.vue'
import AnalysisAccessSkeleton from '../components/common/AnalysisAccessSkeleton.vue'
import PrimaryRecommendationCard from '../components/recommendation/PrimaryRecommendationCard.vue'
import RecommendationAnalysisBars from '../components/recommendation/RecommendationAnalysisBars.vue'
import RecommendationResultSkeleton from '../components/recommendation/RecommendationResultSkeleton.vue'
import SecondaryRecommendationList from '../components/recommendation/SecondaryRecommendationList.vue'
import { useAnalysisAccess } from '../composables/useAnalysisAccess'
import { spendingCategories } from '../data/spendingCategoryData'
import { getApiErrorMessage } from '../services/api'
import { aiService } from '../services/aiService'
import { spendingService } from '../services/spendingService'
import { useCardStore } from '../stores/cardStore'
import { normalizeRecommendations } from '../utils/normalizeRecommendation'
import {
  buildLocalRecommendations,
  buildSpendingFromBreakdown,
  buildSpendingFromSurvey,
  buildScoreReason,
  calculateRecommendationScore,
} from '../utils/recommendationMetrics'

const { authStore, spendingStore, canUseAnalysis, missingRequirements } = useAnalysisAccess()
const cardStore = useCardStore()
const isCheckingAccess = ref(true)
const isPreparingAccess = ref(false)
const isLoadingRecommendations = ref(false)
const recommendationError = ref('')
const recommendations = ref([])
const aiReport = ref(null)
const categoryBreakdown = ref([])
const analysisPeriod = ref({ start: '', end: '' })
const spendingForScore = computed(() => {
  if (categoryBreakdown.value.length) {
    return buildSpendingFromBreakdown(categoryBreakdown.value, spendingStore.latestSurvey)
  }

  return buildSpendingFromSurvey(aiReport.value?.based_on || spendingStore.latestSurvey)
})
const resolvedRecommendations = computed(() =>
  recommendations.value.map((recommendation, index) => {
    const detail = findCardDetail(recommendation)
    return {
      ...recommendation,
      detail,
      score: calculateRecommendationScore(
        recommendation,
        detail,
        spendingForScore.value,
      ),
      scoreReason: recommendation.score_reason || buildScoreReason(
        detail,
        spendingForScore.value,
        recommendation.expected_monthly_savings,
        recommendation.net_benefit,
      ),
      benefitText: getBenefitText(detail),
    }
  }),
)

const primaryRecommendation = computed(() => resolvedRecommendations.value[0] || null)
const primaryCard = computed(() => primaryRecommendation.value?.detail || {})
const secondaryCards = computed(() => resolvedRecommendations.value.slice(1, 3))
const hasHigherScoreAlternative = computed(() =>
  secondaryCards.value.some((card) => Number(card.score || 0) > Number(primaryRecommendation.value?.score || 0)),
)
const strongestCategoryLabel = computed(() => analysisBars.value[0]?.label || '주요 소비')
const analysisPeriodLabel = computed(() => formatPeriodLabel(
  analysisPeriod.value.start || spendingStore.latestCsvSurvey?.transaction_start_date,
  analysisPeriod.value.end || spendingStore.latestCsvSurvey?.transaction_end_date,
))
const analysisBars = computed(() => {
  const items = categoryBreakdown.value.length
    ? categoryBreakdown.value
    : buildBreakdownFromBasedOn(aiReport.value?.based_on)

  return [...items]
    .sort((a, b) => Number(b.ratio) - Number(a.ratio))
    .slice(0, 3)
    .map((item) => ({
      ...item,
      ratio: Math.round(Number(item.ratio || 0)),
    }))
})
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
  const cards = cardStore.cards
  const byId = cards.find((card) => String(card.id) === String(recommendation.card_id))
  const byName = cards.find((card) => normalizeCardName(card.card_name) === normalizedName)

  return byId || byName || {
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

function buildBreakdownFromBasedOn(basedOn = {}) {
  const totals = spendingCategories.map((category) => ({
    category: category.category,
    label: category.label,
    total: Number(basedOn[category.key] || 0),
  }))
  const totalAmount = totals.reduce((sum, item) => sum + item.total, 0)

  return totals
    .filter((item) => item.total > 0)
    .map((item) => ({
      ...item,
      ratio: totalAmount ? Math.round((item.total / totalAmount) * 1000) / 10 : 0,
    }))
}

function normalizeCategoryBreakdown(items = []) {
  return items.map((item) => ({
    ...item,
    category: normalizeCategoryKey(item.category),
    label: getCategoryLabel(item.category),
  }))
}

function normalizeCategoryKey(category) {
  const aliases = {
    transportation: 'transport',
    leisure: 'entertainment',
    culture: 'entertainment',
    medical: 'health',
    hospital: 'health',
    etc: 'other',
  }

  return aliases[category] || category
}

function getCategoryLabel(category) {
  const normalizedCategory = normalizeCategoryKey(category)
  return (
    spendingCategories.find((item) => item.category === normalizedCategory)?.label ||
    normalizedCategory ||
    '기타'
  )
}

function formatPeriodLabel(start, end) {
  if (start && end) return `${formatDate(start)} - ${formatDate(end)}`
  return '소비 데이터 기준'
}

function formatDate(value) {
  if (!value) return '-'

  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(new Date(value))
}

async function loadRecommendationData() {
  isLoadingRecommendations.value = true
  recommendationError.value = ''

  try {
    if (!cardStore.cards.length) {
      await cardStore.fetchCards()
    }

    const csvSurveyId = spendingStore.latestCsvSurvey?.id || spendingStore.analysisStatus.latest_csv_id
    const params = csvSurveyId
      ? { survey_id: csvSurveyId, top: 5 }
      : { top: 5 }
    const [recommendationResult, breakdownResult] = await Promise.allSettled([
      aiService.fetchRecommendations(params),
      spendingService.fetchCategoryBreakdown(params),
    ])

    const recommendationResponse =
      recommendationResult.status === 'fulfilled' ? recommendationResult.value : null
    const breakdownResponse = breakdownResult.status === 'fulfilled' ? breakdownResult.value : null

    aiReport.value = recommendationResponse?.data || {
      based_on: spendingStore.latestSurvey || {},
      recommendations: [],
    }
    const breakdownData = breakdownResponse?.data || {}
    categoryBreakdown.value = normalizeCategoryBreakdown(breakdownData.breakdown || [])
    analysisPeriod.value = {
      start: breakdownData.transaction_start_date || aiReport.value?.transaction_start_date || '',
      end: breakdownData.transaction_end_date || aiReport.value?.transaction_end_date || '',
    }

    const apiRecommendations = normalizeRecommendations(aiReport.value?.recommendations || [])
    recommendations.value = buildReliableRecommendations(apiRecommendations)

    if (!apiRecommendations.length && recommendationResult.status === 'rejected') {
      recommendationError.value = getApiErrorMessage(
        recommendationResult.reason,
        'AI 추천을 불러오지 못했어요. 카드 혜택 기준으로 계산했어요.',
      )
    }
  } catch (error) {
    aiReport.value = null
    categoryBreakdown.value = []
    analysisPeriod.value = {
      start: spendingStore.latestCsvSurvey?.transaction_start_date || '',
      end: spendingStore.latestCsvSurvey?.transaction_end_date || '',
    }
    recommendations.value = buildLocalRecommendations(
      cardStore.cards,
      buildSpendingFromSurvey(spendingStore.latestSurvey),
      5,
    )
    recommendationError.value = getApiErrorMessage(
      error,
      'AI 추천을 불러오지 못했어요. 다시 시도해주세요.',
    )
  } finally {
    isLoadingRecommendations.value = false
  }
}

function buildReliableRecommendations(apiRecommendations = []) {
  const localRecommendations = buildLocalRecommendations(
    cardStore.cards,
    spendingForScore.value,
    5,
  )

  if (!apiRecommendations.length || !localRecommendations.length) return localRecommendations

  return localRecommendations.map((localRecommendation, index) => {
    const matchedAiRecommendation = findMatchingAiRecommendation(localRecommendation, apiRecommendations)

    return {
      ...localRecommendation,
      rank: index + 1,
      reason: matchedAiRecommendation?.reason || localRecommendation.reason,
      isScoreLocked: true,
    }
  })
}

function findMatchingAiRecommendation(localRecommendation, apiRecommendations = []) {
  const localDetail = findCardDetail(localRecommendation)
  const localId = String(localDetail?.id || localRecommendation.card_id || '')
  const localName = normalizeCardName(localDetail?.card_name || localRecommendation.card_name)

  return apiRecommendations.find((apiRecommendation) => {
    const apiDetail = findCardDetail(apiRecommendation)
    const apiId = String(apiDetail?.id || apiRecommendation.card_id || '')
    const apiName = normalizeCardName(apiDetail?.card_name || apiRecommendation.card_name)

    return (localId && apiId && localId === apiId) || (localName && apiName && localName === apiName)
  })
}

onMounted(async () => {
  if (authStore.isAuthenticated) {
    isPreparingAccess.value = true
    await spendingStore.fetchLatestSurvey().catch(() => null)
    isPreparingAccess.value = false
  }

  isCheckingAccess.value = false

  if (canUseAnalysis.value) {
    await loadRecommendationData()
  }
})
</script>
