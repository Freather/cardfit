<template>
  <section class="min-h-screen bg-[#f4f4f5] px-5 py-10 md:px-10 lg:px-20">
    <div class="mx-auto max-w-7xl">
      <h1 class="text-3xl font-bold text-zinc-950">카드 검색</h1>

      <label
        for="card-search"
        class="mt-4 flex h-12 items-center rounded-lg border border-zinc-200 bg-white px-4 shadow-sm"
      >
        <svg class="h-4 w-4 text-zinc-400" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
          <path d="m14 14 3 3" />
          <circle cx="8.5" cy="8.5" r="5.5" />
        </svg>
        <input
          id="card-search"
          v-model="filters.searchKeyword"
          type="search"
          class="ml-3 h-full w-full bg-transparent text-sm text-zinc-800 outline-none placeholder:text-zinc-400"
          placeholder="카드명 또는 혜택을 검색하세요"
        />
      </label>

      <div class="mt-8 grid gap-6 lg:grid-cols-[250px_1fr]">
        <CardFilterPanel
          v-model:filters="filters"
          :benefit-filters="benefitFilters"
          :annual-fee-filters="annualFeeFilters"
          :company-filters="companyFilters"
          :prev-spending-filters="prevSpendingFilters"
          @reset="resetFilters"
        />

        <CardList
          v-model:sort-option="filters.sortOption"
          :cards="filteredCards"
          :failed-image-ids="failedImages"
          @image-error="onImageError"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

import CardFilterPanel from '../components/cards/CardFilterPanel.vue'
import CardList from '../components/cards/CardList.vue'
import { calculateMonthlyBenefit } from '../utils/calculateBenefit'
import { useCardStore } from '../stores/cardStore'

const cardStore = useCardStore()
const failedImages = ref(new Set())
const filters = ref(createDefaultFilters())

const sampleSpending = {
  food_monthly: 320000,
  transport_monthly: 90000,
  fuel_monthly: 100000,
  shopping_monthly: 220000,
  entertainment_monthly: 70000,
  communication_monthly: 60000,
  health_monthly: 20000,
  other_monthly: 50000,
}

const benefitFilters = [
  { label: '주유', value: 'fuel' },
  { label: '통신', value: 'communication' },
  { label: '교통', value: 'transport' },
  { label: '병원/건강', value: 'health' },
  { label: '식사', value: 'food' },
  { label: '쇼핑', value: 'shopping' },
  { label: '문화/여가', value: 'entertainment' },
  { label: '기타', value: 'other' },
]

const benefitCategoryAliases = {
  leisure: 'entertainment',
  culture: 'entertainment',
  travel: 'entertainment',
  medical: 'health',
  hospital: 'health',
  dining: 'food',
  meal: 'food',
  etc: 'other',
}

const annualFeeFilters = [
  { label: '전체', value: '' },
  { label: '무료', value: 'free' },
  { label: '1만원 이하', value: 'under10000' },
  { label: '5만원 이하', value: 'under50000' },
]

const companyFilters = [
  { label: '전체', value: '' },
  { label: '삼성카드', value: 'samsung' },
  { label: '신한카드', value: 'shinhan' },
  { label: '국민카드', value: 'kb' },
]

const companyFilterKeywords = {
  samsung: ['samsung', '삼성'],
  shinhan: ['shinhan', '신한'],
  kb: ['kb', 'kookmin', '국민'],
}

const prevSpendingFilters = [
  { label: '전체', value: '' },
  { label: '30만원 이하', value: 'under300000' },
  { label: '50만원 이하', value: 'under500000' },
]

const cards = computed(() => {
  return (cardStore.cards || []).map((card) => ({
    ...card,
    estimatedBenefit: Math.round(calculateMonthlyBenefit(card, sampleSpending)),
  }))
})

const filteredCards = computed(() => {
  const keyword = filters.value.searchKeyword.trim().toLowerCase()

  const filtered = cards.value.filter((card) => {
    return (
      matchesKeyword(card, keyword) &&
      matchesBenefit(card) &&
      matchesAnnualFee(card) &&
      matchesCompany(card) &&
      matchesPrevSpending(card)
    )
  })

  if (filters.value.sortOption === 'benefit') {
    return [...filtered].sort((a, b) => b.estimatedBenefit - a.estimatedBenefit)
  }

  if (filters.value.sortOption === 'fee') {
    return [...filtered].sort((a, b) => Number(a.annual_fee || 0) - Number(b.annual_fee || 0))
  }

  return filtered
})

onMounted(async () => {
  await cardStore.fetchCards().catch(() => null)
})

function createDefaultFilters() {
  return {
    searchKeyword: '',
    selectedBenefits: [],
    selectedAnnualFee: '',
    selectedCompany: '',
    selectedPrevSpending: '',
    sortOption: 'popular',
  }
}

function onImageError(cardId) {
  failedImages.value = new Set([...failedImages.value, cardId])
}

function resetFilters() {
  filters.value = createDefaultFilters()
}

function matchesKeyword(card, keyword) {
  if (!keyword) return true

  const searchableText = [
    card.card_name,
    card.card_company,
    ...(card.benefits || []).map((benefit) => benefit.condition_description),
  ]
    .filter(Boolean)
    .join(' ')
    .toLowerCase()

  return searchableText.includes(keyword)
}

function matchesBenefit(card) {
  if (!filters.value.selectedBenefits.length) return true

  return (card.benefits || []).some((benefit) => {
    const category = normalizeBenefitCategory(benefit.benefit_category)
    const description = String(benefit.condition_description || '')

    if (filters.value.selectedBenefits.includes(category)) return true

    return filters.value.selectedBenefits.some((selectedBenefit) =>
      getBenefitDescriptionKeywords(selectedBenefit).some((keyword) =>
        description.includes(keyword),
      ),
    )
  })
}

function matchesAnnualFee(card) {
  const selectedAnnualFee = filters.value.selectedAnnualFee

  return (
    !selectedAnnualFee ||
    (selectedAnnualFee === 'free' && Number(card.annual_fee || 0) === 0) ||
    (selectedAnnualFee === 'under10000' && Number(card.annual_fee || 0) <= 10000) ||
    (selectedAnnualFee === 'under50000' && Number(card.annual_fee || 0) <= 50000)
  )
}

function matchesCompany(card) {
  const selectedCompany = filters.value.selectedCompany
  const companyText = String(card.card_company || '').toLowerCase()
  const companyKeywords = companyFilterKeywords[selectedCompany] || []

  return !selectedCompany || companyKeywords.some((keyword) => companyText.includes(keyword))
}

function matchesPrevSpending(card) {
  const selectedPrevSpending = filters.value.selectedPrevSpending
  const spending = Number(card.min_prev_month_spending || 0)

  return (
    !selectedPrevSpending ||
    (selectedPrevSpending === 'under300000' && spending <= 300000) ||
    (selectedPrevSpending === 'under500000' && spending <= 500000)
  )
}

function normalizeBenefitCategory(category) {
  return benefitCategoryAliases[category] || category || 'other'
}

function getBenefitDescriptionKeywords(category) {
  const keywordMap = {
    fuel: ['주유', '충전소', 'LPG', 'S-OIL', 'GS칼텍스', 'SK에너지'],
    communication: ['통신', '휴대폰', 'SKT', 'KT', 'LG U+', '인터넷'],
    transport: ['교통', '버스', '지하철', '택시', '대중교통'],
    health: ['병원', '약국', '의료', '건강'],
    food: ['식사', '음식', '카페', '스타벅스', '배달', '외식', '편의점'],
    shopping: ['쇼핑', '온라인쇼핑', '오프라인', '마트', '쿠팡', 'SSG', 'G마켓'],
    entertainment: ['문화', '여가', 'OTT', '영화', '여행', '스트리밍', '넷플릭스'],
    other: ['기타', '생활', '해외'],
  }

  return keywordMap[category] || []
}
</script>
