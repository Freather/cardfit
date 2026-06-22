<template>
  <section class="min-h-screen bg-[#fbf9f8] px-4 py-8 md:px-10 lg:px-20">
    <div class="mx-auto max-w-7xl space-y-6">
      <header class="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <p class="text-sm font-semibold text-[#001278]">소비 분석 리포트</p>
          <h1 class="mt-2 text-3xl font-bold text-gray-950">나의 소비 리포트</h1>
          <p class="mt-2 text-sm text-gray-500">
            CSV 소비 데이터를 바탕으로 카테고리별 지출과 소비 패턴을 확인합니다.
          </p>
        </div>
        <div
          v-if="isMockPreview"
          class="rounded-2xl border border-blue-200 bg-blue-50 px-4 py-3 text-sm text-blue-800"
        >
          백엔드 없이 개발용 mock 데이터로 표시 중입니다.
        </div>
      </header>

      <section class="grid gap-5 lg:grid-cols-[1.4fr_0.8fr]">
        <div class="rounded-xl border border-[#e0e0e0] bg-white p-7 shadow-[0_4px_12px_rgba(0,0,0,0.05)]">
          <div class="flex flex-col gap-5 md:flex-row md:items-start md:justify-between">
            <div>
              <p class="text-sm font-semibold text-[#001278]">AI 분석 요약</p>
              <h2 class="mt-2 text-2xl font-bold text-gray-950">생활 할인형 카드가 가장 유리합니다</h2>
              <p class="mt-4 max-w-3xl text-sm leading-6 text-gray-600">{{ aiReport.summary }}</p>
            </div>
            <div class="rounded-2xl bg-[#001278] px-5 py-4 text-white">
              <p class="text-xs text-blue-200">월 총 지출</p>
              <p class="mt-1 text-2xl font-bold">{{ formatCurrency(totalCategoryAmount) }}</p>
            </div>
          </div>

          <div class="mt-8 grid gap-4 sm:grid-cols-3">
            <div class="rounded-2xl bg-gray-50 p-5">
              <p class="text-sm text-gray-500">가장 큰 지출</p>
              <p class="mt-2 text-2xl font-bold text-gray-950">{{ topCategory.label }}</p>
            </div>
            <div class="rounded-2xl bg-gray-50 p-5">
              <p class="text-sm text-gray-500">최대 비중</p>
              <p class="mt-2 text-2xl font-bold text-gray-950">{{ formatRatio(topCategory.ratio) }}%</p>
            </div>
            <div class="rounded-2xl bg-gray-50 p-5">
              <p class="text-sm text-gray-500">분석 카테고리</p>
              <p class="mt-2 text-2xl font-bold text-gray-950">{{ displayedCategoryBreakdown.length }}개</p>
            </div>
          </div>
        </div>

        <div class="rounded-xl border border-[#e0e0e0] bg-white p-7 shadow-[0_4px_12px_rgba(0,0,0,0.05)]">
          <p class="text-sm font-semibold text-gray-500">소비 성향</p>
          <div class="mt-5 space-y-4">
            <div class="flex items-center justify-between text-sm">
              <span class="font-semibold text-gray-800">주요 소비</span>
              <span class="text-[#001278]">{{ primarySpendingLabel }}</span>
            </div>
            <div class="flex items-center justify-between text-sm">
              <span class="font-semibold text-gray-800">소득 구간</span>
              <span class="text-gray-600">{{ formatIncomeLevel(aiReport.survey.income_level) }}</span>
            </div>
            <div class="flex items-center justify-between text-sm">
              <span class="font-semibold text-gray-800">연령대</span>
              <span class="text-gray-600">{{ formatAgeGroup(aiReport.survey.age_group) }}</span>
            </div>
            <div class="rounded-2xl bg-amber-50 p-4 text-sm leading-6 text-amber-900">
              고정비보다 변동 지출 비중이 커서 영역별 할인 조건을 맞추기 좋은 패턴입니다.
            </div>
          </div>
        </div>
      </section>

      <section class="rounded-xl border border-[#e0e0e0] bg-white shadow-[0_4px_12px_rgba(0,0,0,0.05)]">
        <div class="grid lg:grid-cols-[0.82fr_1fr]">
          <div class="p-8">
            <div class="flex flex-col items-center gap-8">
              <div class="relative h-80 w-80 max-w-full">
                <div class="relative z-10 h-full w-full">
                  <SpendingDoughnutChart
                    :chart-data="doughnutChartData"
                    :chart-options="doughnutChartOptions"
                  />
                </div>
                <div class="pointer-events-none absolute left-1/2 top-1/2 z-0 flex h-36 w-36 -translate-x-1/2 -translate-y-1/2 flex-col items-center justify-center rounded-full bg-white text-center">
                  <p class="text-sm text-gray-500">총 지출</p>
                  <p class="mt-1 text-xl font-extrabold text-gray-950">{{ formatCurrency(totalCategoryAmount) }}</p>
                </div>
              </div>

              <div class="grid w-full gap-3 sm:grid-cols-2">
                <div
                  v-for="category in displayedCategoryBreakdown"
                  :key="category.category"
                  class="flex items-center justify-between gap-3 rounded-lg bg-[#fbf9f8] px-4 py-3"
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
            <div class="mb-6 flex items-start justify-between gap-4">
              <div>
                <h2 class="text-xl font-bold text-gray-950">카테고리 상세</h2>
                <p class="mt-1 text-sm text-gray-500">지출 금액과 분석 코멘트를 확인하세요.</p>
              </div>
            </div>

            <div class="space-y-4">
              <article
                v-for="category in displayedCategoryBreakdown"
                :key="`detail-${category.category}`"
                class="rounded-xl border border-[#e0e0e0] p-5"
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

      <section class="py-10 text-center">
        <h2 class="text-xl font-bold text-gray-950">분석 결과를 바탕으로 최적의 카드를 확인해볼까요?</h2>
        <p class="mt-2 text-sm text-gray-500">
          CardFit AI가 고객님의 소비 패턴에 맞는 혜택을 실시간으로 계산했습니다.
        </p>
        <RouterLink
          to="/ai-recommendations"
          class="mt-6 inline-flex h-14 min-w-56 items-center justify-center rounded-full bg-[#001278] px-8 text-base font-bold text-white shadow-lg transition hover:bg-[#1428a0]"
        >
          추천 카드 보기
        </RouterLink>
      </section>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { useSpendingStore } from '../stores/spendingStore'
import SpendingDoughnutChart from '../components/report/SpendingDoughnutChart.vue'
import { mockAiReport } from '../data/mockReportData'

const authStore = useAuthStore()
const spendingStore = useSpendingStore()
const aiReport = ref(mockAiReport)
const categoryColors = ['#001278', '#2563eb', '#7c3aed', '#db2777', '#f59e0b', '#10b981']

const latestSurvey = computed(() => spendingStore.latestSurvey)
const categoryBreakdown = computed(() => aiReport.value.category_breakdown || mockAiReport.category_breakdown)
const totalCategoryAmount = computed(() => {
  return categoryBreakdown.value.reduce((total, category) => total + Number(category.total || 0), 0)
})
const displayedCategoryBreakdown = computed(() => {
  return categoryBreakdown.value.map((category, index) => {
    const total = Number(category.total || 0)
    const ratio = totalCategoryAmount.value
      ? Math.round((total / totalCategoryAmount.value) * 1000) / 10
      : Number(category.ratio || 0)

    return {
      ...category,
      ratio,
      color: categoryColors[index % categoryColors.length],
    }
  })
})
const topCategory = computed(() => displayedCategoryBreakdown.value[0] || { label: '-', ratio: 0 })
const primarySpendingLabel = computed(() => {
  return displayedCategoryBreakdown.value
    .slice(0, 2)
    .map((category) => category.label)
    .join(' · ')
})
const doughnutChartData = computed(() => {
  return {
    labels: displayedCategoryBreakdown.value.map((category) => category.label),
    datasets: [
      {
        data: displayedCategoryBreakdown.value.map((category) => Number(category.total || 0)),
        backgroundColor: displayedCategoryBreakdown.value.map((category) => category.color),
        borderColor: '#ffffff',
        borderWidth: 0,
        hoverOffset: 10,
      },
    ],
  }
})
const doughnutChartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  cutout: '58%',
  plugins: {
    legend: {
      display: false,
    },
    tooltip: {
      backgroundColor: '#ffffff',
      titleColor: '#111827',
      bodyColor: '#001278',
      borderColor: '#e0e0e0',
      borderWidth: 1,
      padding: 12,
      displayColors: true,
      callbacks: {
        title(items) {
          const category = displayedCategoryBreakdown.value[items?.[0]?.dataIndex]
          return category?.label || ''
        },
        label(context) {
          const category = displayedCategoryBreakdown.value[context.dataIndex]
          if (!category) return ''
          return `${formatCurrency(category.total)} (${formatRatio(category.ratio)}%)`
        },
      },
    },
  },
}))
const isMockPreview = computed(() => import.meta.env.DEV && authStore.accessToken === 'mock-dev-access-token')

const formatCurrency = (value) => {
  return new Intl.NumberFormat('ko-KR', {
    style: 'currency',
    currency: 'KRW',
    maximumFractionDigits: 0,
  }).format(value || 0)
}

const formatRatio = (value) => {
  return Number(value || 0).toLocaleString('ko-KR', {
    maximumFractionDigits: 1,
  })
}

const formatAgeGroup = (value) => {
  switch (value) {
    case '20s':
      return '20대'
    case '30s':
      return '30대'
    case '40s':
      return '40대'
    case '50s':
      return '50대'
    case '60s':
      return '60대 이상'
    default:
      return '정보 없음'
  }
}

const formatIncomeLevel = (value) => {
  switch (value) {
    case 'low':
      return '저소득'
    case 'mid':
      return '중간'
    case 'high':
      return '고소득'
    default:
      return '정보 없음'
  }
}

const applyMockReport = () => {
  aiReport.value = mockAiReport
  spendingStore.latestSurvey = mockAiReport.survey
}

const loadSavedSurvey = async () => {
  try {
    await spendingStore.fetchLatestSurvey()
    if (latestSurvey.value) {
      aiReport.value = {
        ...mockAiReport,
        survey: latestSurvey.value,
      }
      return
    }
  } catch {
    // Fall through to mock data for backend-free development.
  }

  applyMockReport()
}

onMounted(async () => {
  if (authStore.isAuthenticated) {
    await loadSavedSurvey()
  } else {
    applyMockReport()
  }
})
</script>
