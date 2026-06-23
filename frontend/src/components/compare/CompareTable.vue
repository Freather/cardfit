<template>
  <section class="overflow-hidden rounded-xl border border-[#e0e0e0] bg-white shadow-[0_4px_12px_rgba(0,0,0,0.05)]">
    <div class="grid" :style="{ gridTemplateColumns: `170px repeat(${cards.length}, minmax(190px, 1fr))` }">
      <div class="border-b border-[#e0e0e0] p-6 text-sm font-bold text-gray-700">상품 정보</div>
      <CompareCardSlot
        v-for="card in cards"
        :key="card.id"
        :card="card"
        :recommended="card.id === recommendedCardId"
        @remove="$emit('remove-card', $event)"
      />

      <template v-for="row in rows" :key="row.key">
        <div class="border-b border-[#e0e0e0] p-6 text-sm font-bold text-gray-600">{{ row.label }}</div>
        <div
          v-for="card in cards"
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
            {{ card.annual_fee ? `연회비 ${formatCurrency(card.annual_fee)}` : '없음' }}
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
        v-for="card in cards"
        :key="`action-${card.id}`"
        class="border-l border-[#e0e0e0] p-6 text-center"
        :class="card.id === recommendedCardId ? 'bg-[#001278]/5' : ''"
      >
        <RouterLink
          :to="{ name: 'card-detail', params: { id: card.id } }"
          class="inline-flex h-12 min-w-36 items-center justify-center rounded-lg px-5 text-sm font-bold transition"
          :class="
            card.id === recommendedCardId
              ? 'bg-[#001278] text-white shadow-lg hover:bg-[#1428a0]'
              : 'border border-[#001278] text-[#001278] hover:bg-[#001278] hover:text-white'
          "
        >
          {{ card.id === recommendedCardId ? '추천 카드 알아보기' : '알아보기' }}
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import CompareCardSlot from './CompareCardSlot.vue'

defineProps({
  cards: {
    type: Array,
    default: () => [],
  },
  recommendedCardId: {
    type: [String, Number],
    default: null,
  },
  rows: {
    type: Array,
    default: () => [],
  },
})

defineEmits(['remove-card'])

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
    fuel: '주유 혜택',
    travel: '여행/마일리지',
    entertainment: '문화/여가',
    health: '건강/병원',
    other: '생활 적립',
  }

  return categories.map((category) => tagByCategory[category] || '생활 혜택').slice(0, 3)
}
</script>
