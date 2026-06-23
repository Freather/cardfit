<template>
  <section class="min-h-screen bg-[#faf8f7] px-4 py-4 text-[#121212] md:px-6">
    <div v-if="isLoading" class="flex min-h-[60vh] items-center justify-center text-sm font-bold text-[#4d5870]">
      마이페이지 정보를 불러오는 중...
    </div>

    <div v-else class="mx-auto grid max-w-[1160px] gap-7 lg:grid-cols-[330px_1fr]">
      <aside class="grid content-start gap-5">
        <ProfileInfoCard
          :name="displayName"
          :email="displayEmail"
          @edit="openProfileModal"
          @logout="handleLogout"
        />

        <ProfileWishlistCard
          :cards="wishedCards"
          :failed-image-ids="failedImages"
          @image-error="onImageError"
        />
      </aside>

      <main class="grid content-start gap-7">
        <SurveySummaryCard
          :updated-at="surveyUpdatedAt"
          :main-category="mainCategory"
          :monthly-total-label="formatCompactWon(monthlyTotal)"
          :preferred-benefit="preferredBenefit"
          @open-survey="openSurveyModal"
        />

        <CsvDataTable
          :uploads="uploads"
          @open-upload="openUploadModal"
          @remove-upload="removeUpload"
        />
      </main>
    </div>

    <SurveyEditModal
      v-model:form="surveyForm"
      :open="isSurveyModalOpen"
      :category-options="surveyCategoryOptions"
      :benefit-options="benefitOptions"
      :error="surveyError"
      @close="closeSurveyModal"
      @save="handleSurveySave"
    />

    <CsvUploadModal
      :open="isUploadModalOpen"
      :file="selectedCsvFile"
      :uploading="isUploading"
      :error="uploadError"
      @close="closeUploadModal"
      @file-change="handleFileChange"
      @file-drop="handleFileDrop"
      @clear-file="selectedCsvFile = null"
      @upload="handleCsvUpload"
    />

    <ProfileEditModal
      v-model:form="profileForm"
      :open="isProfileModalOpen"
      :saving="isProfileSaving"
      :error="profileError"
      @close="closeProfileModal"
      @save="handleProfileSave"
    />
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import CsvDataTable from '../components/profile/CsvDataTable.vue'
import CsvUploadModal from '../components/profile/CsvUploadModal.vue'
import ProfileEditModal from '../components/profile/ProfileEditModal.vue'
import ProfileInfoCard from '../components/profile/ProfileInfoCard.vue'
import ProfileWishlistCard from '../components/profile/ProfileWishlistCard.vue'
import SurveyEditModal from '../components/profile/SurveyEditModal.vue'
import SurveySummaryCard from '../components/profile/SurveySummaryCard.vue'
import { markCsvUploadComplete, SURVEY_PREFERENCE_STORAGE_KEY } from '../composables/useAnalysisAccess'
import { authService } from '../services/authService'
import { useAuthStore } from '../stores/authStore'
import { useCardStore } from '../stores/cardStore'
import { useSpendingStore } from '../stores/spendingStore'

const router = useRouter()
const authStore = useAuthStore()
const cardStore = useCardStore()
const spendingStore = useSpendingStore()

const isLoading = ref(true)
const failedImages = ref(new Set())
const isUploadModalOpen = ref(false)
const selectedCsvFile = ref(null)
const uploadError = ref('')
const isUploading = ref(false)
const isProfileModalOpen = ref(false)
const isProfileSaving = ref(false)
const profileError = ref('')
const profileForm = ref({
  username: '',
  email: '',
})
const isSurveyModalOpen = ref(false)
const surveyError = ref('')
const surveyForm = ref({
  categories: ['food', 'shopping'],
  monthlyAmount: 2300000,
  preferredBenefit: '포인트 적립',
})
const uploads = ref([
  {
    id: 1,
    fileName: 'samsung_card_2405.csv',
    uploadedAt: '2024.05.15',
    period: '2024.04.01 - 2024.04.30',
    status: '분석 완료',
    statusTone: 'done',
  },
  {
    id: 2,
    fileName: 'kb_check_q1.csv',
    uploadedAt: '2024.04.10',
    period: '2024.01.01 - 2024.03.31',
    status: '분석 완료',
    statusTone: 'done',
  },
  {
    id: 3,
    fileName: 'manual_entry_2403.csv',
    uploadedAt: '2024.03.02',
    period: '2024.02.01 - 2024.02.29',
    status: '만료됨',
    statusTone: 'expired',
  },
])

const categoryFields = [
  { key: 'food_monthly', label: '식비' },
  { key: 'shopping_monthly', label: '쇼핑' },
  { key: 'transport_monthly', label: '교통' },
  { key: 'fuel_monthly', label: '주유' },
  { key: 'communication_monthly', label: '통신' },
  { key: 'entertainment_monthly', label: '여가/문화' },
  { key: 'health_monthly', label: '의료/건강' },
  { key: 'other_monthly', label: '기타' },
]

const surveyCategoryOptions = [
  { value: 'food', label: '식비', field: 'food_monthly' },
  { value: 'transport', label: '교통', field: 'transport_monthly' },
  { value: 'fuel', label: '주유', field: 'fuel_monthly' },
  { value: 'shopping', label: '쇼핑', field: 'shopping_monthly' },
  { value: 'communication', label: '통신', field: 'communication_monthly' },
  { value: 'entertainment', label: '여가/문화', field: 'entertainment_monthly' },
  { value: 'health', label: '의료/건강', field: 'health_monthly' },
  { value: 'other', label: '기타', field: 'other_monthly' },
]

const benefitOptions = [
  '음식점, 카페 할인',
  '버스, 지하철, 택시',
  '주유소 할인/적립',
  '온/오프라인 쇼핑',
  '통신요금 할인',
  'OTT, 영화, 여행',
  '약국, 병원',
  '그 외 혜택',
]

const user = computed(() => authStore.user || {})
const displayName = computed(() => user.value.username || user.value.email?.split('@')[0] || '김삼성')
const displayEmail = computed(() => user.value.email || 'samsung.kim@cardfit.ai')
const wishlist = computed(() => cardStore.wishlist || [])
const wishedCards = computed(() => wishlist.value.map((wish) => wish.card).filter(Boolean).slice(0, 3))
const latestSurvey = computed(() => spendingStore.latestSurvey)
const selectedCategoryLabels = computed(() =>
  surveyForm.value.categories
    .map((category) => surveyCategoryOptions.find((option) => option.value === category)?.label)
    .filter(Boolean),
)

const surveyUpdatedAt = computed(() => {
  const rawDate = latestSurvey.value?.updated_at || latestSurvey.value?.created_at
  if (!rawDate) return '2024. 05. 12'

  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(new Date(rawDate))
})

const monthlyTotal = computed(() => {
  if (surveyForm.value.monthlyAmount) return Number(surveyForm.value.monthlyAmount)
  if (latestSurvey.value?.total_monthly) return Number(latestSurvey.value.total_monthly)

  const total = categoryFields.reduce((sum, item) => {
    return sum + Number(latestSurvey.value?.[item.key] || 0)
  }, 0)

  return total || 2300000
})

const mainCategory = computed(() => {
  if (selectedCategoryLabels.value.length) return selectedCategoryLabels.value.join(', ')
  if (!latestSurvey.value) return '식비, 쇼핑'

  const totalsByLabel = categoryFields.reduce((acc, item) => {
    acc[item.label] = (acc[item.label] || 0) + Number(latestSurvey.value?.[item.key] || 0)
    return acc
  }, {})

  const top = Object.entries(totalsByLabel).sort((a, b) => b[1] - a[1])[0]
  return top?.[1] ? top[0] : '식비, 쇼핑'
})

const preferredBenefit = computed(() => surveyForm.value.preferredBenefit || '그 외 혜택')

onMounted(async () => {
  isLoading.value = true
  loadSavedSurveyPreferences()

  await Promise.allSettled([
    authStore.fetchProfile(),
    cardStore.fetchWishlist(),
    spendingStore.fetchLatestSurvey(),
  ])

  isLoading.value = false
})

function formatCompactWon(value) {
  const amount = Number(value || 0)
  if (amount >= 10000) return `${Math.round(amount / 10000)}만원`
  return `${amount.toLocaleString('ko-KR')}원`
}

function onImageError(cardId) {
  failedImages.value = new Set([...failedImages.value, cardId])
}

function removeUpload(uploadId) {
  uploads.value = uploads.value.filter((upload) => upload.id !== uploadId)
}

function openProfileModal() {
  profileError.value = ''
  profileForm.value = {
    username: user.value.username || '',
    email: user.value.email || '',
  }
  isProfileModalOpen.value = true
}

function closeProfileModal() {
  if (isProfileSaving.value) return
  isProfileModalOpen.value = false
  profileError.value = ''
}

async function handleProfileSave() {
  const username = profileForm.value.username.trim()

  if (!username) {
    profileError.value = '이름을 입력해주세요.'
    return
  }

  isProfileSaving.value = true
  profileError.value = ''

  try {
    const { data } = await authService.updateProfile({ username })
    authStore.user = data
    closeProfileModal()
  } catch (error) {
    if (authStore.accessToken === 'mock-dev-access-token') {
      authStore.user = {
        ...user.value,
        username,
        updated_at: new Date().toISOString(),
      }
      closeProfileModal()
      return
    }

    profileError.value = '회원정보 수정에 실패했습니다.'
  } finally {
    isProfileSaving.value = false
  }
}

function openSurveyModal() {
  surveyError.value = ''
  isSurveyModalOpen.value = true
}

function closeSurveyModal() {
  isSurveyModalOpen.value = false
  surveyError.value = ''
}

async function handleSurveySave() {
  if (!surveyForm.value.categories.length) {
    surveyError.value = '메인 소비 카테고리를 하나 이상 선택해주세요.'
    return
  }

  if (!surveyForm.value.monthlyAmount || surveyForm.value.monthlyAmount < 10000) {
    surveyError.value = '평균 월 지출액을 입력해주세요.'
    return
  }

  surveyError.value = ''

  const amountPerCategory = Math.round(
    Number(surveyForm.value.monthlyAmount) / surveyForm.value.categories.length,
  )
  const payload = {
    input_type: 'manual',
    age_group: spendingStore.spendingForm.age_group,
    income_level: spendingStore.spendingForm.income_level,
    max_annual_fee: spendingStore.spendingForm.max_annual_fee,
  }

  surveyCategoryOptions.forEach((option) => {
    payload[option.field] = surveyForm.value.categories.includes(option.value) ? amountPerCategory : 0
  })

  await spendingStore.createSurvey(payload)
  saveSurveyPreferences()
  closeSurveyModal()
}

function loadSavedSurveyPreferences() {
  try {
    const saved = JSON.parse(localStorage.getItem(SURVEY_PREFERENCE_STORAGE_KEY) || 'null')
    if (!saved) return

    surveyForm.value = {
      categories: Array.isArray(saved.categories) && saved.categories.length
        ? saved.categories
        : surveyForm.value.categories,
      monthlyAmount: Number(saved.monthlyAmount) || surveyForm.value.monthlyAmount,
      preferredBenefit: saved.preferredBenefit || surveyForm.value.preferredBenefit,
    }
  } catch (error) {
    localStorage.removeItem(SURVEY_PREFERENCE_STORAGE_KEY)
  }
}

function saveSurveyPreferences() {
  localStorage.setItem(
    SURVEY_PREFERENCE_STORAGE_KEY,
    JSON.stringify({
      categories: surveyForm.value.categories,
      monthlyAmount: surveyForm.value.monthlyAmount,
      preferredBenefit: surveyForm.value.preferredBenefit,
      updatedAt: new Date().toISOString(),
    }),
  )
}

function openUploadModal() {
  uploadError.value = ''
  selectedCsvFile.value = null
  isUploadModalOpen.value = true
}

function closeUploadModal() {
  if (isUploading.value) return
  isUploadModalOpen.value = false
  uploadError.value = ''
  selectedCsvFile.value = null
}

function handleFileChange(event) {
  const file = event.target.files?.[0]
  setCsvFile(file)
}

function handleFileDrop(event) {
  const file = event.dataTransfer.files?.[0]
  setCsvFile(file)
}

function setCsvFile(file) {
  uploadError.value = ''

  if (!file) {
    selectedCsvFile.value = null
    return
  }

  if (!file.name.toLowerCase().endsWith('.csv')) {
    selectedCsvFile.value = null
    uploadError.value = 'CSV 파일만 업로드할 수 있습니다.'
    return
  }

  selectedCsvFile.value = file
}

function formatToday() {
  const today = new Date()
  const year = today.getFullYear()
  const month = String(today.getMonth() + 1).padStart(2, '0')
  const day = String(today.getDate()).padStart(2, '0')
  return `${year}.${month}.${day}`
}

async function handleCsvUpload() {
  if (!selectedCsvFile.value) {
    uploadError.value = '업로드할 CSV 파일을 선택해주세요.'
    return
  }

  isUploading.value = true
  uploadError.value = ''

  try {
    await spendingStore.uploadCsv(selectedCsvFile.value)
    markCsvUploadComplete(selectedCsvFile.value.name)
    uploads.value = [
      {
        id: Date.now(),
        fileName: selectedCsvFile.value.name,
        uploadedAt: formatToday(),
        period: '업로드 데이터 기준',
        status: '분석 완료',
        statusTone: 'done',
      },
      ...uploads.value,
    ]
    closeUploadModal()
  } catch (error) {
    uploadError.value = '업로드에 실패했습니다. 로그인 상태와 CSV 형식을 확인해주세요.'
  } finally {
    isUploading.value = false
  }
}

async function handleLogout() {
  await authStore.logout()
  router.push({ name: 'login' })
}
</script>
