<template>
  <section class="border-b border-zinc-200 bg-white/70 px-5 py-12 md:px-10 lg:px-20">
    <div class="mx-auto max-w-7xl rounded-xl border border-blue-100 bg-white p-8 shadow-sm">
      <div class="grid gap-8 lg:grid-cols-[260px_1fr]">
        <div>
          <div class="flex items-center gap-3">
            <div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-indigo-100 text-xl text-blue-900">
              AI
            </div>
            <div>
              <p class="text-xs font-extrabold uppercase tracking-[0.16em] text-blue-700">Spending Match</p>
              <h2 class="mt-1 text-lg font-bold text-blue-950">소비 데이터 분석</h2>
            </div>
          </div>

          <div class="mt-6 flex justify-center">
            <div
              class="grid h-40 w-40 place-items-center rounded-full"
              :style="{ background: `conic-gradient(#001278 ${coverageRatio * 3.6}deg, #e8ecff 0deg)` }"
            >
              <div class="grid h-28 w-28 place-items-center rounded-full bg-white text-center shadow-inner">
                <div>
                  <p class="text-xs font-bold text-zinc-500">혜택 적중률</p>
                  <p class="mt-1 text-3xl font-extrabold text-blue-950">{{ coverageRatio }}%</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="space-y-6">
          <p class="rounded-lg bg-[#f0f3ff] px-4 py-3 text-sm font-bold leading-6 text-[#001278]">
            {{ insight }}
          </p>

          <div class="grid gap-4 md:grid-cols-3">
            <article class="rounded-lg bg-[#f8f9fc] p-5">
              <p class="text-xs font-bold text-zinc-500">혜택 적용 소비</p>
              <p class="mt-2 text-2xl font-extrabold text-blue-950">{{ formatWon(coveredSpending) }}</p>
              <p class="mt-1 text-xs font-semibold text-zinc-500">전체 소비 중 카드 혜택과 겹치는 금액</p>
            </article>

            <article class="rounded-lg bg-[#f8f9fc] p-5">
              <p class="text-xs font-bold text-zinc-500">예상 월 혜택</p>
              <p class="mt-2 text-2xl font-extrabold text-blue-950">{{ formatWon(monthlyBenefit) }}</p>
              <p class="mt-1 text-xs font-semibold text-zinc-500">현재 소비 기준 예상 절약액</p>
            </article>

            <article class="rounded-lg bg-[#f8f9fc] p-5">
              <p class="text-xs font-bold text-zinc-500">주요 매칭 영역</p>
              <p class="mt-2 text-lg font-extrabold text-blue-950">{{ topMatchedLabels }}</p>
              <p class="mt-1 text-xs font-semibold text-zinc-500">카드 혜택과 소비가 만나는 카테고리</p>
            </article>
          </div>

          <div class="rounded-lg border border-blue-100 bg-white p-5">
            <div class="flex flex-wrap items-center justify-between gap-3">
              <div>
                <p class="text-sm font-bold text-blue-950">전월 실적 충족률</p>
                <p class="mt-1 text-xs font-semibold text-zinc-500">
                  현재 월 소비 {{ formatWon(totalSpending) }} / 필요 실적 {{ formatWon(minPrevMonthSpending) }}
                </p>
              </div>
              <p class="text-2xl font-extrabold text-blue-950">{{ prevProgressRatio }}%</p>
            </div>

            <div class="mt-4 h-3 overflow-hidden rounded-full bg-[#e8ecff]">
              <div
                class="h-full rounded-full bg-[#001278] transition-all"
                :style="{ width: `${Math.min(prevProgressRatio, 100)}%` }"
              ></div>
            </div>

            <p class="mt-3 text-xs font-semibold text-zinc-500">
              {{ prevProgressText }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  coverageRatio: {
    type: Number,
    default: 0,
  },
  coveredSpending: {
    type: Number,
    default: 0,
  },
  totalSpending: {
    type: Number,
    default: 0,
  },
  monthlyBenefit: {
    type: Number,
    default: 0,
  },
  minPrevMonthSpending: {
    type: Number,
    default: 0,
  },
  matchedLabels: {
    type: Array,
    default: () => [],
  },
  insight: {
    type: String,
    default: '',
  },
})

const topMatchedLabels = computed(() => props.matchedLabels.slice(0, 3).join(', ') || '매칭 혜택 없음')
const prevProgressRatio = computed(() => {
  if (!props.minPrevMonthSpending) return 100
  return Math.round((props.totalSpending / props.minPrevMonthSpending) * 100)
})
const prevProgressText = computed(() => {
  if (!props.minPrevMonthSpending) return '이 카드는 별도 전월 실적 조건 없이 사용할 수 있습니다.'
  if (prevProgressRatio.value >= 100) return '현재 소비 기준으로 전월 실적 조건을 충분히 충족할 가능성이 높습니다.'
  return `현재 소비 기준으로 필요 실적까지 ${formatWon(props.minPrevMonthSpending - props.totalSpending)} 남았습니다.`
})

function formatWon(value) {
  return `${Math.max(0, Math.round(Number(value || 0))).toLocaleString('ko-KR')}원`
}
</script>
