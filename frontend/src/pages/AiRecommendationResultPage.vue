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
          <SecondaryRecommendationList :cards="secondaryCards" @select="openRecommendationModal" />
          <RecommendationAnalysisBars :items="analysisBars" :period-label="analysisPeriodLabel" />
        </aside>
      </div>
    </div>

    <div
      v-if="selectedRecommendation"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/45 px-4 py-6"
      role="dialog"
      aria-modal="true"
      @click.self="closeRecommendationModal"
    >
      <article class="max-h-[90vh] w-full max-w-3xl overflow-y-auto rounded-2xl bg-white shadow-[0_28px_80px_rgba(0,0,0,0.28)]">
        <div class="flex items-start justify-between gap-4 border-b border-gray-100 px-6 py-5">
          <div>
            <p class="text-xs font-black uppercase tracking-[0.14em] text-[#001278]">
              추천 {{ selectedRecommendation.rank || '카드' }}위
            </p>
            <h2 class="mt-1 text-2xl font-extrabold leading-tight text-gray-950">
              {{ selectedRecommendation.detail.card_name || selectedRecommendation.card_name }}
            </h2>
            <p class="mt-1 text-sm font-bold text-gray-500">
              {{ selectedRecommendation.detail.card_company || 'CardFit 추천' }}
            </p>
          </div>
          <button
            type="button"
            class="flex h-10 w-10 shrink-0 cursor-pointer items-center justify-center rounded-full bg-gray-100 text-xl font-black text-gray-500 transition hover:bg-gray-200 hover:text-gray-900"
            aria-label="추천 카드 확대 보기 닫기"
            @click="closeRecommendationModal"
          >
            ×
          </button>
        </div>

        <div class="grid gap-6 px-6 py-6 md:grid-cols-[260px_1fr]">
          <div class="flex min-h-52 items-center justify-center rounded-xl bg-gradient-to-br from-[#f4f5f2] via-[#e6ebe9] to-[#cfd8d3] p-6">
            <img
              v-if="selectedRecommendation.detail.image_url"
              :src="selectedRecommendation.detail.image_url"
              :alt="selectedRecommendation.detail.card_name"
              class="max-h-44 w-full object-contain drop-shadow-[0_18px_22px_rgba(0,0,0,0.2)]"
            />
            <div
              v-else
              class="flex h-36 w-56 items-end rounded-xl bg-[#001278] p-5 text-lg font-extrabold text-white shadow-2xl"
            >
              {{ selectedRecommendation.detail.card_name || selectedRecommendation.card_name }}
            </div>
          </div>

          <div>
            <div class="grid gap-3 sm:grid-cols-2">
              <div class="rounded-xl bg-[#eef1ff] p-4">
                <p class="text-xs font-bold text-[#001278]/70">예상 월 절약</p>
                <p class="mt-1 text-2xl font-black text-[#001278]">
                  {{ selectedRecommendation.expected_monthly_benefit }}
                </p>
              </div>
              <div class="rounded-xl bg-[#f7f7f7] p-4">
                <p class="text-xs font-bold text-gray-500">소비 패턴 적합도</p>
                <p class="mt-1 text-2xl font-black text-gray-950">{{ selectedRecommendation.score }}%</p>
              </div>
            </div>

            <p class="mt-4 rounded-xl border border-[#dfe3ff] bg-white px-4 py-3 text-sm font-bold leading-6 text-[#001278]">
              {{ selectedRecommendation.scoreReason }}
            </p>
            <p class="mt-3 text-sm leading-6 text-gray-600">
              {{ selectedRecommendation.reason }}
            </p>
          </div>
        </div>

        <section class="border-t border-gray-100 px-6 py-5">
          <h3 class="text-sm font-extrabold text-gray-950">주요 혜택</h3>
          <div class="mt-3 grid gap-3 sm:grid-cols-3">
            <article
              v-for="benefit in selectedRecommendationBenefits"
              :key="benefit.title"
              class="rounded-xl border border-gray-100 bg-[#fbfaf9] p-4"
            >
              <p class="text-xs font-extrabold text-gray-500">{{ benefit.title }}</p>
              <p class="mt-2 text-lg font-black text-[#001278]">{{ benefit.rate }}</p>
              <p class="mt-2 line-clamp-3 text-xs leading-5 text-gray-500">{{ benefit.description }}</p>
            </article>
          </div>
        </section>

        <div class="grid gap-3 border-t border-gray-100 px-6 py-5 sm:grid-cols-2">
          <RouterLink
            :to="{ name: 'card-detail', params: { id: selectedRecommendation.detail.id || selectedRecommendation.card_id } }"
            class="inline-flex h-12 cursor-pointer items-center justify-center rounded-lg border border-[#001278] px-5 text-sm font-extrabold text-[#001278] transition hover:bg-[#eef1ff]"
            @click="closeRecommendationModal"
          >
            내부 상세 페이지 보기
          </RouterLink>
          <a
            :href="selectedRecommendation.detail.apply_url || '#'"
            target="_blank"
            rel="noreferrer"
            class="inline-flex h-12 items-center justify-center rounded-lg bg-[#001278] px-5 text-sm font-extrabold text-white transition hover:bg-[#1428a0]"
          >
            카드사 사이트 열기
          </a>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

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
const selectedRecommendation = ref(null)
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
const selectedRecommendationBenefits = computed(() => buildBenefitCards(selectedRecommendation.value?.detail))

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
const recommendationCacheKey = 'cardfit.aiRecommendationResult.v1'

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

function buildBenefitCards(card) {
  const benefits = card?.benefits || []
  if (!benefits.length) {
    return [
      {
        title: '맞춤 혜택',
        rate: selectedRecommendation.value?.benefitText || '소비 패턴 기준',
        description: 'AI 추천 계산에 사용된 카드 혜택 정보를 기준으로 확인해주세요.',
      },
    ]
  }

  return benefits.slice(0, 3).map((benefit) => ({
    title: benefitTitleMap[benefit.benefit_category] || '생활 혜택',
    rate: `${Number(benefit.discount_rate || 0)}% ${benefitTypeMap[benefit.benefit_type] || '할인'}`,
    description: benefit.condition_description || '소비 패턴에 맞춘 혜택',
  }))
}

function openRecommendationModal(recommendation) {
  selectedRecommendation.value = recommendation
}

function closeRecommendationModal() {
  selectedRecommendation.value = null
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

    if (restoreCachedRecommendationData()) {
      return
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

    cacheRecommendationData()
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
    cacheRecommendationData()
  } finally {
    isLoadingRecommendations.value = false
  }
}

function restoreCachedRecommendationData() {
  const cached = readRecommendationCache()
  const currentSourceId = getRecommendationSourceId()
  if (!cached || cached.sourceId !== currentSourceId) return false

  aiReport.value = cached.aiReport || null
  categoryBreakdown.value = cached.categoryBreakdown || []
  analysisPeriod.value = cached.analysisPeriod || { start: '', end: '' }
  recommendations.value = cached.recommendations || []
  recommendationError.value = cached.recommendationError || ''
  return recommendations.value.length > 0
}

function cacheRecommendationData() {
  try {
    sessionStorage.setItem(
      recommendationCacheKey,
      JSON.stringify({
        sourceId: getRecommendationSourceId(),
        aiReport: aiReport.value,
        categoryBreakdown: categoryBreakdown.value,
        analysisPeriod: analysisPeriod.value,
        recommendations: recommendations.value,
        recommendationError: recommendationError.value,
      }),
    )
  } catch {
    // 세션 캐시는 편의 기능이라 저장 실패해도 추천 흐름은 그대로 유지합니다.
  }
}

function readRecommendationCache() {
  try {
    return JSON.parse(sessionStorage.getItem(recommendationCacheKey) || 'null')
  } catch {
    return null
  }
}

function getRecommendationSourceId() {
  return String(
    spendingStore.latestCsvSurvey?.id ||
    spendingStore.analysisStatus.latest_csv_id ||
    spendingStore.latestSurvey?.id ||
    'default',
  )
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
