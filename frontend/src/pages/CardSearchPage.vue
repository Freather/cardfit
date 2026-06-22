<script setup>
import { computed, ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'

import { getBenefitCategoryLabel } from '../data/benefitData'
import { calculateMonthlyBenefit } from '../utils/calculateBenefit'
import { useCardStore } from '../stores/cardStore'

const cardStore = useCardStore()

const failedImages = ref(new Set())
function onImageError(cardId) {
  failedImages.value = new Set([...failedImages.value, cardId])
}

const searchKeyword = ref('')
const selectedBenefits = ref([])
const selectedAnnualFee = ref('')
const selectedCompany = ref('samsung')
const selectedPrevSpending = ref('')
const sortOption = ref('popular')

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
]

const annualFeeFilters = [
  { label: '전체', value: '' },
  { label: '무료', value: 'free' },
  { label: '1만원 이하', value: 'under10000' },
  { label: '5만원 이하', value: 'under50000' },
]

const companyFilters = [
  { label: '삼성카드', value: 'samsung' },
  { label: '신한카드', value: 'shinhan' },
  { label: '국민카드', value: 'kb' },
]

const prevSpendingFilters = [
  { label: '전체', value: '' },
  { label: '30만원 이하', value: 'under300000' },
  { label: '50만원 이하', value: 'under500000' },
]

const cards = computed(() => {
  return cardStore.cards.map((card) => ({
    ...card,
    estimatedBenefit: Math.round(calculateMonthlyBenefit(card, sampleSpending)),
  }))
})

onMounted(() => {
  cardStore.fetchCards()
})

const filteredCards = computed(() => {
  const keyword = searchKeyword.value.trim().toLowerCase()

  const filtered = cards.value.filter((card) => {
    const matchesKeyword =
      !keyword ||
      card.card_name.toLowerCase().includes(keyword) ||
      card.card_company.toLowerCase().includes(keyword)

    const matchesBenefit =
      selectedBenefits.value.length === 0 ||
      card.benefits.some((benefit) => {
        if (selectedBenefits.value.includes('fuel')) {
          const matchesFuel =
            benefit.benefit_category === 'fuel' || benefit.condition_description?.includes('주유')

          if (matchesFuel) return true
        }

        return selectedBenefits.value.includes(benefit.benefit_category)
      })

    const matchesAnnualFee =
      !selectedAnnualFee.value ||
      (selectedAnnualFee.value === 'free' && card.annual_fee === 0) ||
      (selectedAnnualFee.value === 'under10000' && card.annual_fee <= 10000) ||
      (selectedAnnualFee.value === 'under50000' && card.annual_fee <= 50000)

    const matchesCompany =
      !selectedCompany.value ||
      (selectedCompany.value === 'samsung' && card.card_company.includes('삼성'))

    const matchesPrevSpending =
      !selectedPrevSpending.value ||
      (selectedPrevSpending.value === 'under300000' && card.min_prev_month_spending <= 300000) ||
      (selectedPrevSpending.value === 'under500000' && card.min_prev_month_spending <= 500000)

    return (
      matchesKeyword &&
      matchesBenefit &&
      matchesAnnualFee &&
      matchesCompany &&
      matchesPrevSpending
    )
  })

  if (sortOption.value === 'benefit') {
    return [...filtered].sort((a, b) => b.estimatedBenefit - a.estimatedBenefit)
  }

  if (sortOption.value === 'fee') {
    return [...filtered].sort((a, b) => a.annual_fee - b.annual_fee)
  }

  return filtered
})

function formatWon(value) {
  return new Intl.NumberFormat('ko-KR').format(value)
}

function getMainBenefit(card) {
  const benefit = card.benefits[0]
  if (!benefit) return '혜택'

  return `${getBenefitCategoryLabel(benefit.benefit_category)} ${Number(benefit.discount_rate)}%`
}

function formatPrevSpending(value) {
  if (!value) return '조건 없음'
  return `전월실적 ${Math.floor(value / 10000)}만`
}

function resetFilters() {
  searchKeyword.value = ''
  selectedBenefits.value = []
  selectedAnnualFee.value = ''
  selectedCompany.value = 'samsung'
  selectedPrevSpending.value = ''
  sortOption.value = 'popular'
}

function toggleBenefit(value) {
  if (selectedBenefits.value.includes(value)) {
    selectedBenefits.value = selectedBenefits.value.filter((benefit) => benefit !== value)
    return
  }

  selectedBenefits.value = [...selectedBenefits.value, value]
}
</script>

<template>
  <section class="min-h-screen bg-[#f4f4f5] px-5 py-10 md:px-10 lg:px-20">
    <div class="mx-auto max-w-7xl">
      <h1 class="text-3xl font-bold text-zinc-950">카드 검색</h1>

      <label
        for="card-search"
        class="mt-4 flex h-12 items-center rounded-lg border border-zinc-200 bg-white px-4 shadow-sm"
      >
        <span class="text-zinc-400">⌕</span>
        <input
          id="card-search"
          v-model="searchKeyword"
          type="search"
          class="ml-3 h-full w-full bg-transparent text-sm text-zinc-800 outline-none placeholder:text-zinc-400"
          placeholder="카드명 또는 혜택을 검색하세요"
        />
      </label>

      <div class="mt-8 grid gap-6 lg:grid-cols-[250px_1fr]">
        <aside class="h-fit rounded-xl bg-white p-6 shadow-md shadow-zinc-200/80">
          <h2 class="text-base font-bold text-zinc-900">필터</h2>

          <div class="mt-6">
            <h3 class="text-sm font-bold text-zinc-800">혜택 유형</h3>
            <div class="mt-3 flex flex-wrap gap-2 lg:flex-col">
              <button
                v-for="filter in benefitFilters"
                :key="filter.label"
                type="button"
                class="w-fit rounded-full border px-4 py-1.5 text-sm transition"
                :class="
                  selectedBenefits.includes(filter.value)
                    ? 'border-blue-600 bg-blue-50 text-blue-700'
                    : 'border-zinc-200 bg-white text-zinc-600 hover:border-blue-300'
                "
                @click="toggleBenefit(filter.value)"
              >
                {{ filter.label }}
              </button>
            </div>
          </div>

          <div class="mt-7">
            <h3 class="text-sm font-bold text-zinc-800">연회비</h3>
            <label
              v-for="filter in annualFeeFilters"
              :key="filter.value"
              class="mt-3 flex items-center gap-2 text-sm text-zinc-600"
            >
              <input
                v-model="selectedAnnualFee"
                type="radio"
                name="annual-fee"
                :value="filter.value"
                class="h-4 w-4 accent-blue-600"
              />
              {{ filter.label }}
            </label>
          </div>

          <div class="mt-7">
            <h3 class="text-sm font-bold text-zinc-800">카드사</h3>
            <label
              v-for="filter in companyFilters"
              :key="filter.value"
              class="mt-3 flex items-center gap-2 text-sm"
              :class="filter.value === 'samsung' ? 'text-zinc-700' : 'text-zinc-400'"
            >
              <input
                v-model="selectedCompany"
                type="radio"
                name="company"
                :value="filter.value"
                :disabled="filter.value !== 'samsung'"
                class="h-4 w-4 accent-blue-600 disabled:accent-zinc-200"
              />
              {{ filter.label }}
            </label>
          </div>

          <div class="mt-7">
            <h3 class="text-sm font-bold text-zinc-800">전월 실적</h3>
            <label
              v-for="filter in prevSpendingFilters"
              :key="filter.value"
              class="mt-3 flex items-center gap-2 text-sm text-zinc-600"
            >
              <input
                v-model="selectedPrevSpending"
                type="radio"
                name="prev-spending"
                :value="filter.value"
                class="h-4 w-4 accent-blue-600"
              />
              {{ filter.label }}
            </label>
          </div>

          <button
            type="button"
            class="mt-6 h-11 w-full rounded-lg bg-blue-600 text-sm font-bold text-white transition hover:bg-blue-700"
            @click="resetFilters"
          >
            필터 적용
          </button>
        </aside>

        <div>
          <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <p class="text-sm font-bold text-zinc-900">총 {{ filteredCards.length }}개 카드</p>
            <label class="flex items-center gap-2 self-start text-sm text-zinc-500 sm:self-auto">
              정렬:
              <select v-model="sortOption" class="rounded-md bg-transparent text-zinc-700 outline-none">
                <option value="popular">인기순</option>
                <option value="benefit">혜택순</option>
                <option value="fee">연회비 낮은순</option>
              </select>
            </label>
          </div>

          <div class="mt-4 grid gap-6 md:grid-cols-2">
            <article
              v-for="card in filteredCards"
              :key="card.id"
              class="rounded-xl bg-white p-6 shadow-lg shadow-zinc-200/90"
            >
              <div class="flex gap-6">
                <div class="flex h-28 w-32 shrink-0 items-center justify-center rounded-lg border border-zinc-200 bg-zinc-50 overflow-hidden">
                  <img
                    v-if="card.image_url && !failedImages.has(card.id)"
                    :src="card.image_url"
                    :alt="card.card_name"
                    class="h-full w-full object-contain p-2"
                    @error="onImageError(card.id)"
                  />
                  <div
                    v-else
                    class="flex h-full w-full items-end rounded-lg p-3"
                    style="background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 60%, #3b82f6 100%)"
                  >
                    <span class="text-[10px] font-bold leading-tight text-white/90">{{ card.card_name }}</span>
                  </div>
                </div>

                <div class="min-w-0 flex-1">
                  <h2 class="truncate text-lg font-bold text-zinc-950">{{ card.card_name }}</h2>
                  <p class="mt-1 text-sm text-zinc-500">{{ getMainBenefit(card) }} 특화</p>
                  <p class="mt-1 text-sm text-zinc-500">연회비 {{ formatWon(card.annual_fee) }}원</p>
                </div>
              </div>

              <div class="mt-6 flex flex-wrap gap-2">
                <span class="rounded-full border border-zinc-200 px-4 py-1.5 text-xs text-zinc-600">
                  {{ formatPrevSpending(card.min_prev_month_spending) }}
                </span>
                <span class="rounded-full border border-zinc-200 px-4 py-1.5 text-xs text-zinc-600">
                  {{ getMainBenefit(card) }}
                </span>
              </div>

              <div class="mt-6 flex items-center justify-between gap-4">
                <p class="text-sm font-bold text-emerald-600">
                  예상 월 혜택 ₩{{ formatWon(card.estimatedBenefit) }}
                </p>
                <RouterLink
                  :to="{ name: 'card-detail', params: { id: card.id } }"
                  class="inline-flex h-9 w-24 items-center justify-center rounded-md border border-blue-600 text-sm font-bold text-blue-600 transition hover:bg-blue-50"
                >
                  상세
                </RouterLink>
              </div>
            </article>
          </div>

          <div
            v-if="filteredCards.length === 0"
            class="mt-4 rounded-xl bg-white p-10 text-center text-sm text-zinc-500 shadow-md shadow-zinc-200/80"
          >
            조건에 맞는 카드가 없습니다.
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
