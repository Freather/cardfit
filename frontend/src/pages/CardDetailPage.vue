<template>
  <CardDetailSkeleton v-if="cardStore.isLoading" />
  <div v-else-if="!card.id" class="flex min-h-screen items-center justify-center text-zinc-500">
    카드를 찾지 못했어요.
  </div>
  <div v-else class="min-h-screen bg-[#faf9f8] text-zinc-950">
    <CardDetailHeader
      :card="card"
      :is-wished="isWished"
      :wishlist-loading="wishlistLoading"
      :wishlist-message="wishlistMessage"
      :wishlist-message-tone="wishlistMessageTone"
      :compare-message="compareMessage"
      :compare-message-tone="compareMessageTone"
      @toggle-wishlist="handleToggleWishlist"
      @add-compare="handleAddCompare"
    />

    <CardAiReason
      v-if="!isCheckingAnalysisAccess && canUseAnalysis"
      :coverage-ratio="spendingAnalysis.coverageRatio"
      :covered-spending="spendingAnalysis.coveredSpending"
      :total-spending="spendingAnalysis.totalSpending"
      :monthly-benefit="spendingAnalysis.monthlyBenefit"
      :min-prev-month-spending="Number(card.min_prev_month_spending || 0)"
      :matched-labels="spendingAnalysis.matchedLabels"
      :insight="spendingAnalysis.insight"
    />
    <AnalysisRequirementNotice
      v-else-if="!isCheckingAnalysisAccess"
      compact
      eyebrow="AI 추천 사유 준비"
      title="CSV와 소비 설문을 준비해주세요."
      description="두 가지를 준비하면 이 카드가 맞는 이유를 알려드릴게요."
      :missing-requirements="missingRequirements"
    />

    <CardBenefitList
      :benefits="detailBenefits"
      :min-prev-month-spending="Number(card.min_prev_month_spending || 0)"
    />

    <CardConditionTable :rows="conditionRows" />

    <footer class="border-t border-zinc-200 bg-white px-5 py-12 text-sm text-zinc-500 md:px-10 lg:px-20">
      <div class="mx-auto max-w-7xl">
        <p class="font-bold text-zinc-900">CardFit</p>
        <div class="mt-6 flex flex-wrap gap-6">
          <a href="#" class="hover:text-blue-900">이용약관</a>
          <a href="#" class="font-bold text-blue-950 hover:text-blue-700">개인정보처리방침</a>
          <a href="#" class="hover:text-blue-900">고객센터</a>
          <a href="#" class="hover:text-blue-900">공지사항</a>
        </div>
        <p class="mt-6">© 2024 CardFit Financial Services.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'

import AnalysisRequirementNotice from '../components/common/AnalysisRequirementNotice.vue'
import CardAiReason from '../components/cards/CardAiReason.vue'
import CardBenefitList from '../components/cards/CardBenefitList.vue'
import CardConditionTable from '../components/cards/CardConditionTable.vue'
import CardDetailSkeleton from '../components/cards/CardDetailSkeleton.vue'
import CardDetailHeader from '../components/cards/CardDetailHeader.vue'
import { SURVEY_PREFERENCE_STORAGE_KEY, useAnalysisAccess } from '../composables/useAnalysisAccess'
import { getBenefitCategoryLabel } from '../data/benefitData'
import { getApiErrorMessage } from '../services/api'
import { spendingService } from '../services/spendingService'
import { useCardStore } from '../stores/cardStore'
import { useCompareStore } from '../stores/compareStore'
import { calculateMonthlyBenefit } from '../utils/calculateBenefit'

const props = defineProps({
  id: {
    type: [String, Number],
    default: null,
  },
})

const compareStore = useCompareStore()
const cardStore = useCardStore()
const { authStore, spendingStore, canUseAnalysis, missingRequirements } = useAnalysisAccess()

const compareMessage = ref('')
const compareMessageTone = ref('info')
const wishlistMessage = ref('')
const wishlistMessageTone = ref('info')
const wishlistLoading = ref(false)
const isCheckingAnalysisAccess = ref(true)
const categoryBreakdown = ref([])

const card = computed(() => cardStore.selectedCard || {})
const isWished = computed(() => {
  if (card.value?.is_wished) return true

  return cardStore.wishlist.some((wish) => {
    const wishCardId = wish.card?.id || wish.card || wish.card_id
    return String(wishCardId) === String(card.value?.id)
  })
})

const preferredBenefitCategories = computed(() => {
  const savedPreferences = loadSavedSurveyPreferences()
  const preferredCategories = getPreferredBenefitCategories(savedPreferences?.preferredBenefit)
  const selectedCategories = Array.isArray(savedPreferences?.categories) ? savedPreferences.categories : []

  return new Set([...preferredCategories, ...selectedCategories].map(normalizeBenefitCategory))
})

const detailBenefits = computed(() => {
  const baseBenefits = card.value?.benefits || []
  const hasPreferredMatch = baseBenefits.some((benefit) =>
    preferredBenefitCategories.value.has(normalizeBenefitCategory(benefit.benefit_category)),
  )

  return baseBenefits.map((benefit) => {
    const category = normalizeBenefitCategory(benefit.benefit_category)
    const isPreferenceMatch = hasPreferredMatch && preferredBenefitCategories.value.has(category)

    return {
      id: benefit.id,
      title: `${getBenefitCategoryLabel(benefit.benefit_category)} 혜택`,
      icon: getBenefitIconType(benefit.benefit_category),
      category,
      rate: formatBenefitRate(benefit),
      description: benefit.condition_description || '주요 생활 영역 혜택',
      limit: benefit.monthly_limit ? `최대 ${formatWon(benefit.monthly_limit)}원` : '제한 없음',
      condition: formatPrevSpending(card.value.min_prev_month_spending),
      tone: isPreferenceMatch ? 'blue' : 'light',
      isPreferenceMatch,
    }
  })
})

const conditionRows = [
  {
    label: '전월 실적 산정 기준',
    value: '전월 1일부터 말일까지 이용한 일시불 및 할부 합계 금액을 기준으로 산정합니다. 무이자할부, 국세, 지방세 등 일부 금액은 제외될 수 있습니다.',
  },
  {
    label: '할인 적용 방식',
    value: '결제 시 즉시 할인되는 방식이 아닌, 카드사 청구 시점에 할인 금액이 반영되는 청구할인 방식일 수 있습니다.',
  },
  {
    label: '해외 이용 수수료',
    value: '해외 결제 시 국제 브랜드 수수료와 카드사 해외서비스 수수료가 합산 청구될 수 있습니다.',
  },
  {
    label: '포인트 유효기간',
    value: '포인트는 기간이 지나면 사라질 수 있어요. 자세한 내용은 약관에서 확인해보세요.',
  },
]

const categoryLabelMap = {
  food: '식비',
  transport: '교통',
  fuel: '주유',
  shopping: '쇼핑',
  communication: '통신비',
  entertainment: '문화/여가',
  health: '의료/건강',
  other: '기타',
}

const surveyFieldByCategory = {
  food: 'food_monthly',
  transport: 'transport_monthly',
  fuel: 'fuel_monthly',
  shopping: 'shopping_monthly',
  communication: 'communication_monthly',
  entertainment: 'entertainment_monthly',
  health: 'health_monthly',
  other: 'other_monthly',
}

const spendingAnalysis = computed(() => {
  const spending = buildSpendingMap()
  const totalSpending = Object.values(spending).reduce((sum, amount) => sum + Number(amount || 0), 0)
  const benefitCategories = new Set(
    (card.value?.benefits || []).map((benefit) => normalizeBenefitCategory(benefit.benefit_category)),
  )
  const matchedItems = Object.entries(spending)
    .map(([category, amount]) => ({
      category,
      amount: Number(amount || 0),
      label: categoryLabelMap[category] || '기타',
    }))
    .filter((item) => benefitCategories.has(item.category) && item.amount > 0)
    .sort((a, b) => b.amount - a.amount)
  const coveredSpending = matchedItems.reduce((sum, item) => sum + item.amount, 0)
  const coverageRatio = totalSpending ? Math.round((coveredSpending / totalSpending) * 100) : 0
  const monthlyBenefit = calculateMonthlyBenefit(card.value, toSurveySpending(spending))
  const matchedLabels = matchedItems.map((item) => item.label)

  return {
    totalSpending,
    coveredSpending,
    coverageRatio,
    monthlyBenefit,
    matchedLabels,
    insight: buildAnalysisInsight(matchedLabels, coverageRatio, monthlyBenefit),
  }
})

onMounted(async () => {
  if (props.id) await cardStore.fetchCardDetail(props.id).catch(() => null)

  if (authStore.isAuthenticated) {
    await spendingStore.fetchLatestSurvey().catch(() => null)
    await fetchCategoryBreakdown()
  }

  isCheckingAnalysisAccess.value = false
})

watch(
  () => props.id,
  async (id) => {
    if (id) await cardStore.fetchCardDetail(id).catch(() => null)
  },
)

watch(
  () => card.value?.id,
  () => {
    compareMessage.value = ''
    wishlistMessage.value = ''
  },
)

function handleAddCompare() {
  if (!card.value?.id) return

  wishlistMessage.value = ''

  const alreadyAdded = compareStore.compareCards.some(
    (item) => String(item.id) === String(card.value.id),
  )

  if (alreadyAdded) {
    compareMessage.value = '이미 카드 비교에 담겨 있습니다.'
    compareMessageTone.value = 'info'
    return
  }

  const added = compareStore.addCard(card.value)

  if (!added) {
    compareMessage.value = '카드는 3개까지 비교할 수 있어요.'
    compareMessageTone.value = 'error'
    return
  }

  compareMessage.value = '비교함에 담았어요.'
  compareMessageTone.value = 'success'
}

async function handleToggleWishlist() {
  if (!card.value?.id || wishlistLoading.value) return

  compareMessage.value = ''

  if (!authStore.isAuthenticated) {
    wishlistMessage.value = '로그인하면 찜할 수 있어요.'
    wishlistMessageTone.value = 'error'
    return
  }

  wishlistLoading.value = true
  wishlistMessage.value = ''

  try {
    if (isWished.value) {
      await cardStore.removeWishlist(card.value.id)
      wishlistMessage.value = '찜에서 뺐어요.'
      wishlistMessageTone.value = 'info'
      return
    }

    await cardStore.addWishlist(card.value.id, 'detail')
    wishlistMessage.value = '찜에 담았어요.'
    wishlistMessageTone.value = 'success'
  } catch (error) {
    wishlistMessage.value = getApiErrorMessage(error, '찜을 바꾸지 못했어요.')
    wishlistMessageTone.value = 'error'
  } finally {
    wishlistLoading.value = false
  }
}

function formatWon(value) {
  return new Intl.NumberFormat('ko-KR').format(Number(value || 0))
}

function formatPrevSpending(value) {
  if (!value) return '조건 없음'
  return `${Math.floor(Number(value) / 10000)}만원 이상`
}

function formatBenefitRate(benefit) {
  const typeLabelMap = {
    cashback: '캐시백',
    point: '적립',
    mileage: '마일리지',
    discount: '할인',
  }

  return `${Number(benefit.discount_rate || 0)}% ${typeLabelMap[benefit.benefit_type] || '할인'}`
}

async function fetchCategoryBreakdown() {
  const surveyId = spendingStore.latestCsvSurvey?.id || spendingStore.analysisStatus.latest_csv_id
  if (!surveyId) {
    categoryBreakdown.value = []
    return
  }

  try {
    const { data } = await spendingService.fetchCategoryBreakdown({ survey_id: surveyId })
    categoryBreakdown.value = Array.isArray(data?.breakdown) ? data.breakdown : []
  } catch (error) {
    categoryBreakdown.value = []
  }
}

function buildSpendingMap() {
  const spending = Object.keys(categoryLabelMap).reduce((acc, category) => {
    acc[category] = 0
    return acc
  }, {})

  categoryBreakdown.value.forEach((item) => {
    const category = normalizeBenefitCategory(item.category)
    if (spending[category] !== undefined) {
      spending[category] = Number(item.total || 0)
    }
  })

  const hasBreakdown = Object.values(spending).some((amount) => amount > 0)
  if (hasBreakdown) return spending

  Object.entries(surveyFieldByCategory).forEach(([category, field]) => {
    spending[category] = Number(spendingStore.latestCsvSurvey?.[field] || 0)
  })

  return spending
}

function toSurveySpending(spending) {
  return Object.entries(surveyFieldByCategory).reduce((acc, [category, field]) => {
    acc[field] = Number(spending[category] || 0)
    return acc
  }, {})
}

function buildAnalysisInsight(labels, coverageRatio, monthlyBenefit) {
  if (!labels.length) {
    return '현재 소비 데이터에서 이 카드의 주요 혜택과 직접 겹치는 카테고리가 많지 않습니다. 다른 카드와 함께 비교해 보세요.'
  }

  return `${labels.slice(0, 2).join('와 ')} 지출이 이 카드의 혜택 영역과 겹칩니다. 전체 소비의 ${coverageRatio}%가 혜택 대상이며, 월 ${formatWon(monthlyBenefit)}원 절약이 예상됩니다.`
}

function getBenefitIconType(category) {
  const normalizedCategory = normalizeBenefitCategory(category)
  const iconTypes = {
    food: 'food',
    fuel: 'fuel',
    transport: 'transport',
    shopping: 'shopping',
    communication: 'communication',
    entertainment: 'entertainment',
    travel: 'travel',
    health: 'health',
    other: 'other',
  }

  return iconTypes[normalizedCategory] || 'other'
}

function normalizeBenefitCategory(category) {
  const categoryMap = {
    transportation: 'transport',
    leisure: 'entertainment',
    culture: 'entertainment',
    medical: 'health',
    hospital: 'health',
    etc: 'other',
  }

  return categoryMap[category] || category || 'other'
}

function getPreferredBenefitCategories(preferredBenefit) {
  const preferredCategoryMap = {
    '음식점, 카페 할인': ['food'],
    '버스, 지하철, 택시': ['transport'],
    '주유소 할인/적립': ['fuel'],
    '온/오프라인 쇼핑': ['shopping'],
    '통신요금 할인': ['communication'],
    'OTT, 영화, 여행': ['entertainment', 'travel'],
    '약국, 병원': ['health'],
    '그 외 혜택': ['other'],
  }

  return preferredCategoryMap[preferredBenefit] || []
}

function loadSavedSurveyPreferences() {
  try {
    return JSON.parse(localStorage.getItem(SURVEY_PREFERENCE_STORAGE_KEY) || 'null')
  } catch (error) {
    localStorage.removeItem(SURVEY_PREFERENCE_STORAGE_KEY)
    return null
  }
}
</script>
