<template>
  <section class="rounded-xl border border-[#e0e0e0] bg-white shadow-[0_4px_12px_rgba(0,0,0,0.05)]">
    <div class="grid lg:grid-cols-[0.82fr_1fr]">
      <div class="p-8">
        <div class="flex flex-col items-center gap-8">
          <div class="relative h-80 w-80 max-w-full">
            <div class="relative z-10 h-full w-full">
              <SpendingDoughnutChart
                :chart-data="chartData"
                :chart-options="chartOptions"
              />
            </div>
            <div class="pointer-events-none absolute left-1/2 top-1/2 z-0 flex h-36 w-36 -translate-x-1/2 -translate-y-1/2 flex-col items-center justify-center rounded-full bg-white text-center">
              <p class="text-sm text-gray-500">총 지출</p>
              <p class="mt-1 text-xl font-extrabold text-gray-950">{{ totalAmountLabel }}</p>
            </div>
          </div>

          <div class="grid w-full gap-3 sm:grid-cols-2">
            <div
              v-for="category in categories"
              :key="category.category"
              class="flex items-center justify-between gap-3 rounded-lg bg-[#fbf9f8] px-4 py-3 text-left transition hover:-translate-y-0.5 hover:bg-[#eef1ff] focus:outline-none focus:ring-2 focus:ring-[#001278]/30"
              role="button"
              tabindex="0"
              @click="emit('select-category', category)"
              @keydown.enter.prevent="emit('select-category', category)"
              @keydown.space.prevent="emit('select-category', category)"
            >
              <div class="flex min-w-0 items-center gap-2">
                <span
                  class="h-3 w-3 shrink-0 rounded-full"
                  :style="{ backgroundColor: category.color }"
                ></span>
                <span class="truncate text-sm font-semibold text-gray-800">{{ category.label }}</span>
              </div>
              <span class="shrink-0 text-sm font-bold text-gray-700">{{ formatRatio(category.ratio) }}%</span>
            </div>
          </div>
        </div>
      </div>

      <div class="p-8">
        <div class="mb-6">
          <h2 class="text-xl font-bold text-gray-950">카테고리 상세</h2>
          <p class="mt-1 text-sm text-gray-500">
            지출 금액과 분석 코멘트를 확인해보세요. 하단 카테고리를 눌러 내역을 확인할 수 있습니다.
          </p>
        </div>

        <div class="space-y-4">
          <article
            v-for="category in categories"
            :key="`detail-${category.category}`"
            class="rounded-xl border border-[#e0e0e0] p-5 text-left transition hover:-translate-y-0.5 hover:border-[#001278]/30 hover:shadow-[0_10px_24px_rgba(0,18,120,0.08)] focus:outline-none focus:ring-2 focus:ring-[#001278]/30"
            role="button"
            tabindex="0"
            @click="emit('select-category', category)"
            @keydown.enter.prevent="emit('select-category', category)"
            @keydown.space.prevent="emit('select-category', category)"
          >
            <div class="flex items-start justify-between gap-4">
              <div class="flex items-center gap-3">
                <span
                  class="h-4 w-4 rounded-full"
                  :style="{ backgroundColor: category.color }"
                ></span>
                <div>
                  <h3 class="font-bold text-gray-950">{{ category.label }}</h3>
                  <p class="mt-1 text-sm text-gray-500">{{ category.insight }}</p>
                </div>
              </div>
              <div class="shrink-0 text-right">
                <p class="font-bold text-gray-950">{{ formatCurrency(category.total) }}</p>
                <p class="mt-1 text-sm text-gray-500">{{ formatRatio(category.ratio) }}%</p>
              </div>
            </div>
          </article>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import SpendingDoughnutChart from './SpendingDoughnutChart.vue'

defineProps({
  categories: {
    type: Array,
    default: () => [],
  },
  chartData: {
    type: Object,
    required: true,
  },
  chartOptions: {
    type: Object,
    required: true,
  },
  totalAmountLabel: {
    type: String,
    required: true,
  },
})

const emit = defineEmits(['select-category'])

function formatCurrency(value) {
  return new Intl.NumberFormat('ko-KR', {
    style: 'currency',
    currency: 'KRW',
    maximumFractionDigits: 0,
  }).format(value || 0)
}

function formatRatio(value) {
  return Number(value || 0).toLocaleString('ko-KR', {
    maximumFractionDigits: 1,
  })
}
</script>
