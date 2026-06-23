<template>
  <main class="min-h-screen bg-gray-100 px-4 py-10 md:px-20">
    <div class="mx-auto max-w-6xl space-y-10">
      <SpendingSurveyForm
        :is-logged-in="isLoggedIn"
        :has-survey="hasSurvey"
        :has-csv="hasCsv"
        :username="username"
      />

      <AiRecommendationSummary
        v-if="isAnalysisReady && spendingReport"
        :report="spendingReport"
        :category-labels="categoryLabels"
      />

      <RecommendedCardList
        :cards="cards"
        :has-recommendations="recommendations.length > 0"
      />
    </div>
  </main>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'

import AiRecommendationSummary from '../components/home/AiRecommendationSummary.vue'
import RecommendedCardList from '../components/home/RecommendedCardList.vue'
import SpendingSurveyForm from '../components/home/SpendingSurveyForm.vue'
import {
  hasSavedCsvUpload,
  hasSavedSurveyPreferences,
} from '../composables/useAnalysisAccess'
import { useAuthState } from '../composables/useAuthState'
import { aiService } from '../services/aiService'
import { spendingService } from '../services/spendingService'
import { useCardStore } from '../stores/cardStore'
import { useSpendingStore } from '../stores/spendingStore'

const { authStore, isLoggedIn, displayName, ensureProfile } = useAuthState()
const spendingStore = useSpendingStore()
const cardStore = useCardStore()

const cards = ref([])
const spendingReport = ref(null)
const recommendations = ref([])
const accessVersion = ref(0)

const username = computed(() => displayName.value)
const hasSurvey = computed(() => {
  accessVersion.value
  return Boolean(spendingStore.latestSurvey) || hasSavedSurveyPreferences()
})
const hasCsv = computed(() => {
  accessVersion.value
  return hasSavedCsvUpload()
})
const isAnalysisReady = computed(() => isLoggedIn.value && hasSurvey.value && hasCsv.value)

const categoryLabels = {
  food: '식비',
  transport: '교통',
  fuel: '주유',
  shopping: '쇼핑',
  entertainment: '문화/여가',
  communication: '통신',
  health: '병원/건강',
  other: '기타',
}

function buildDefaultCards(storeCards) {
  return storeCards.slice(0, 3).map((card) => {
    const mainBenefit = card.benefits?.[0]

    return {
      id: card.id,
      name: card.card_name,
      desc: mainBenefit
        ? `${categoryLabels[mainBenefit.benefit_category] || '생활'} 혜택 중심 카드`
        : '생활 혜택 중심 카드',
      benefit: card.annual_fee ? `연회비 ${formatNumber(card.annual_fee)}원` : '연회비 무료',
      image_url: card.image_url || '',
    }
  })
}

async function loadCards() {
  await cardStore.fetchCards()
  cards.value = buildDefaultCards(cardStore.cards)
}

async function loadSavedSurvey() {
  if (!isLoggedIn.value) return

  await spendingStore.fetchLatestSurvey().catch(() => null)
  accessVersion.value += 1
}

async function loadRecommendations() {
  if (!isAnalysisReady.value) {
    recommendations.value = []
    cards.value = buildDefaultCards(cardStore.cards)
    return
  }

  try {
    const params = spendingStore.latestSurvey?.id ? { survey_id: spendingStore.latestSurvey.id } : {}
    const response = await aiService.fetchRecommendations(params)
    const data = response?.data ?? {}
    recommendations.value = data.recommendations || []

    if (!recommendations.value.length) {
      cards.value = buildDefaultCards(cardStore.cards)
      return
    }

    cards.value = recommendations.value.slice(0, 3).map((item) => {
      const cardInfo = cardStore.cards.find((card) => String(card.id) === String(item.card_id))

      return {
        id: item.card_id,
        name: item.card_name,
        desc: item.reason || '소비 패턴과 잘 맞는 카드입니다.',
        benefit: item.expected_monthly_benefit,
        rank: item.rank || 0,
        image_url: cardInfo?.image_url || '',
      }
    })
  } catch (error) {
    recommendations.value = []
    cards.value = buildDefaultCards(cardStore.cards)
  }
}

async function loadSpendingReport() {
  if (!isAnalysisReady.value) {
    spendingReport.value = null
    return
  }

  try {
    const { data } = await spendingService.fetchSpendingSummary()
    spendingReport.value = data
  } catch (error) {
    spendingReport.value = null
  }
}

async function refreshHomeData() {
  await ensureProfile()

  await loadSavedSurvey()
  await loadRecommendations()
  await loadSpendingReport()
}

function formatNumber(value) {
  return new Intl.NumberFormat('ko-KR').format(Number(value || 0))
}

onMounted(async () => {
  await loadCards()
  await refreshHomeData()
})

watch(isLoggedIn, async () => {
  await refreshHomeData()
})

watch(() => spendingStore.latestSurvey, async () => {
  accessVersion.value += 1
  await loadRecommendations()
  await loadSpendingReport()
})
</script>
