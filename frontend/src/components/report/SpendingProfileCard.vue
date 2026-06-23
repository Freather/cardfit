<template>
  <section class="rounded-xl border border-[#e0e0e0] bg-white p-7 shadow-[0_4px_12px_rgba(0,0,0,0.05)]">
    <p class="text-sm font-semibold text-gray-500">소비 성향</p>
    <div class="mt-5 space-y-4">
      <div class="flex items-center justify-between text-sm">
        <span class="font-semibold text-gray-800">주요 소비</span>
        <span class="text-[#001278]">{{ primarySpendingLabel }}</span>
      </div>
      <div class="flex items-center justify-between text-sm">
        <span class="font-semibold text-gray-800">소득 구간</span>
        <span class="text-gray-600">{{ incomeLabel }}</span>
      </div>
      <div class="flex items-center justify-between text-sm">
        <span class="font-semibold text-gray-800">연령대</span>
        <span class="text-gray-600">{{ ageLabel }}</span>
      </div>
      <div class="rounded-2xl bg-amber-50 p-4 text-sm leading-6 text-amber-900">
        고정비보다 변동 지출 비중이 커서 생활 영역별 할인 조건을 맞추기 좋은 패턴입니다.
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  primarySpendingLabel: {
    type: String,
    required: true,
  },
  incomeLabel: {
    type: String,
    required: true,
  },
  ageLabel: {
    type: String,
    required: true,
  },
})
</script>
