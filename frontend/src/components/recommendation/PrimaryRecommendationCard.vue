<template>
  <article class="rounded-xl border border-[#e5e0dd] bg-white p-8 shadow-[0_18px_52px_rgba(0,18,120,0.08)]">
    <div class="grid gap-8 md:grid-cols-[1fr_0.92fr]">
      <div class="flex min-h-72 items-center justify-center rounded-lg bg-gradient-to-br from-[#f4f5f2] via-[#e6ebe9] to-[#cfd8d3] p-8">
        <img
          v-if="card.image_url && !imageFailed"
          :src="card.image_url"
          :alt="card.card_name"
          class="max-h-52 w-full max-w-72 object-contain drop-shadow-[0_22px_24px_rgba(0,0,0,0.22)]"
          @error="imageFailed = true"
        />
        <div
          v-else
          class="flex h-40 w-64 items-end rounded-xl bg-[#001278] p-5 text-lg font-extrabold text-white shadow-2xl"
        >
          {{ card.card_name }}
        </div>
      </div>

      <div class="flex flex-col justify-center">
        <div class="mb-4 inline-flex w-fit items-center gap-2 rounded-full bg-[#e7e9ff] px-4 py-2 text-[11px] font-extrabold uppercase tracking-[0.08em] text-[#001278]">
          최대 절약 추천
          <span class="normal-case tracking-normal">소비 패턴 적합도 {{ recommendation.score }}%</span>
        </div>
        <p class="text-sm font-bold text-[#001278]">{{ card.card_company || 'CardFit 추천' }}</p>
        <h2 class="mt-1 text-3xl font-extrabold leading-tight text-gray-950">{{ card.card_name }}</h2>
        <p class="mt-3 rounded-lg border border-[#dfe3ff] bg-white px-4 py-3 text-xs font-bold leading-5 text-gray-600">
          추천 순위는 예상 절약 금액과 연 순혜택을 우선 반영하고, 소비 패턴 적합도는 혜택 커버 범위와 전월실적 조건까지 함께 봅니다.
          <span v-if="hasHigherScoreAlternative" class="text-[#001278]">
            그래서 절약 금액은 이 카드가 더 커도, 다른 카드의 적합도가 더 높게 보일 수 있습니다.
          </span>
        </p>
        <p class="mt-3 rounded-lg bg-[#eef1ff] px-4 py-3 text-xs font-bold leading-5 text-[#001278]">
          {{ recommendation.scoreReason }}
        </p>
        <p class="mt-4 text-sm leading-6 text-gray-500">{{ recommendation.reason }}</p>

        <div class="mt-6 rounded-lg bg-[#f2eeee] p-6">
          <p class="text-xs font-bold text-gray-500">예상 절약 금액</p>
          <p class="mt-2 text-lg font-extrabold text-[#001278]">월 평균</p>
          <p class="mt-1 text-4xl font-extrabold leading-tight text-[#001278]">
            {{ recommendation.expected_monthly_benefit }}
          </p>
          <p class="mt-1 text-lg font-extrabold text-[#001278]">절약 가능</p>
        </div>
      </div>
    </div>

    <div class="my-8 h-px bg-[#ece7e3]"></div>

    <section>
      <h3 class="text-lg font-extrabold text-gray-950">맞춤 혜택 요약</h3>
      <div class="mt-5 grid gap-4 sm:grid-cols-3">
        <article
          v-for="benefit in benefits"
          :key="benefit.title"
          class="rounded-lg border border-[#eee9e5] bg-[#fbfaf9] p-5"
        >
          <div class="mb-5 flex h-9 w-9 items-center justify-center rounded-full bg-[#eef1ff] text-sm font-black text-[#001278]">
            {{ benefit.initial }}
          </div>
          <p class="text-sm font-extrabold text-gray-950">{{ benefit.title }}</p>
          <p class="mt-2 text-xl font-extrabold leading-tight text-[#001278]">{{ benefit.rate }}</p>
          <p class="mt-2 text-xs leading-5 text-gray-500">{{ benefit.description }}</p>
        </article>
      </div>
    </section>

    <div class="mt-8 grid gap-3 sm:grid-cols-2">
      <a
        :href="card.apply_url || '#'"
        target="_blank"
        rel="noreferrer"
        class="inline-flex h-14 items-center justify-center rounded-lg bg-[#001278] px-5 text-sm font-extrabold text-white transition hover:bg-[#1428a0]"
      >
        알아보러 가기
      </a>
      <RouterLink
        :to="{ name: 'card-detail', params: { id: card.id || recommendation.card_id } }"
        class="inline-flex h-14 items-center justify-center rounded-lg border border-[#001278] px-5 text-sm font-extrabold text-[#001278] transition hover:bg-[#eef1ff]"
      >
        카드 상세 보기
      </RouterLink>
    </div>
  </article>
</template>

<script setup>
import { ref, watch } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  recommendation: {
    type: Object,
    required: true,
  },
  card: {
    type: Object,
    required: true,
  },
  benefits: {
    type: Array,
    default: () => [],
  },
  hasHigherScoreAlternative: {
    type: Boolean,
    default: false,
  },
})

const imageFailed = ref(false)

watch(
  () => props.card?.id,
  () => {
    imageFailed.value = false
  },
)
</script>
