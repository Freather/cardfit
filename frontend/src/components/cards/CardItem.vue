<template>
  <article class="rounded-xl bg-white p-6 shadow-lg shadow-zinc-200/90">
    <div class="flex gap-6">
      <div class="flex h-28 w-32 shrink-0 items-center justify-center overflow-hidden rounded-lg border border-zinc-200 bg-zinc-50">
        <img
          v-if="card.image_url && !failed"
          :src="card.image_url"
          :alt="card.card_name"
          class="h-full w-full object-contain p-2"
          @error="$emit('image-error', card.id)"
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
        <p class="mt-1 text-sm text-zinc-500">{{ specialtyLabel }}</p>
        <p class="mt-1 text-sm text-zinc-500">연회비 {{ formatWon(card.annual_fee) }}원</p>
      </div>
    </div>

    <div class="mt-6 flex flex-wrap gap-2">
      <span class="rounded-full border border-zinc-200 px-4 py-1.5 text-xs text-zinc-600">
        {{ formatPrevSpending(card.min_prev_month_spending) }}
      </span>
      <span class="rounded-full border border-zinc-200 px-4 py-1.5 text-xs text-zinc-600">
        {{ mainBenefit }}
      </span>
    </div>

    <div class="mt-6 flex items-center justify-between gap-4">
      <p class="text-sm font-bold text-emerald-600">
        예상 월 혜택 {{ formatWon(card.estimatedBenefit) }}원
      </p>
      <RouterLink
        :to="{ name: 'card-detail', params: { id: card.id } }"
        class="inline-flex h-9 w-24 items-center justify-center rounded-md border border-blue-600 text-sm font-bold text-blue-600 transition hover:bg-blue-50"
      >
        상세
      </RouterLink>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { getBenefitCategoryLabel } from '../../data/benefitData'
import { getRepresentativeBenefit } from '../../utils/representativeBenefit'

const props = defineProps({
  card: {
    type: Object,
    required: true,
  },
  failed: Boolean,
})

defineEmits(['image-error'])

const mainBenefit = computed(() => {
  const benefit = representativeBenefit.value
  if (!benefit) return '기본 혜택'

  return `${getBenefitCategoryLabel(benefit.benefit_category)} ${formatRate(benefit.discount_rate)}%`
})

const specialtyLabel = computed(() => {
  if (!representativeBenefit.value) return '기본 혜택 카드'
  return `${mainBenefit.value} 특화`
})

const representativeBenefit = computed(() => {
  return getRepresentativeBenefit(props.card)
})

function formatWon(value) {
  return new Intl.NumberFormat('ko-KR').format(Number(value || 0))
}

function formatRate(value) {
  const rate = Number(value || 0)
  return Number.isInteger(rate) ? rate : rate.toFixed(1)
}

function formatPrevSpending(value) {
  if (!value) return '조건 없음'
  return `전월실적 ${Math.floor(Number(value) / 10000)}만`
}
</script>
