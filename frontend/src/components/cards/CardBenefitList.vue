<template>
  <section class="mx-auto max-w-7xl px-5 py-16 md:px-10 lg:px-20">
    <div class="mb-10 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
      <h2 class="text-3xl font-extrabold text-black">상세 혜택 안내</h2>
      <p class="text-sm text-zinc-500">* 전월 이용금액 {{ formatPrevSpending(minPrevMonthSpending) }} 시 제공</p>
    </div>

    <div class="grid gap-6 md:grid-cols-2 xl:grid-cols-6">
      <article
        v-for="(benefit, index) in benefits"
        :key="benefit.id"
        class="rounded-xl border p-8 shadow-sm"
        :class="getBenefitCardClass(benefit, index)"
      >
        <div class="flex items-start justify-between gap-4">
          <div class="min-w-0 flex-1">
            <div
              class="mb-5 flex h-10 w-10 items-center justify-center rounded-md"
              :class="benefit.tone === 'blue' ? 'bg-white/10 text-blue-100' : 'bg-indigo-100 text-blue-950'"
            >
              <BenefitCategoryIcon :type="benefit.icon" />
            </div>
            <h3 class="text-lg font-bold">{{ benefit.title }}</h3>
            <p
              class="mt-2 text-sm leading-6"
              :class="benefit.tone === 'blue' ? 'text-blue-100' : 'text-zinc-500'"
            >
              {{ benefit.description }}
            </p>
          </div>
          <span
            v-if="benefit.tone !== 'blue'"
            class="rounded-full bg-indigo-100 px-3 py-1 text-xs font-medium text-blue-900"
          >
            {{ benefit.rate }}
          </span>
        </div>

        <div
          class="mt-10 grid grid-cols-2 gap-5 border-t pt-6"
          :class="benefit.tone === 'blue' ? 'border-white/20' : 'border-zinc-200'"
        >
          <div>
            <p :class="benefit.tone === 'blue' ? 'text-sm text-blue-100' : 'text-sm text-zinc-500'">월 한도</p>
            <p class="mt-1 font-bold">{{ benefit.limit }}</p>
          </div>
          <div>
            <p :class="benefit.tone === 'blue' ? 'text-sm text-blue-100' : 'text-sm text-zinc-500'">주요 조건</p>
            <p class="mt-1 font-bold">{{ benefit.condition }}</p>
          </div>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup>
import BenefitCategoryIcon from './BenefitCategoryIcon.vue'

const props = defineProps({
  benefits: {
    type: Array,
    default: () => [],
  },
  minPrevMonthSpending: {
    type: Number,
    default: 0,
  },
})

function formatPrevSpending(value) {
  if (!value) return '조건 없음'
  return `${Math.floor(Number(value) / 10000)}만원 이상`
}

function getBenefitCardClass(benefit, index) {
  const total = props.benefits.length
  const mdSpan = total % 2 === 1 && index === total - 1 ? 'md:col-span-2' : 'md:col-span-1'
  let xlSpan = 'xl:col-span-2'

  if (total % 3 === 1 && index === total - 1) {
    xlSpan = 'xl:col-span-6'
  } else if (total % 3 === 2 && index >= total - 2) {
    xlSpan = 'xl:col-span-3'
  }

  const toneClass =
    benefit.tone === 'blue'
      ? 'border-blue-950 bg-blue-900 text-white'
      : 'border-zinc-200 bg-white text-zinc-950'

  return `${toneClass} ${mdSpan} ${xlSpan}`
}
</script>
