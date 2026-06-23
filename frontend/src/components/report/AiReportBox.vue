<template>
  <section class="rounded-xl border border-[#e0e0e0] bg-white p-7 shadow-[0_4px_12px_rgba(0,0,0,0.05)]">
    <div class="flex flex-col gap-5 md:flex-row md:items-start md:justify-between">
      <div>
        <p class="text-sm font-semibold text-[#001278]">AI 분석 요약</p>
        <h2 class="mt-2 text-2xl font-bold text-gray-950">생활 할인형 카드가 가장 유리합니다</h2>
        <p class="mt-4 max-w-3xl text-sm leading-6 text-gray-600">{{ summary }}</p>
      </div>
      <div class="rounded-2xl bg-[#001278] px-5 py-4 text-white">
        <p class="text-xs text-blue-200">총 지출</p>
        <p class="mt-1 text-2xl font-bold">{{ totalAmountLabel }}</p>
      </div>
    </div>

    <div class="mt-8 grid gap-4 sm:grid-cols-3">
      <div class="rounded-2xl bg-gray-50 p-5">
        <p class="text-sm text-gray-500">가장 큰 지출</p>
        <p class="mt-2 text-2xl font-bold text-gray-950">{{ topCategoryLabel }}</p>
      </div>
      <div class="rounded-2xl bg-gray-50 p-5">
        <p class="text-sm text-gray-500">최대 비중</p>
        <p class="mt-2 text-2xl font-bold text-gray-950">{{ topCategoryRatio }}%</p>
      </div>
      <div class="rounded-2xl bg-gray-50 p-5">
        <p class="text-sm text-gray-500">분석 카테고리</p>
        <p class="mt-2 text-2xl font-bold text-gray-950">{{ categoryCount }}개</p>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  summary: {
    type: String,
    default: '',
  },
  totalAmountLabel: {
    type: String,
    required: true,
  },
  topCategoryLabel: {
    type: String,
    required: true,
  },
  topCategoryRatio: {
    type: String,
    required: true,
  },
  categoryCount: {
    type: Number,
    default: 0,
  },
})
</script>
