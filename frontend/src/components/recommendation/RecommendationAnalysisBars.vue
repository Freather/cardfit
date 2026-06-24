<template>
  <section class="rounded-xl border border-[#e5e0dd] bg-white p-7 shadow-[0_14px_36px_rgba(0,18,120,0.06)]">
    <h3 class="text-lg font-extrabold text-gray-950">소비 데이터 분석</h3>
    <div class="mt-6 space-y-5">
      <div v-for="item in items" :key="item.category">
        <div class="mb-2 flex items-center justify-between text-xs font-bold text-gray-950">
          <span>{{ item.label }}</span>
          <span>{{ item.ratio }}%</span>
        </div>
        <div class="h-2 rounded-full bg-[#e2e2e2]">
          <div class="h-2 rounded-full bg-[#001278]" :style="{ width: `${item.ratio}%` }"></div>
        </div>
      </div>
    </div>
    <p class="mt-8 text-xs text-gray-500">분석 기간: {{ periodLabel }}</p>
  </section>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    default: () => [],
  },
  periodLabel: {
    type: String,
    default: '-',
  },
})
</script>
