<template>
  <div v-if="cardStore.isLoading" class="flex min-h-screen items-center justify-center text-zinc-500">
    카드 정보를 불러오는 중...
  </div>
  <div v-else-if="!card.id" class="flex min-h-screen items-center justify-center text-zinc-500">
    카드를 찾을 수 없습니다.
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
      v-if="authStore.isAuthenticated"
      :keywords="aiKeywords"
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

import CardAiReason from '../components/cards/CardAiReason.vue'
import CardBenefitList from '../components/cards/CardBenefitList.vue'
import CardConditionTable from '../components/cards/CardConditionTable.vue'
import CardDetailHeader from '../components/cards/CardDetailHeader.vue'
import { SURVEY_PREFERENCE_STORAGE_KEY } from '../composables/useAnalysisAccess'
import { getBenefitCategoryLabel } from '../data/benefitData'
import { useAuthStore } from '../stores/authStore'
import { useCardStore } from '../stores/cardStore'
import { useCompareStore } from '../stores/compareStore'

const props = defineProps({
  id: {
    type: [String, Number],
    default: null,
  },
})

const compareStore = useCompareStore()
const cardStore = useCardStore()
const authStore = useAuthStore()

const compareMessage = ref('')
const compareMessageTone = ref('info')
const wishlistMessage = ref('')
const wishlistMessageTone = ref('info')
const wishlistLoading = ref(false)

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

    return {
      id: benefit.id,
      title: `${getBenefitCategoryLabel(benefit.benefit_category)} 혜택`,
      icon: getBenefitIconType(benefit.benefit_category),
      category,
      rate: formatBenefitRate(benefit),
      description: benefit.condition_description || '주요 생활 영역 혜택',
      limit: benefit.monthly_limit ? `최대 ${formatWon(benefit.monthly_limit)}원` : '제한 없음',
      condition: formatPrevSpending(card.value.min_prev_month_spending),
      tone: hasPreferredMatch && preferredBenefitCategories.value.has(category) ? 'blue' : 'light',
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
    value: '적립 포인트는 카드사 정책에 따라 일정 기간 이후 소멸될 수 있으므로 상세 약관을 확인해주세요.',
  },
]

const aiKeywords = ['배달 앱', '스트리밍 서비스', '생활비 결제']

onMounted(() => {
  if (props.id) cardStore.fetchCardDetail(props.id)
})

watch(
  () => props.id,
  (id) => {
    if (id) cardStore.fetchCardDetail(id)
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
    compareMessage.value = '카드 비교는 최대 3개까지만 담을 수 있습니다.'
    compareMessageTone.value = 'error'
    return
  }

  compareMessage.value = '카드 비교에 담았습니다.'
  compareMessageTone.value = 'success'
}

async function handleToggleWishlist() {
  if (!card.value?.id || wishlistLoading.value) return

  if (!authStore.isAuthenticated) {
    wishlistMessage.value = '로그인 후 찜할 수 있습니다.'
    wishlistMessageTone.value = 'error'
    return
  }

  wishlistLoading.value = true
  wishlistMessage.value = ''

  try {
    if (isWished.value) {
      await cardStore.removeWishlist(card.value.id)
      wishlistMessage.value = '찜 목록에서 제거했습니다.'
      wishlistMessageTone.value = 'info'
      return
    }

    await cardStore.addWishlist(card.value.id, 'detail')
    wishlistMessage.value = '찜 목록에 추가했습니다.'
    wishlistMessageTone.value = 'success'
  } catch (error) {
    wishlistMessage.value = '찜 처리 중 문제가 발생했습니다.'
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
