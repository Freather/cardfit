<template>
  <div class="min-h-screen bg-gray-100 py-10 px-4 md:px-20">
    <div class="max-w-6xl mx-auto space-y-12">
      
      <div v-if="isLoggedIn && hasSurvey" class="bg-blue-900 text-white p-8 rounded-2xl shadow-md flex flex-col md:flex-row justify-between items-start md:items-center">
        <div>
          <h1 class="text-2xl font-bold mb-2">{{ username }}님의 소비 분석이 완료되었어요 🎉</h1>
          <p class="text-blue-200 text-sm">설문 및 CSV 업로드 기반으로 분석된 지출 패턴입니다.</p>
        </div>
        <button @click="goToReport" class="mt-4 md:mt-0 bg-white text-blue-950 font-semibold px-5 py-2.5 rounded-lg text-sm shadow hover:bg-gray-100 transition">
          리포트 자세히 보기
        </button>
      </div>

      <div v-if="isLoggedIn && !hasSurvey" class="bg-amber-900 text-white p-8 rounded-2xl shadow-md flex flex-col md:flex-row justify-between items-start md:items-center">
        <div>
          <h1 class="text-2xl font-bold mb-2">설문을 작성해주세요 📝</h1>
          <p class="text-amber-200 text-sm">연령대와 소득 구간, 최대 연간 회비를 입력하고 CSV를 업로드하여 맞춤형 카드 추천을 받으세요.</p>
        </div>
        <button @click="goToReport" class="mt-4 md:mt-0 bg-white text-amber-950 font-semibold px-5 py-2.5 rounded-lg text-sm shadow hover:bg-gray-100 transition">
          설문 작성하기
        </button>
      </div>

      <div v-else-if="!isLoggedIn" class="bg-gray-800 text-white p-8 rounded-2xl shadow-md flex flex-col md:flex-row justify-between items-start md:items-center">
        <div>
          <h1 class="text-2xl font-bold mb-2">나에게 딱 맞는 카드를 찾고 싶으신가요? 🤔</h1>
          <p class="text-gray-400 text-sm">정확한 소비 패턴 분석을 원하시면 로그인을 진행해 주세요.</p>
        </div>
        <button 
          @click="goToLogin" 
          class="mt-4 md:mt-0 bg-blue-600 text-white font-semibold px-5 py-2.5 rounded-lg text-sm shadow hover:bg-blue-700 transition"
        >
          로그인하러 가기
        </button>
      </div>

      <div v-if="isLoggedIn && spendingReport" class="bg-white p-6 rounded-2xl shadow-sm border border-gray-200">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h3 class="text-lg font-semibold text-gray-900">이번 달 지출 요약</h3>
            <p class="text-sm text-gray-500">저장된 설문을 기준으로 한 달 소비 패턴을 요약합니다.</p>
          </div>
          <div class="text-right">
            <p class="text-sm text-gray-500">총 지출</p>
            <p class="text-2xl font-bold text-blue-700">{{ formattedTotal }}</p>
          </div>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mt-5">
          <div v-for="(value, key) in spendingReport.categories" :key="key" class="rounded-xl bg-gray-50 p-4">
            <div class="text-xs uppercase tracking-wide text-gray-400">{{ categoryLabels[key] }}</div>
            <div class="mt-2 text-lg font-semibold text-gray-900">{{ formatCurrency(value) }}</div>
          </div>
        </div>
      </div>

      <div>
<h2 class="text-xl font-bold text-gray-900 mb-1">
        {{ recommendations.length ? 'AI 추천 카드 TOP 3' : '삼성 카드 추천 라인업' }}
      </h2>
      <p class="text-sm text-gray-500 mb-6">
        {{ recommendations.length ? '내 소비 패턴 기반 예상 혜택 순' : '다양한 혜택의 삼성 카드를 만나보세요' }}
      </p>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div 
            v-for="(card, index) in cards" 
            :key="card.id" 
            class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm flex flex-col justify-between"
          >
            <div>
              <div class="w-full h-40 bg-gray-100 rounded-xl flex items-center justify-center text-xs text-gray-400 mb-5 relative">
                카드 이미지
                <span v-if="card.rank" class="absolute top-3 left-3 bg-blue-600 text-white text-xs font-bold px-2 py-1 rounded-md">
                  추천 {{ card.rank }}위
                </span>
              </div>

              <h3 class="text-lg font-bold text-gray-900 mb-1">{{ card.name }}</h3>
              <p class="text-xs text-gray-400 mb-6">{{ card.desc }}</p>
            </div>

            <button class="w-full py-2.5 rounded-xl font-medium text-sm bg-white text-blue-600 border border-blue-600 hover:bg-blue-50 transition">
              자세히 보기
            </button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import { useSpendingStore } from '../stores/spendingStore'
import { spendingService } from '../services/spendingService'
import { aiService } from '../services/aiService'

const router = useRouter()
const authStore = useAuthStore()
const spendingStore = useSpendingStore()
const isLoggedIn = computed(() => authStore.isAuthenticated)
const username = computed(() => authStore.user?.username || authStore.user?.email || '사용자')
const hasSurvey = computed(() => !!spendingStore.latestSurvey)
const cards = ref([])
const spendingReport = ref(null)
const recommendations = ref([])

const categoryLabels = {
  food: '식비',
  transport: '교통',
  shopping: '쇼핑',
  entertainment: '여가',
  communication: '통신',
  other: '기타',
}

const defaultCards = [
  { id: 1, name: '삼성 iD ON 카드', desc: '쇼핑·주유·통신 특화', benefit: '₩12,000', annual: '연간 약 ₩144,000' },
  { id: 2, name: '삼성 taptap O 카드', desc: '외식·배달 특화', benefit: '₩9,500', annual: '연간 약 ₩114,000' },
  { id: 3, name: '삼성 momo 카드', desc: '교통·편의점 특화', benefit: '₩7,200', annual: '연간 약 ₩86,400' },
]

const loadRecommendations = async (surveyId) => {
  try {
    const params = surveyId ? { survey_id: surveyId } : {}
    const response = await aiService.fetchRecommendations(params)
    const data = response?.data ?? {}
    recommendations.value = data.recommendations || []

    if (recommendations.value.length) {
      cards.value = recommendations.value.map((item) => ({
        id: item.card_id,
        name: item.card_name,
        desc: item.reason,
        benefit: item.expected_monthly_benefit,
        annual: item.tip,
        rank: item.rank || 0,
      }))
    } else {
      cards.value = defaultCards
    }
  } catch (error) {
    recommendations.value = []
    cards.value = defaultCards
  }
}

const goToLogin = () => {
  router.push({ name: 'login' })
}

const goToReport = () => {
  router.push({ name: 'report' })
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW', maximumFractionDigits: 0 }).format(value || 0)
}

const formattedTotal = computed(() => {
  if (!spendingReport.value) return '₩0'
  return formatCurrency(spendingReport.value.total_monthly || 0)
})

const loadSpendingReport = async () => {
  try {
    const { data } = await spendingService.fetchSpendingSummary()
    spendingReport.value = data
  } catch (error) {
    spendingReport.value = null
  }
}

const loadSavedSurvey = async () => {
  try {
    const saved = await spendingStore.fetchLatestSurvey()
    return saved
  } catch {
    return null
  }
}

onMounted(async () => {
  cards.value = defaultCards

  if (isLoggedIn.value) {
    if (!authStore.user) {
      await authStore.fetchProfile().catch(() => {})
    }
    await loadSavedSurvey()
    await loadRecommendations(spendingStore.latestSurvey?.id)
    if (hasSurvey.value) {
      await loadSpendingReport()
    }
  }
})

watch(isLoggedIn, async (value) => {
  if (value) {
    if (!authStore.user) {
      await authStore.fetchProfile().catch(() => {})
    }
    await loadSavedSurvey()
    await loadRecommendations(spendingStore.latestSurvey?.id)
    if (hasSurvey.value) {
      await loadSpendingReport()
    }
  } else {
    spendingReport.value = null
    cards.value = defaultCards
    recommendations.value = []
  }
})

watch(() => spendingStore.latestSurvey, async (survey) => {
  if (isLoggedIn.value && survey) {
    await loadSpendingReport()
    await loadRecommendations(survey.id)
  }
})

</script>