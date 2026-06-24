<template>
  <AnalysisRequirementNotice
    v-if="!isCheckingAccess && !canUseAnalysis"
    eyebrow="소비 리포트 준비"
    title="CSV와 소비 설문을 준비해주세요."
    :missing-requirements="missingRequirements"
  />
  <AnalysisAccessSkeleton
    v-else-if="isCheckingAccess"
    message="소비 리포트 이용 가능 여부를 확인하는 중입니다..."
  />
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

      <p
        v-if="reportError"
        class="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm font-bold text-red-700"
      >
        {{ reportError }}
      </p>

      <SpendingReportSkeleton
        v-if="isLoadingReport"
      />

      <template v-else>
        <div class="grid gap-5 lg:grid-cols-[1.4fr_0.8fr]">
          <AiReportBox
            :summary="aiReport.summary"
            :total-amount-label="formatCurrency(totalCategoryAmount)"
            :top-category-label="topCategory.label"
            :top-category-ratio="formatRatio(topCategory.ratio)"
            :category-count="displayedCategoryBreakdown.length"
            :period-label="analysisPeriodLabel"
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
          @select-category="openCategoryTransactions"
        />
      </template>

      <ReportRecommendationCta />
    </div>

    <CategoryTransactionsModal
      :open="isTransactionModalOpen"
      :category="selectedTransactionCategory"
      :transactions="categoryTransactions"
      :loading="isLoadingTransactions"
      :error="transactionModalError"
      :period-label="analysisPeriodLabel"
      @close="closeCategoryTransactions"
    />
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

import AnalysisRequirementNotice from '../components/common/AnalysisRequirementNotice.vue'
import AnalysisAccessSkeleton from '../components/common/AnalysisAccessSkeleton.vue'
import AiReportBox from '../components/report/AiReportBox.vue'
import CategoryTransactionsModal from '../components/report/CategoryTransactionsModal.vue'
import ReportRecommendationCta from '../components/report/ReportRecommendationCta.vue'
import SpendingCategorySection from '../components/report/SpendingCategorySection.vue'
import SpendingProfileCard from '../components/report/SpendingProfileCard.vue'
import SpendingReportSkeleton from '../components/report/SpendingReportSkeleton.vue'
import { SURVEY_PREFERENCE_STORAGE_KEY, useAnalysisAccess } from '../composables/useAnalysisAccess'
import { mockAiReport } from '../data/mockReportData'
import { spendingCategories } from '../data/spendingCategoryData'
import { getApiErrorMessage } from '../services/api'
import { spendingService } from '../services/spendingService'

const { authStore, spendingStore, canUseAnalysis, missingRequirements } = useAnalysisAccess()
const aiReport = ref(mockAiReport)
const isCheckingAccess = ref(true)
const isLoadingReport = ref(false)
const reportError = ref('')
const isTransactionModalOpen = ref(false)
const isLoadingTransactions = ref(false)
const transactionModalError = ref('')
const selectedTransactionCategory = ref(null)
const categoryTransactions = ref([])
const categoryColors = ['#001278', '#2563eb', '#7c3aed', '#db2777', '#f59e0b', '#10b981']
const categoryMetaMap = Object.fromEntries(spendingCategories.map((category) => [category.category, category]))

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
    .filter(Boolean)
    .join(' · ') || '정보 없음'
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
const analysisPeriodLabel = computed(() => formatPeriodLabel(
  aiReport.value.survey?.transaction_start_date || latestSurvey.value?.transaction_start_date,
  aiReport.value.survey?.transaction_end_date || latestSurvey.value?.transaction_end_date,
))

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

async function loadReportData() {
  isLoadingReport.value = true
  reportError.value = ''

  try {
    const summaryResponse = await spendingService.fetchSpendingSummary()
    const summary = summaryResponse?.data || {}
    const surveyId = summary.survey_id || latestSurvey.value?.id
    const breakdownResponse = await spendingService.fetchCategoryBreakdown(
      surveyId ? { survey_id: surveyId } : {},
    )

    aiReport.value = buildReportFromApi(summary, breakdownResponse?.data)
  } catch (error) {
    if (isMockPreview.value) {
      aiReport.value = mockAiReport
      return
    }

    reportError.value = getApiErrorMessage(
      error,
      '소비 리포트를 불러오지 못했어요. 다시 시도해주세요.',
    )

    try {
      await spendingStore.fetchLatestSurvey()
      aiReport.value = buildReportFromSurvey(latestSurvey.value)
    } catch {
      aiReport.value = mockAiReport
    }
  } finally {
    isLoadingReport.value = false
  }
}

function buildReportFromApi(summary, breakdownData = {}) {
  const survey = normalizeSurveySummary(summary)
  const breakdown = normalizeCategoryBreakdown(breakdownData?.breakdown || [], survey)

  return {
    ...mockAiReport,
    survey,
    based_on: buildBasedOn(survey),
    category_breakdown: breakdown,
    summary: buildSummaryText(breakdown),
  }
}

function buildReportFromSurvey(survey) {
  const normalizedSurvey = normalizeSurveySummary(survey)

  return {
    ...mockAiReport,
    survey: normalizedSurvey,
    based_on: buildBasedOn(normalizedSurvey),
    category_breakdown: buildBreakdownFromSurvey(normalizedSurvey),
  }
}

function normalizeSurveySummary(summary = {}) {
  const categories = summary.categories || {}

  return {
    id: summary.survey_id || summary.id || null,
    input_type: summary.input_type || 'csv',
    age_group: summary.age_group || latestSurvey.value?.age_group || getSavedSurveyPreference('age_group') || spendingStore.spendingForm.age_group || '',
    income_level: summary.income_level || latestSurvey.value?.income_level || spendingStore.spendingForm.income_level || '',
    max_annual_fee: summary.max_annual_fee || 0,
    transaction_start_date: summary.transaction_start_date || latestSurvey.value?.transaction_start_date || '',
    transaction_end_date: summary.transaction_end_date || latestSurvey.value?.transaction_end_date || '',
    food_monthly: summary.food_monthly ?? categories.food ?? 0,
    transport_monthly: summary.transport_monthly ?? categories.transport ?? 0,
    fuel_monthly: summary.fuel_monthly ?? categories.fuel ?? 0,
    shopping_monthly: summary.shopping_monthly ?? categories.shopping ?? 0,
    communication_monthly: summary.communication_monthly ?? categories.communication ?? 0,
    entertainment_monthly: summary.entertainment_monthly ?? categories.entertainment ?? 0,
    health_monthly: summary.health_monthly ?? categories.health ?? 0,
    other_monthly: summary.other_monthly ?? categories.other ?? 0,
    total_monthly: summary.total_monthly || 0,
    created_at: summary.created_at || '',
  }
}

function getSavedSurveyPreference(key) {
  try {
    const saved = JSON.parse(localStorage.getItem(SURVEY_PREFERENCE_STORAGE_KEY) || 'null')
    return saved?.[key] || ''
  } catch (error) {
    localStorage.removeItem(SURVEY_PREFERENCE_STORAGE_KEY)
    return ''
  }
}

function formatPeriodLabel(start, end) {
  if (start && end) return `${formatDate(start)} - ${formatDate(end)}`
  return '소비 데이터 기준'
}

function formatDate(value) {
  if (!value) return '-'

  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(new Date(value))
}

function buildBasedOn(survey) {
  return spendingCategories.reduce(
    (acc, category) => ({
      ...acc,
      [category.key]: Number(survey?.[category.key] || 0),
    }),
    {
      total_monthly: Number(survey?.total_monthly || 0),
      max_annual_fee: Number(survey?.max_annual_fee || 0),
    },
  )
}

function normalizeCategoryBreakdown(items, survey) {
  const transactionBreakdown = items
    .filter((item) => Number(item.total || 0) > 0)
    .map((item) => enrichCategory(item))

  if (transactionBreakdown.length) return transactionBreakdown
  return buildBreakdownFromSurvey(survey)
}

function buildBreakdownFromSurvey(survey) {
  const calculatedTotal = spendingCategories.reduce(
    (sum, category) => sum + Number(survey?.[category.key] || 0),
    0,
  )
  const total = Number(survey?.total_monthly || 0) || calculatedTotal

  return spendingCategories
    .map((category) => {
      const amount = Number(survey?.[category.key] || 0)
      return enrichCategory({
        category: category.category,
        total: amount,
        count: 0,
        ratio: total ? Math.round((amount / total) * 1000) / 10 : 0,
      })
    })
    .filter((item) => item.total > 0)
}

function enrichCategory(item) {
  const meta = categoryMetaMap[item.category] || { label: item.category || '기타' }

  return {
    ...item,
    label: meta.label,
    total: Number(item.total || 0),
    ratio: Number(item.ratio || 0),
    insight: buildCategoryInsight(meta.label, item),
  }
}

function buildCategoryInsight(label, item) {
  const count = Number(item.count || 0)
  if (count > 0) {
    return `${label} 영역에서 ${count.toLocaleString('ko-KR')}건의 결제가 확인되었습니다.`
  }

  return `${label} 영역의 월 예상 지출을 기준으로 분석했습니다.`
}

function buildSummaryText(breakdown) {
  const topItems = breakdown.slice(0, 2).map((item) => item.label).filter(Boolean)
  if (!topItems.length) {
    return '소비 데이터를 더 준비하면 리포트를 볼 수 있어요.'
  }

  return `최근 소비는 ${topItems.join(', ')} 영역의 비중이 높습니다. 주요 지출 카테고리에 맞춰 혜택이 집중된 카드를 함께 확인해 보세요.`
}

async function openCategoryTransactions(category) {
  selectedTransactionCategory.value = category
  categoryTransactions.value = []
  transactionModalError.value = ''
  isTransactionModalOpen.value = true

  if (isMockPreview.value) {
    categoryTransactions.value = []
    return
  }

  isLoadingTransactions.value = true

  try {
    const surveyId = aiReport.value.survey?.id || latestSurvey.value?.id
    const params = {
      category: category.category,
      ...(surveyId ? { survey_id: surveyId } : {}),
    }
    const { data } = await spendingService.fetchTransactions(params)
    categoryTransactions.value = Array.isArray(data) ? data : []
  } catch (error) {
    transactionModalError.value = getApiErrorMessage(
      error,
      '소비 내역을 불러오지 못했어요.',
    )
  } finally {
    isLoadingTransactions.value = false
  }
}

function closeCategoryTransactions() {
  isTransactionModalOpen.value = false
  transactionModalError.value = ''
}

onMounted(async () => {
  if (authStore.isAuthenticated) {
    await spendingStore.fetchLatestSurvey().catch(() => null)
  }

  if (canUseAnalysis.value) {
    await loadReportData()
  }

  isCheckingAccess.value = false
})
</script>
