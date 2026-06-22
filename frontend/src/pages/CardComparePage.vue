<template>
  <section class="min-h-screen bg-[#fbf9f8] px-4 py-8 md:px-10 lg:px-20">
    <div class="mx-auto max-w-7xl space-y-8">
      <header class="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <p class="text-sm font-semibold text-[#001278]">카드 비교</p>
          <h1 class="mt-2 text-3xl font-bold text-gray-950">카드 비교하기</h1>
          <p class="mt-2 text-sm text-gray-500">선택한 카드들의 혜택과 조건을 한눈에 비교해 보세요.</p>
        </div>

        <RouterLink
          to="/cards"
          class="inline-flex items-center justify-center rounded-lg border border-[#001278] px-5 py-3 text-sm font-bold text-[#001278] transition hover:bg-[#001278] hover:text-white"
        >
          + 카드 추가
        </RouterLink>
      </header>

      <section class="overflow-hidden rounded-xl border border-[#e0e0e0] bg-white shadow-[0_4px_12px_rgba(0,0,0,0.05)]">
        <div class="grid" :style="{ gridTemplateColumns: `170px repeat(${compareCards.length}, minmax(190px, 1fr))` }">
          <div class="border-b border-[#e0e0e0] p-6 text-sm font-bold text-gray-700">상품 정보</div>
          <article
            v-for="card in compareCards"
            :key="card.id"
            class="relative border-b border-l border-[#e0e0e0] p-6 text-center"
            :class="card.id === recommendedCardId ? 'bg-[#001278]/5' : ''"
          >
            <span
              v-if="card.id === recommendedCardId"
              class="absolute left-1/2 top-0 -translate-x-1/2 rounded-b-md bg-[#001278] px-3 py-1 text-xs font-bold text-white"
            >
              추천
            </span>
            <button
              type="button"
              class="absolute right-3 top-3 flex h-7 w-7 items-center justify-center rounded-full text-gray-400 transition hover:bg-[#f0eded] hover:text-[#001278]"
              aria-label="비교 카드 제거"
              @click="removeCard(card.id)"
            >
              <span class="relative block h-3.5 w-3.5">
                <span class="absolute left-1/2 top-1/2 h-0.5 w-4 -translate-x-1/2 -translate-y-1/2 rotate-45 rounded-full bg-current"></span>
                <span class="absolute left-1/2 top-1/2 h-0.5 w-4 -translate-x-1/2 -translate-y-1/2 -rotate-45 rounded-full bg-current"></span>
              </span>
            </button>
            <div class="mx-auto mt-4 flex h-24 items-center justify-center">
              <img
                v-if="card.image_url"
                :src="card.image_url"
                :alt="card.card_name"
                class="max-h-20 max-w-32 object-contain drop-shadow-md"
              />
              <div v-else class="flex h-20 w-32 items-center justify-center rounded-lg bg-[#f0eded] text-xs text-gray-400">
                카드 이미지
              </div>
            </div>
            <h2 class="mt-4 text-base font-bold text-[#001278]">{{ card.card_name }}</h2>
          </article>

          <template v-for="row in rows" :key="row.key">
            <div class="border-b border-[#e0e0e0] p-6 text-sm font-bold text-gray-600">{{ row.label }}</div>
            <div
              v-for="card in compareCards"
              :key="`${row.key}-${card.id}`"
              class="border-b border-l border-[#e0e0e0] p-6 text-sm"
              :class="card.id === recommendedCardId ? 'bg-[#001278]/5' : ''"
            >
              <ul v-if="row.key === 'benefits'" class="space-y-2 text-left">
                <li v-for="benefit in card.benefits?.slice(0, 3)" :key="benefit.id" class="flex gap-2">
                  <span class="mt-1 h-2 w-2 shrink-0 rounded-full bg-[#001278]"></span>
                  <span>{{ benefit.condition_description }}</span>
                </li>
              </ul>
              <div v-else-if="row.key === 'monthlyBenefit'" class="text-lg font-extrabold text-[#001278]">
                약 {{ formatCurrency(estimateMonthlyBenefit(card)) }}
              </div>
              <div v-else-if="row.key === 'annualFee'">
                {{ card.annual_fee ? `해외겸용 ${formatCurrency(card.annual_fee)}` : '없음' }}
              </div>
              <div v-else-if="row.key === 'prevSpending'">
                {{ formatPrevSpending(card.min_prev_month_spending) }}
              </div>
              <div v-else-if="row.key === 'tags'" class="flex flex-wrap gap-2">
                <span
                  v-for="tag in buildTags(card)"
                  :key="tag"
                  class="rounded-full bg-[#f0eded] px-3 py-1 text-xs font-semibold text-gray-600"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
          </template>

          <div class="p-6"></div>
          <div
            v-for="card in compareCards"
            :key="`action-${card.id}`"
            class="border-l border-[#e0e0e0] p-6 text-center"
            :class="card.id === recommendedCardId ? 'bg-[#001278]/5' : ''"
          >
            <a
              :href="card.apply_url || '#'"
              target="_blank"
              rel="noreferrer"
              class="inline-flex h-12 min-w-36 items-center justify-center rounded-lg px-5 text-sm font-bold transition"
              :class="
                card.id === recommendedCardId
                  ? 'bg-[#001278] text-white shadow-lg hover:bg-[#1428a0]'
                  : 'border border-[#001278] text-[#001278] hover:bg-[#001278] hover:text-white'
              "
            >
              {{ card.id === recommendedCardId ? '추천 카드 알아보기' : '알아보기' }}
            </a>
          </div>
        </div>
      </section>

      <section class="rounded-xl bg-[#f6f3f2] p-8 text-sm leading-7 text-gray-600">
        <h2 class="mb-3 text-base font-bold text-[#001278]">안내사항</h2>
        <p>ⓘ 예상 월 혜택은 고정 입력 정보와 카드 혜택 조건을 기준으로 계산한 참고값입니다.</p>
        <p>ⓘ 카드는 최대 3개까지 비교할 수 있습니다.</p>
        <p>ⓘ 연회비는 기본 해외겸용 기준이며 실제 카드사 안내와 다를 수 있습니다.</p>
      </section>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useCardStore } from '../stores/cardStore'
import { useCompareStore } from '../stores/compareStore'

const cardStore = useCardStore()
const compareStore = useCompareStore()

const rows = [
  { key: 'benefits', label: '주요 혜택' },
  { key: 'monthlyBenefit', label: '예상 월 혜택' },
  { key: 'annualFee', label: '연회비' },
  { key: 'prevSpending', label: '전월 이용금액' },
  { key: 'tags', label: '특징점' },
]

const compareCards = computed(() => {
  const selected = compareStore.compareCards
  if (selected.length) return selected.slice(0, 3)
  return cardStore.cards.slice(0, 3)
})

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
  return (card.benefits || []).reduce((total, benefit) => {
    const limit = Number(benefit.monthly_limit || 0)
    if (limit) return total + limit
    return total + Math.round(Number(benefit.discount_rate || 0) * 1000)
  }, 0)
}

function formatCurrency(value) {
  return new Intl.NumberFormat('ko-KR', {
    style: 'currency',
    currency: 'KRW',
    maximumFractionDigits: 0,
  }).format(value || 0)
}

function formatPrevSpending(value) {
  if (!value) return '없음'
  return `${Math.floor(Number(value) / 10000)}만원 이상`
}

function buildTags(card) {
  const categories = (card.benefits || []).map((benefit) => benefit.benefit_category)
  const tagByCategory = {
    food: '카페/식당 특화',
    shopping: '쇼핑 혜택',
    transport: '교통 혜택',
    communication: '통신 혜택',
    travel: '여행/마일리지',
    health: '건강/병원',
    other: '생활 적립',
  }
  return categories.map((category) => tagByCategory[category] || '조건 없는 혜택').slice(0, 3)
}

onMounted(async () => {
  if (!cardStore.cards.length) {
    await cardStore.fetchCards()
  }
})
</script>
