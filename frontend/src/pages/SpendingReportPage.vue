<template>
  <section class="min-h-screen bg-gray-100 py-10 px-4 md:px-20">
    <div class="max-w-6xl mx-auto space-y-8">
      <div class="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">설문 & CSV 업로드</h1>
        </div>

      </div>

      <div class="grid gap-6 lg:grid-cols-[1.25fr_0.9fr]">
        <div class="space-y-6">
          <section class="rounded-3xl bg-white p-8 shadow-sm border border-gray-200">
            <div class="mb-6 flex items-center justify-between gap-4">
              <div>
                <h2 class="text-xl font-semibold text-gray-900">설문 설정</h2>
                <p class="text-sm text-gray-500">연령대, 소득 구간, 최대 연간 회비를 설정하면 CSV 업로드 시 함께 저장됩니다.</p>
              </div>
              <span class="rounded-full bg-blue-50 px-3 py-1 text-sm text-blue-700">설정</span>
            </div>

            <div class="space-y-6">
              <div class="grid gap-4 sm:grid-cols-3">
                <label class="block space-y-2 text-sm text-gray-700">
                  <span>연령대</span>
                  <select
                    v-model="spendingStore.spendingForm.age_group"
                    class="w-full rounded-2xl border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                  >
                    <option value="20s">20대</option>
                    <option value="30s">30대</option>
                    <option value="40s">40대</option>
                    <option value="50s">50대</option>
                    <option value="60s">60대 이상</option>
                  </select>
                </label>

                <label class="block space-y-2 text-sm text-gray-700">
                  <span>소득 구간</span>
                  <select
                    v-model="spendingStore.spendingForm.income_level"
                    class="w-full rounded-2xl border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                  >
                    <option value="low">저소득</option>
                    <option value="mid">중간</option>
                    <option value="high">고소득</option>
                  </select>
                </label>

                <label class="block space-y-2 text-sm text-gray-700">
                  <span>연간 최대 카드 수수료</span>
                  <select
                    v-model.number="spendingStore.spendingForm.max_annual_fee"
                    class="w-full rounded-2xl border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                  >
                    <option :value="0">0원</option>
                    <option :value="30000">30,000원</option>
                    <option :value="50000">50,000원</option>
                    <option :value="100000">100,000원</option>
                    <option :value="200000">200,000원</option>
                  </select>
                </label>
              </div>

              <div class="flex flex-col gap-3 sm:flex-row sm:items-center">
                <button
                  type="button"
                  @click="saveSurveySettings"
                  :disabled="isLoading"
                  class="inline-flex justify-center rounded-2xl bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  설정 저장
                </button>
                <button
                  type="button"
                  @click="resetSurveyForm"
                  class="inline-flex justify-center rounded-2xl border border-gray-300 bg-white px-6 py-3 text-sm font-semibold text-gray-700 hover:bg-gray-50"
                >
                  설정 초기화
                </button>
              </div>

              <p v-if="surveyMessage" class="text-sm text-green-600">{{ surveyMessage }}</p>
              <p v-if="storeError" class="text-sm text-red-600">{{ storeError }}</p>
            </div>
          </section>

          <section class="rounded-3xl bg-white p-8 shadow-sm border border-gray-200">
            <div class="mb-6 flex items-center justify-between gap-4">
              <div>
                <h2 class="text-xl font-semibold text-gray-900">CSV 업로드</h2>
                <p class="text-sm text-gray-500">삼성카드 이용내역 CSV를 업로드하면 월별 지출을 분석하고 자동으로 저장합니다.</p>
              </div>
              <span class="rounded-full bg-emerald-50 px-3 py-1 text-sm text-emerald-700">자동 분석</span>
            </div>

            <form @submit.prevent="submitCsv" class="space-y-4">
              <label class="block text-sm text-gray-700">
                <span class="mb-2 block">CSV 파일 선택</span>
                <input
                  type="file"
                  accept=".csv"
                  @change="handleFileChange"
                  class="w-full rounded-2xl border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 outline-none"
                />
              </label>

              <button
                type="submit"
                :disabled="isLoading"
                class="inline-flex justify-center rounded-2xl bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
              >
                CSV 업로드 및 분석
              </button>

              <p v-if="fileError" class="text-sm text-red-600">{{ fileError }}</p>
              <p v-if="uploadMessage" class="text-sm text-green-600">{{ uploadMessage }}</p>
            </form>
          </section>
        </div>

        <div class="space-y-6">
          <section class="rounded-3xl bg-white p-8 shadow-sm border border-gray-200">
            <div class="mb-5">
              <h2 class="text-xl font-semibold text-gray-900">최근 설문 요약</h2>
              <p class="text-sm text-gray-500">가장 마지막에 저장된 설문 결과를 보여줍니다.</p>
            </div>

            <div v-if="latestSurvey" class="space-y-5">
              <div class="rounded-3xl bg-gray-50 p-6">
                <div class="flex items-center justify-between gap-4">
                  <div>
                    <p class="text-sm text-gray-500">총 월 지출</p>
                    <p class="text-3xl font-bold text-blue-600">{{ formatCurrency(latestSurvey.total_monthly) }}</p>
                  </div>
                  <div class="text-right text-sm text-gray-600">
                    <p>연령대: {{ formatAgeGroup(latestSurvey.age_group) }}</p>
                    <p>소득: {{ formatIncomeLevel(latestSurvey.income_level) }}</p>
                    <p>연간 수수료: {{ formatCurrency(latestSurvey.max_annual_fee) }}</p>
                  </div>
                </div>
              </div>

              <div class="grid gap-3 sm:grid-cols-2">
                <div v-for="category in spendingCategories" :key="category.key" class="rounded-3xl bg-gray-50 p-5">
                  <p class="text-sm text-gray-500">{{ category.label }}</p>
                  <p class="mt-3 text-2xl font-semibold text-gray-900">{{ formatCurrency(latestSurvey[category.key]) }}</p>
                </div>
              </div>
            </div>

            <div v-else class="rounded-3xl bg-gray-50 p-6 text-gray-600">
              아직 저장된 설문이 없습니다. 설문을 입력하거나 CSV 업로드를 해보세요.
            </div>
          </section>

          <section class="rounded-3xl bg-white p-8 shadow-sm border border-gray-200">
            <div class="mb-5">
              <h2 class="text-xl font-semibold text-gray-900">AI 추천 카드</h2>
              <p class="text-sm text-gray-500">설문 또는 CSV 업로드 후에 AI 추천 결과가 표시됩니다.</p>
            </div>

            <div v-if="recommendations.length" class="space-y-4">
              <div v-for="(card, index) in recommendations" :key="card.id" class="rounded-3xl border border-gray-200 p-5">
                <div class="flex items-center justify-between gap-4">
                  <div>
                    <p class="text-sm text-gray-500">추천 {{ index + 1 }}위</p>
                    <h3 class="text-xl font-semibold text-gray-900">{{ card.card_name }}</h3>
                  </div>
                  <span class="rounded-full bg-blue-50 px-3 py-1 text-sm text-blue-700">예상 혜택</span>
                </div>
                <p class="mt-3 text-sm text-gray-700">{{ card.reason }}</p>
                <div class="mt-4 flex flex-wrap gap-3 text-sm text-gray-600">
                  <span>월 혜택: {{ card.expected_monthly_benefit }}</span>
                  <span>연간 팁: {{ card.tip }}</span>
                </div>
              </div>
            </div>

            <div v-else class="rounded-3xl bg-gray-50 p-6 text-gray-600">
              아직 AI 추천 결과가 없습니다. 먼저 설문 입력 또는 CSV 업로드를 시도해 주세요.
            </div>
          </section>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { useSpendingStore } from '../stores/spendingStore'
import { spendingCategories } from '../data/spendingCategoryData'
import { aiService } from '../services/aiService'

const authStore = useAuthStore()
const spendingStore = useSpendingStore()
const file = ref(null)
const fileError = ref('')
const uploadMessage = ref('')
const surveyMessage = ref('')
const recommendations = ref([])

const isLoading = computed(() => spendingStore.isLoading)
const latestSurvey = computed(() => spendingStore.latestSurvey)
const storeError = computed(() => {
  if (!spendingStore.error) return ''
  return spendingStore.error?.response?.data?.detail || spendingStore.error?.message || '오류가 발생했습니다.'
})

const formatCurrency = (value) => {
  return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW', maximumFractionDigits: 0 }).format(value || 0)
}

const formatAgeGroup = (value) => {
  switch (value) {
    case '20s': return '20대'
    case '30s': return '30대'
    case '40s': return '40대'
    case '50s': return '50대'
    case '60s': return '60대 이상'
    default: return '알 수 없음'
  }
}

const formatIncomeLevel = (value) => {
  switch (value) {
    case 'low': return '저소득'
    case 'mid': return '중간'
    case 'high': return '고소득'
    default: return '알 수 없음'
  }
}

const handleFileChange = (event) => {
  fileError.value = ''
  uploadMessage.value = ''

  const selected = event.target.files?.[0]
  if (!selected) {
    file.value = null
    return
  }

  if (!selected.name.toLowerCase().endsWith('.csv')) {
    fileError.value = 'CSV 파일만 업로드할 수 있습니다.'
    file.value = null
    return
  }

  file.value = selected
}

const loadRecommendations = async (surveyId) => {
  try {
    const params = surveyId ? { survey_id: surveyId } : {}
    const response = await aiService.fetchRecommendations(params)
    const data = response?.data ?? {}
    recommendations.value = data?.recommendations || []
  } catch {
    recommendations.value = []
  }
}

const loadSavedSurvey = async () => {
  if (!authStore.isAuthenticated) return

  try {
    await spendingStore.fetchLatestSurvey()
    const survey = spendingStore.latestSurvey
    if (survey) {
      spendingStore.updateSpendingForm({
        age_group: survey.age_group,
        income_level: survey.income_level,
        max_annual_fee: survey.max_annual_fee,
      })
      await loadRecommendations(survey.id)
    }
  } catch {
    // ignore load errors, 최신 survey가 없으면 그대로 둔다
  }
}

const submitSurvey = async () => {
  surveyMessage.value = ''
  fileError.value = ''
  uploadMessage.value = ''

  try {
    const survey = await spendingStore.createSurvey()
    surveyMessage.value = '설문이 저장되었습니다. AI 추천 결과를 불러옵니다.'
    await loadRecommendations(survey?.id)
  } catch (error) {
    surveyMessage.value = ''
  }
}

const saveSurveySettings = () => {
  surveyMessage.value = '설정이 저장되었습니다. CSV 업로드 시 이 설정이 적용됩니다.'
}

const submitCsv = async () => {
  uploadMessage.value = ''
  fileError.value = ''
  surveyMessage.value = ''

  if (!file.value) {
    fileError.value = 'CSV 파일을 선택해 주세요.'
    return
  }

  try {
    const result = await spendingStore.uploadCsv(file.value)
    const data = result ?? {}
    uploadMessage.value = data.message || 'CSV 업로드가 완료되었습니다.'
    const surveyId = data?.survey?.id || spendingStore.latestSurvey?.id
    if (surveyId) {
      await loadRecommendations(surveyId)
    } else {
      await loadRecommendations()
    }
  } catch (error) {
    console.error('CSV upload error', error)
    fileError.value = spendingStore.error?.response?.data?.detail || error?.message || 'CSV 업로드 중 오류가 발생했습니다.'
  }
}

onMounted(async () => {
  if (authStore.isAuthenticated) {
    await loadSavedSurvey()
  }
})

const resetSurveyForm = () => {
  spendingStore.resetSpendingForm()
  surveyMessage.value = ''
  uploadMessage.value = ''
  fileError.value = ''
  file.value = null
}
</script>
