<template>
  <section class="min-h-screen bg-[#fbf9f8] px-4 py-10 md:px-10 lg:px-20">
    <div class="mx-auto max-w-6xl">
      <header class="max-w-3xl">
        <h1 class="text-3xl font-extrabold text-gray-950 md:text-4xl">AI가 분석한 최적의 카드입니다</h1>
        <p class="mt-4 text-sm leading-6 text-gray-600">
          최근 3개월간의 소비 패턴을 분석한 결과,
          <strong class="font-extrabold text-[#001278]">{{ strongestCategoryLabel }}</strong>
          비중이 가장 높았습니다. 당신의 소비 습관에 가장 큰 혜택을 줄 카드를 확인해보세요.
        </p>
      </header>

      <div class="mt-12 grid gap-8 lg:grid-cols-[1.35fr_0.9fr]">
        <article class="rounded-xl border border-[#e5e0dd] bg-white p-8 shadow-[0_18px_52px_rgba(0,18,120,0.08)]">
          <div class="grid gap-8 md:grid-cols-[1fr_0.92fr]">
            <div class="flex min-h-72 items-center justify-center rounded-lg bg-gradient-to-br from-[#f4f5f2] via-[#e6ebe9] to-[#cfd8d3] p-8">
              <img
                v-if="primaryCard.image_url"
                :src="primaryCard.image_url"
                :alt="primaryCard.card_name"
                class="max-h-52 w-full max-w-72 object-contain drop-shadow-[0_22px_24px_rgba(0,0,0,0.22)]"
              />
              <div
                v-else
                class="flex h-40 w-64 items-end rounded-xl bg-[#001278] p-5 text-lg font-extrabold text-white shadow-2xl"
              >
                {{ primaryCard.card_name }}
              </div>
            </div>

            <div class="flex flex-col justify-center">
              <div class="mb-4 inline-flex w-fit items-center gap-2 rounded-full bg-[#e7e9ff] px-4 py-2 text-[11px] font-extrabold uppercase tracking-[0.08em] text-[#001278]">
                Best Match
                <span class="normal-case tracking-normal">Match Score 98%</span>
              </div>
              <p class="text-sm font-bold text-[#001278]">{{ primaryCard.card_company || 'CardFit 추천' }}</p>
              <h2 class="mt-1 text-3xl font-extrabold leading-tight text-gray-950">{{ primaryCard.card_name }}</h2>
              <p class="mt-4 text-sm leading-6 text-gray-500">{{ primaryRecommendation.reason }}</p>

              <div class="mt-6 rounded-lg bg-[#f2eeee] p-6">
                <p class="text-xs font-bold text-gray-500">예상 절약 금액</p>
                <p class="mt-2 text-lg font-extrabold text-[#001278]">월 평균</p>
                <p class="mt-1 text-4xl font-extrabold leading-tight text-[#001278]">
                  {{ primaryRecommendation.expected_monthly_benefit.replace('월 ', '') }}
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
                v-for="benefit in primaryBenefits"
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
              :href="primaryCard.apply_url || '#'"
              target="_blank"
              rel="noreferrer"
              class="inline-flex h-14 items-center justify-center rounded-lg bg-[#001278] px-5 text-sm font-extrabold text-white transition hover:bg-[#1428a0]"
            >
              알아보러 가기
            </a>
            <RouterLink
              :to="{ name: 'card-detail', params: { id: primaryCard.id || primaryRecommendation.card_id } }"
              class="inline-flex h-14 items-center justify-center rounded-lg border border-[#001278] px-5 text-sm font-extrabold text-[#001278] transition hover:bg-[#eef1ff]"
            >
              카드 상세 보기
            </RouterLink>
          </div>
        </article>

        <aside class="space-y-7">
          <section>
            <h3 class="text-lg font-extrabold text-gray-950">다른 추천 카드</h3>
            <div class="mt-5 space-y-5">
              <RouterLink
                v-for="card in secondaryCards"
                :key="card.card_id"
                :to="{ name: 'card-detail', params: { id: card.detail.id || card.card_id } }"
                class="grid grid-cols-[88px_1fr_auto] items-center gap-4 rounded-lg border border-[#ebe5e0] bg-white p-4 shadow-[0_8px_24px_rgba(0,18,120,0.04)] transition hover:-translate-y-0.5 hover:border-[#001278]/30"
              >
                <div class="flex h-16 items-center justify-center rounded bg-[#eef2f5] px-2">
                  <img
                    v-if="card.detail.image_url"
                    :src="card.detail.image_url"
                    :alt="card.detail.card_name"
                    class="max-h-12 max-w-full object-contain"
                  />
                </div>
                <div class="min-w-0">
                  <p class="truncate text-sm font-extrabold text-gray-950">{{ card.detail.card_name || card.card_name }}</p>
                  <p class="mt-1 truncate text-xs text-[#001278]">{{ card.benefitText }}</p>
                  <p class="mt-1 text-xs font-extrabold text-[#001278]">{{ card.expected_monthly_benefit }} 절약</p>
                </div>
                <span class="rounded bg-[#eef1ff] px-2 py-1 text-[11px] font-extrabold text-[#001278]">
                  {{ card.score }}%
                </span>
              </RouterLink>
            </div>
          </section>

          <section class="rounded-xl border border-[#e5e0dd] bg-white p-7 shadow-[0_14px_36px_rgba(0,18,120,0.06)]">
            <h3 class="text-lg font-extrabold text-gray-950">소비 데이터 분석</h3>
            <div class="mt-6 space-y-5">
              <div v-for="item in analysisBars" :key="item.category">
                <div class="mb-2 flex items-center justify-between text-xs font-bold text-gray-950">
                  <span>{{ item.label }}</span>
                  <span>{{ item.ratio }}%</span>
                </div>
                <div class="h-2 rounded-full bg-[#e2e2e2]">
                  <div class="h-2 rounded-full bg-[#001278]" :style="{ width: `${item.ratio}%` }"></div>
                </div>
              </div>
            </div>
            <p class="mt-8 text-xs text-gray-500">분석 기간: 2024.01.01 ~ 2024.03.31</p>
          </section>
        </aside>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { cardData } from '../data/cardData'
import { mockAiRecommendations, mockAiReport } from '../data/mockReportData'

const recommendations = mockAiRecommendations

const resolvedRecommendations = computed(() =>
  recommendations.map((recommendation, index) => {
    const detail = findCardDetail(recommendation)
    return {
      ...recommendation,
      detail,
      score: index === 0 ? 98 : index === 1 ? 92 : 85,
      benefitText: getBenefitText(detail),
    }
  }),
)

const primaryRecommendation = computed(() => resolvedRecommendations.value[0])
const primaryCard = computed(() => primaryRecommendation.value.detail)
const secondaryCards = computed(() => resolvedRecommendations.value.slice(1, 3))

const strongestCategoryLabel = computed(() => analysisBars.value[0]?.label || '주요 소비')

const analysisBars = computed(() =>
  [...(mockAiReport.category_breakdown || [])]
    .sort((a, b) => Number(b.ratio) - Number(a.ratio))
    .slice(0, 3)
    .map((item) => ({
      ...item,
      ratio: Math.round(Number(item.ratio || 0)),
    })),
)

const primaryBenefits = computed(() => {
  const benefits = primaryCard.value?.benefits || []

  return benefits.slice(0, 3).map((benefit) => ({
    title: benefitTitleMap[benefit.benefit_category] || '생활 혜택',
    initial: benefitInitialMap[benefit.benefit_category] || 'C',
    rate: `${Number(benefit.discount_rate || 0)}% ${benefit.benefit_type === 'point' ? '적립' : benefit.benefit_type === 'mileage' ? '마일리지' : '할인'}`,
    description: benefit.condition_description || '소비 패턴에 맞춘 혜택',
  }))
})

const benefitTitleMap = {
  food: 'Food & Beverage',
  transport: 'Transport',
  shopping: 'Shopping',
  communication: 'Communication',
  fuel: 'Fuel',
  travel: 'Travel',
  health: 'Health',
  other: 'Life',
}

const benefitInitialMap = {
  food: 'F',
  transport: 'T',
  shopping: 'S',
  communication: 'C',
  fuel: 'G',
  travel: 'M',
  health: 'H',
  other: 'L',
}

function findCardDetail(recommendation) {
  const normalizedName = normalizeCardName(recommendation.card_name)
  const byName = cardData.find((card) => normalizeCardName(card.card_name) === normalizedName)
  const byId = cardData.find((card) => card.id === recommendation.card_id)

  return byName || byId || {
    id: recommendation.card_id,
    card_company: '삼성카드',
    card_name: recommendation.card_name,
    image_url: '',
    apply_url: '',
    benefits: [],
  }
}

function normalizeCardName(value) {
  return String(value || '')
    .toLowerCase()
    .replace(/삼성카드|삼성/g, '')
    .replace(/카드/g, '')
    .replace(/\s+/g, '')
}

function getBenefitText(card) {
  const benefit = card?.benefits?.[0]
  if (!benefit) return '맞춤 생활 혜택'

  const title = benefitTitleMap[benefit.benefit_category] || '생활'
  return `${title} ${Number(benefit.discount_rate || 0)}% 혜택`
}
</script>
