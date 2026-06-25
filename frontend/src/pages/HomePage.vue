<template>
  <main class="min-h-screen bg-gray-100 px-4 py-10 md:px-20">
    <div class="mx-auto max-w-6xl space-y-10">
      <TodayCardDraw
        :cards="todayCards"
      />

      <SpendingSurveyForm
        :is-logged-in="isLoggedIn"
        :has-survey="hasSurvey"
        :has-csv="hasCsv"
        :username="username"
      />

      <RecommendedCardList
        :cards="cards"
      />
    </div>
  </main>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'

import RecommendedCardList from '../components/home/RecommendedCardList.vue'
import SpendingSurveyForm from '../components/home/SpendingSurveyForm.vue'
import TodayCardDraw from '../components/home/TodayCardDraw.vue'
import { useAuthState } from '../composables/useAuthState'
import { useCardStore } from '../stores/cardStore'
import { useSpendingStore } from '../stores/spendingStore'
import { getRepresentativeBenefit } from '../utils/representativeBenefit'

const { authStore, isLoggedIn, displayName, ensureProfile } = useAuthState()
const spendingStore = useSpendingStore()
const cardStore = useCardStore()

const cards = ref([])
const accessVersion = ref(0)

const username = computed(() => displayName.value)
const hasSurvey = computed(() => {
  accessVersion.value
  return Boolean(spendingStore.analysisStatus.has_survey)
})
const hasCsv = computed(() => {
  accessVersion.value
  return Boolean(spendingStore.analysisStatus.has_csv)
})
const todayCards = computed(() => cardStore.cards.map(normalizeTodayCard))
const categoryLabels = {
  food: '식비',
  transport: '교통',
  fuel: '주유',
  shopping: '쇼핑',
  entertainment: '문화/여가',
  communication: '통신',
  health: '병원/건강',
  point: '포인트',
  other: '기타',
}

function normalizeTodayCard(card) {
  return {
    id: card.id,
    name: card.card_name,
    card_company: card.card_company,
    annual_fee: card.annual_fee,
    min_prev_month_spending: card.min_prev_month_spending,
    benefits: card.benefits || [],
    image_url: card.image_url || '',
  }
}

function buildDefaultCards(storeCards) {
  return storeCards.slice(0, 3).map((card) => {
    const mainBenefit = getRepresentativeBenefit(card)

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
  await cardStore.fetchCards().catch(() => null)
  cards.value = buildDefaultCards(cardStore.cards)
}

async function loadSavedSurvey() {
  if (!isLoggedIn.value) return

  await spendingStore.fetchLatestSurvey().catch(() => null)
  accessVersion.value += 1
}

async function refreshHomeData() {
  await ensureProfile()

  await loadSavedSurvey()
  cards.value = buildDefaultCards(cardStore.cards)
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
  cards.value = buildDefaultCards(cardStore.cards)
})
</script>
