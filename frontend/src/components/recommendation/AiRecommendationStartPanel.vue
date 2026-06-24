<template>
  <section class="mx-auto mt-10 max-w-3xl rounded-xl border border-[#e0e0e0] bg-white/85 p-8 shadow-[0_18px_60px_rgba(0,18,120,0.08)] backdrop-blur md:mt-12">
    <template v-if="loading">
      <p class="rounded-lg bg-[#f0f3ff] px-4 py-3 text-center text-sm font-bold text-[#001278]">
        소비 분석 데이터를 정리하는 중입니다...
      </p>

      <div class="mt-8">
        <SkeletonBlock custom-class="h-10 w-56" />
        <SkeletonBlock custom-class="mt-4 h-4 w-full max-w-xl" />
      </div>

      <div class="mt-8 grid gap-5 sm:grid-cols-2">
        <article
          v-for="index in 4"
          :key="index"
          class="skeleton-card flex items-center justify-between rounded-lg bg-[#f6f7fb] px-5 py-4"
        >
          <div class="flex items-center gap-3">
            <SkeletonBlock custom-class="h-6 w-6 rounded-full" />
            <SkeletonBlock custom-class="h-5 w-24" />
          </div>
          <SkeletonBlock custom-class="h-6 w-20" />
        </article>
      </div>

      <div class="mt-12 flex justify-center">
        <SkeletonBlock custom-class="h-16 w-80 rounded-lg" />
      </div>
    </template>

    <template v-else>
      <div class="rounded-lg bg-[#f0f3ff] px-4 py-3 text-center text-sm font-bold text-[#4254b8]">
        사용자의 최근 소비 데이터를 바탕으로 분석되었습니다.
      </div>

      <div class="mt-8">
        <h2 class="text-3xl font-extrabold text-[#001278]">AI 맞춤 분석</h2>
      </div>

      <div class="mt-8 grid gap-5 sm:grid-cols-2">
        <article
          v-for="item in analysisItems"
          :key="item.key"
          class="flex items-center justify-between rounded-lg bg-[#f6f7fb] px-5 py-4"
        >
          <div class="flex items-center gap-3">
            <span class="text-xl">{{ item.icon }}</span>
            <span class="text-base font-bold text-[#001278]">{{ item.label }}</span>
          </div>
          <span class="text-lg font-extrabold text-[#001278]">{{ formatCompactWon(item.amount) }}</span>
        </article>
      </div>

      <div class="mt-12 flex justify-center">
        <RouterLink
          :to="{ name: 'ai-recommendations-result' }"
          class="inline-flex h-16 min-w-80 items-center justify-center rounded-lg bg-[#001278] px-8 text-base font-extrabold text-white shadow-[0_14px_32px_rgba(0,18,120,0.24)] transition hover:bg-[#1428a0]"
        >
          맞춤 카드 추천 시작
        </RouterLink>
      </div>
    </template>
  </section>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import SkeletonBlock from '../common/SkeletonBlock.vue'

defineProps({
  analysisItems: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

function formatCompactWon(value) {
  return `${Math.round(Number(value || 0) / 10000)}만원`
}
</script>

<style scoped>
.skeleton-card {
  animation: card-drift 2.8s ease-in-out infinite;
}

.skeleton-card:nth-child(2),
.skeleton-card:nth-child(3) {
  animation-delay: 0.18s;
}

.skeleton-card:nth-child(4) {
  animation-delay: 0.34s;
}

@keyframes card-drift {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-3px);
  }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton-card {
    animation: none;
  }
}
</style>
