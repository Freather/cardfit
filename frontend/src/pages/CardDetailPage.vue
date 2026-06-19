<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

import { cardData } from '../data/cardData'
import { getBenefitCategoryLabel } from '../data/benefitData'
import { useCompareStore } from '../stores/compareStore'

const props = defineProps({
  id: {
    type: [String, Number],
    default: null,
  },
})

const compareStore = useCompareStore()

const card = computed(() => {
  return cardData.find((item) => String(item.id) === String(props.id)) || cardData[1] || cardData[0]
})

const detailBenefits = computed(() => {
  const baseBenefits = card.value?.benefits || []
  const mappedBenefits = baseBenefits.map((benefit) => ({
    id: benefit.id,
    title: `${getBenefitCategoryLabel(benefit.benefit_category)} 할인`,
    rate: `${Number(benefit.discount_rate)}% 할인`,
    description: benefit.condition_description || '주요 생활 영역 혜택',
    limit: benefit.monthly_limit ? `최대 ${formatWon(benefit.monthly_limit)}원` : '제한 없음',
    condition: formatPrevSpending(card.value.min_prev_month_spending),
    tone: 'light',
  }))

  return [
    ...mappedBenefits,
    {
      id: 'digital',
      title: '디지털 구독',
      rate: '50% 할인',
      description: '넷플릭스, 유튜브 프리미엄, 웨이브',
      limit: '5,000원',
      condition: '전월 실적 30만원 이상',
      tone: 'light',
    },
    {
      id: 'online',
      title: '온라인 쇼핑 / 간편 결제',
      rate: '1.5% 적립',
      description: '네이버페이, 카카오페이, 쿠팡, 마켓컬리 등 온라인 가맹점 자동 적립',
      limit: '무제한',
      condition: '실적 조건 충족 시',
      tone: 'blue',
    },
  ].slice(0, 4)
})

const conditionRows = [
  {
    label: '전월 실적 산정 기준',
    value: '전월 1일부터 말일까지 이용한 일시불 및 할부 합계 금액. 단, 무이자할부 및 국세/지방세 등은 제외됩니다.',
  },
  {
    label: '할인 적용 방식',
    value: '결제 시 할인되는 방식이 아닌, 결제 후 결제일에 할인된 금액이 청구되는 청구할인 방식입니다.',
  },
  {
    label: '해외 이용 수수료',
    value: 'Mastercard/Visa 브랜드 수수료 1.0% + 삼성카드 서비스 수수료 0.2%가 합산 청구됩니다.',
  },
  {
    label: '포인트 유효기간',
    value: '적립일로부터 5년이며, 기간 경과 시 월 단위로 자동 소멸됩니다.',
  },
]

const aiKeywords = ['배달 앱', '스트리밍 서비스', '생활비 결제']

function formatWon(value) {
  return new Intl.NumberFormat('ko-KR').format(Number(value || 0))
}

function formatPrevSpending(value) {
  if (!value) return '조건 없음'
  return `${Math.floor(value / 10000)}만원 이상`
}

function handleAddCompare() {
  compareStore.addCard(card.value)
}
</script>

<template>
  <div class="min-h-screen bg-[#faf9f8] text-zinc-950">
    <section class="border-b border-zinc-200 bg-[#fbfaf9]">
      <div class="relative mx-auto grid max-w-7xl gap-12 px-5 py-14 md:px-10 lg:grid-cols-[430px_1fr] lg:px-20">
        <RouterLink
          to="/cards"
          class="absolute right-5 top-6 text-sm font-semibold text-zinc-500 transition hover:text-blue-800 md:right-10 lg:right-20"
        >
          목록으로
        </RouterLink>

        <div class="flex justify-center lg:justify-start">
          <div
            class="relative h-[330px] w-[390px] rotate-[-6deg] overflow-hidden rounded-xl bg-[#061018] shadow-2xl shadow-zinc-300"
          >
            <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,#1d5260_0%,#07151b_45%,#030609_100%)]" />
            <div class="absolute left-16 top-28 h-24 w-56 -rotate-[-10deg] rounded-xl bg-gradient-to-br from-cyan-300 via-slate-700 to-slate-950 shadow-xl">
              <div class="ml-6 mt-10 h-4 w-7 rounded bg-yellow-300" />
              <p class="ml-6 mt-3 text-[10px] tracking-[0.25em] text-white">1234 5678 9012 3456</p>
            </div>
            <div class="absolute bottom-10 left-12 text-xs font-bold uppercase tracking-[0.18em] text-cyan-100">
              Midnight<br />Blues Card
            </div>
            <div class="absolute bottom-20 left-24 h-1 w-48 rounded-full bg-cyan-300 blur-sm" />
          </div>
        </div>

        <div class="flex flex-col justify-center">
          <p class="text-xs font-semibold uppercase tracking-[0.32em] text-blue-900">Premium Choice</p>
          <h1 class="mt-4 text-4xl font-extrabold tracking-tight text-black md:text-5xl">
            {{ card.card_name }}
          </h1>
          <p class="mt-4 max-w-2xl text-sm leading-6 text-zinc-500">
            사용자의 소비 패턴을 AI가 분석하여 가장 높은 혜택을 제공하는 맞춤형 프리미엄 카드입니다.
          </p>

          <div class="mt-8 grid max-w-2xl grid-cols-3 border-y border-zinc-200 py-5">
            <div>
              <p class="text-sm text-zinc-500">연회비</p>
              <p class="mt-1 font-bold text-blue-950">{{ formatWon(card.annual_fee) }}원</p>
            </div>
            <div>
              <p class="text-sm text-zinc-500">기준 실적</p>
              <p class="mt-1 font-bold text-blue-950">{{ formatPrevSpending(card.min_prev_month_spending) }}</p>
            </div>
            <div>
              <p class="text-sm text-zinc-500">카드 종류</p>
              <p class="mt-1 font-bold text-blue-950">{{ card.card_type_display }}</p>
            </div>
          </div>

          <div class="mt-8 flex flex-wrap items-center gap-5">
            <a
              :href="card.apply_url"
              target="_blank"
              rel="noreferrer"
              class="inline-flex h-12 items-center justify-center rounded-md bg-blue-950 px-9 text-sm font-bold text-white shadow-md transition hover:bg-blue-900"
            >
              공식 발급 신청
            </a>
            <button
              type="button"
              class="h-12 px-7 text-sm font-semibold text-zinc-500 transition hover:text-blue-800"
              @click="handleAddCompare"
            >
              비교 추가
            </button>
          </div>
        </div>
      </div>
    </section>

    <section class="border-b border-zinc-200 bg-white/70 px-5 py-12 md:px-10 lg:px-20">
      <div class="mx-auto max-w-7xl rounded-xl border border-blue-100 bg-white p-8 shadow-sm">
        <div class="flex gap-6">
          <div class="flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-indigo-100 text-2xl text-blue-900">
            ✨
          </div>
          <div>
            <h2 class="text-lg font-bold text-blue-950">AI 맞춤 추천 사유</h2>
            <p class="mt-2 text-sm leading-6 text-zinc-600">
              최근 3개월 소비 데이터를 분석한 결과,
              <strong class="font-bold text-blue-950">{{ aiKeywords.join(', ') }}</strong>
              영역의 지출 비중이 높게 나타났습니다. 이 카드는 해당 카테고리에서 혜택을 제공해
              현재 사용 중인 카드 대비
              <strong class="font-bold text-blue-950">월 평균 15,400원의 추가 혜택</strong>
              을 받을 수 있습니다.
            </p>
          </div>
        </div>
      </div>
    </section>

    <section class="mx-auto max-w-7xl px-5 py-16 md:px-10 lg:px-20">
      <div class="mb-10 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <h2 class="text-3xl font-extrabold text-black">상세 혜택 안내</h2>
        <p class="text-sm text-zinc-500">* 전월 이용금액 {{ formatPrevSpending(card.min_prev_month_spending) }} 시 제공</p>
      </div>

      <div class="grid gap-6 md:grid-cols-3">
        <article
          v-for="benefit in detailBenefits"
          :key="benefit.id"
          class="rounded-xl border p-8 shadow-sm"
          :class="
            benefit.tone === 'blue'
              ? 'md:col-span-2 border-blue-950 bg-blue-900 text-white'
              : 'border-zinc-200 bg-white text-zinc-950'
          "
        >
          <div class="flex items-start justify-between gap-4">
            <div>
              <div
                class="mb-5 flex h-10 w-10 items-center justify-center rounded-md"
                :class="benefit.tone === 'blue' ? 'bg-white/10 text-blue-100' : 'bg-indigo-100 text-blue-950'"
              >
                {{ benefit.tone === 'blue' ? '🛍' : '▣' }}
              </div>
              <h3 class="text-lg font-bold">{{ benefit.title }}</h3>
              <p
                class="mt-2 text-sm"
                :class="benefit.tone === 'blue' ? 'text-blue-100' : 'text-zinc-500'"
              >
                {{ benefit.description }}
              </p>
            </div>
            <span
              v-if="benefit.tone !== 'blue'"
              class="rounded-full bg-indigo-100 px-3 py-1 text-xs font-medium text-blue-900"
            >
              {{ benefit.rate.includes('%') ? benefit.rate.replace(' 할인', '% Discount').replace('%%', '%') : benefit.rate }}
            </span>
          </div>

          <div
            class="mt-10 grid gap-5 border-t pt-6"
            :class="benefit.tone === 'blue' ? 'grid-cols-2 border-white/20' : 'grid-cols-2 border-zinc-200'"
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

    <section class="bg-[#f7f5f3] px-5 py-16 md:px-10 lg:px-20">
      <div class="mx-auto max-w-7xl">
        <h2 class="text-3xl font-extrabold text-black">유의사항 및 세부 조건</h2>

        <div class="mt-10 overflow-hidden rounded-xl border border-zinc-200 bg-white">
          <table class="w-full border-collapse text-left text-sm">
            <thead class="bg-zinc-100 text-zinc-900">
              <tr>
                <th class="w-56 px-6 py-4 font-bold">구분</th>
                <th class="px-6 py-4 font-bold">세부 내용</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in conditionRows" :key="row.label" class="border-t border-zinc-200">
                <th class="bg-zinc-50 px-6 py-5 font-semibold text-zinc-700">{{ row.label }}</th>
                <td class="px-6 py-5 leading-6 text-zinc-600">{{ row.value }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <footer class="border-t border-zinc-200 bg-white px-5 py-12 text-sm text-zinc-500 md:px-10 lg:px-20">
      <div class="mx-auto max-w-7xl">
        <p class="font-bold text-zinc-900">CardFit</p>
        <div class="mt-6 flex flex-wrap gap-6">
          <a href="#" class="hover:text-blue-900">이용약관</a>
          <a href="#" class="font-bold text-blue-950 hover:text-blue-700">개인정보처리방침</a>
          <a href="#" class="hover:text-blue-900">고객센터</a>
          <a href="#" class="hover:text-blue-900">공지사항</a>
        </div>
        <p class="mt-6">© 2024 CardFit Financial Services. This is a mock service inspired by Samsung Card.</p>
      </div>
    </footer>
  </div>
</template>
