<template>
  <AnalysisRequirementNotice
    v-if="!isCheckingAccess && !canUseAnalysis"
    eyebrow="소비 리포트 준비 필요"
    title="소비 리포트를 보려면 CSV 업로드와 소비 설문이 필요합니다."
    :missing-requirements="missingRequirements"
  />
  <section
    v-else-if="isCheckingAccess"
    class="min-h-screen bg-[#fbf9f8] px-4 py-20 text-center text-sm font-bold text-gray-500 md:px-10 lg:px-20"
  >
    이용 가능 여부를 확인하는 중...
  </section>
  <section v-else class="min-h-screen bg-[#fbf9f8] px-4 py-8 md:px-10 lg:px-20">
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

      <div class="grid gap-5 lg:grid-cols-[1.4fr_0.8fr]">
        <AiReportBox
          :summary="aiReport.summary"
          :total-amount-label="formatCurrency(totalCategoryAmount)"
          :top-category-label="topCategory.label"
          :top-category-ratio="formatRatio(topCategory.ratio)"
          :category-count="displayedCategoryBreakdown.length"
        />

        <SpendingProfileCard
          :primary-spending-label="primarySpendingLabel"
          :income-label="formatIncomeLevel(aiReport.survey.income_level)"
          :age-label="formatAgeGroup(aiReport.survey.age_group)"
        />
      </div>

      <SpendingCategorySection
        :categories="displayedCategoryBreakdown"
        :chart-data="doughnutChartData"
        :chart-options="doughnutChartOptions"
        :total-amount-label="formatCurrency(totalCategoryAmount)"
      />

      <ReportRecommendationCta />
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

import AnalysisRequirementNotice from '../components/common/AnalysisRequirementNotice.vue'
import AiReportBox from '../components/report/AiReportBox.vue'
import ReportRecommendationCta from '../components/report/ReportRecommendationCta.vue'
import SpendingCategorySection from '../components/report/SpendingCategorySection.vue'
import SpendingProfileCard from '../components/report/SpendingProfileCard.vue'
import { useAnalysisAccess } from '../composables/useAnalysisAccess'
import { mockAiReport } from '../data/mockReportData'

const { authStore, spendingStore, canUseAnalysis, missingRequirements } = useAnalysisAccess()
const aiReport = ref(mockAiReport)
const isCheckingAccess = ref(true)
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

function formatCurrency(value) {
  return new Intl.NumberFormat('ko-KR', {
    style: 'currency',
    currency: 'KRW',
    maximumFractionDigits: 0,
  }).format(value || 0)
}

function formatRatio(value) {
  return Number(value || 0).toLocaleString('ko-KR', {
    maximumFractionDigits: 1,
  })
}

function formatAgeGroup(value) {
  const ageGroupMap = {
    '20s': '20대',
    '30s': '30대',
    '40s': '40대',
    '50s': '50대',
    '60s': '60대 이상',
  }

  return ageGroupMap[value] || '정보 없음'
}

function formatIncomeLevel(value) {
  const incomeLevelMap = {
    low: '저소득',
    mid: '중간',
    high: '고소득',
  }

  return incomeLevelMap[value] || '정보 없음'
}

async function loadSavedSurvey() {
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
    // Keep mock report for backend-free development.
  }

  aiReport.value = mockAiReport
}

onMounted(async () => {
  if (authStore.isAuthenticated) {
    await loadSavedSurvey()
  }

  isCheckingAccess.value = false
})
</script>
