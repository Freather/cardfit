<template>
  <section
    v-if="report"
    class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm"
  >
    <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
      <div>
        <p class="text-sm font-extrabold text-[#001278]">이번 달 지출 요약</p>
        <h2 class="mt-1 text-xl font-extrabold text-gray-950">소비 패턴 기반 추천 데이터</h2>
        <p class="mt-2 text-sm text-gray-500">
          저장된 설문과 CSV 데이터를 바탕으로 주요 소비 카테고리를 정리했습니다.
        </p>
      </div>
      <div class="rounded-xl bg-[#eef1ff] px-5 py-4 text-right">
        <p class="text-xs font-bold text-[#4254b8]">총 지출</p>
        <p class="mt-1 text-2xl font-extrabold text-[#001278]">{{ formattedTotal }}</p>
      </div>
    </div>

    <div class="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <article
        v-for="item in categoryItems"
        :key="item.key"
        class="rounded-xl bg-gray-50 p-4"
      >
        <p class="text-xs font-bold uppercase tracking-wide text-gray-400">{{ item.label }}</p>
        <p class="mt-2 text-lg font-extrabold text-gray-950">{{ formatCurrency(item.value) }}</p>
      </article>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  report: {
    type: Object,
    default: null,
  },
  categoryLabels: {
    type: Object,
    default: () => ({}),
  },
})

const categoryItems = computed(() => {
  return Object.entries(props.report?.categories || {}).map(([key, value]) => ({
    key,
    value,
    label: props.categoryLabels[key] || key,
  }))
})

const formattedTotal = computed(() => formatCurrency(props.report?.total_monthly || 0))

function formatCurrency(value) {
  return new Intl.NumberFormat('ko-KR', {
    style: 'currency',
    currency: 'KRW',
    maximumFractionDigits: 0,
  }).format(value || 0)
}
</script>
