<template>
  <section class="min-h-screen bg-[#faf8f7] px-4 py-4 text-[#121212] md:px-6">
    <ProfilePageSkeleton v-if="isLoading" />

    <div v-else class="mx-auto grid max-w-[1160px] gap-7 lg:grid-cols-[330px_1fr]">
      <p
        v-if="profileSuccessMessage"
        class="lg:col-span-2 rounded-lg border border-emerald-200 bg-emerald-50 px-5 py-4 text-sm font-extrabold text-emerald-700 shadow-[0_8px_20px_rgba(16,185,129,0.12)]"
      >
        {{ profileSuccessMessage }}
      </p>

      <aside class="grid content-start gap-5">
        <ProfileInfoCard
          :name="displayName"
          :email="displayEmail"
          :age-label="displayAgeGroup"
          @edit="openProfileModal"
          @logout="openLogoutConfirm"
        />

        <ProfileWishlistCard
          :cards="wishedCards"
          :failed-image-ids="failedImages"
          @image-error="onImageError"
        />
      </aside>

      <main class="grid content-start gap-7">
        <SurveySummaryCard
          :has-survey="hasManualSurvey"
          :updated-at="surveyUpdatedAt"
          :main-category="mainCategory"
          :monthly-total-label="formatCompactWon(monthlyTotal)"
          :preferred-benefit="preferredBenefit"
          @open-survey="openSurveyModal"
        />

        <CsvDataTable
          :uploads="uploads"
          :loading="isLoadingUploads"
          :error="uploadListError"
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
      :age-options="ageGroupOptions"
      :error="profileError"
      @close="closeProfileModal"
      @save="handleProfileSave"
    />

    <div
      v-if="isLogoutConfirmOpen"
      class="fixed inset-0 z-[100] flex items-center justify-center bg-black/45 px-4 py-6"
      role="dialog"
      aria-modal="true"
      aria-labelledby="profile-logout-confirm-title"
      @click.self="closeLogoutConfirm"
    >
      <section class="w-full max-w-[420px] rounded-lg bg-white shadow-2xl">
        <div class="border-b border-[#ececf2] px-6 py-5">
          <p class="text-sm font-extrabold text-[#001278]">로그아웃 확인</p>
          <h2 id="profile-logout-confirm-title" class="mt-1 text-xl font-extrabold text-[#111827]">
            로그아웃할까요?
          </h2>
          <p class="mt-2 text-sm leading-6 text-[#4d5870]">
            현재 계정에서 나가면 다시 로그인해야 서비스를 이용할 수 있어요.
          </p>
        </div>

        <div class="flex justify-end gap-3 px-6 py-5">
          <button
            type="button"
            class="inline-flex h-11 items-center justify-center rounded-md border border-[#d4d8e8] bg-white px-5 text-sm font-bold text-[#4d5870] transition hover:bg-[#f7f7fa]"
            :disabled="isLoggingOut"
            @click="closeLogoutConfirm"
          >
            취소
          </button>
          <button
            type="button"
            class="inline-flex h-11 min-w-[104px] items-center justify-center rounded-md bg-[#001278] px-5 text-sm font-extrabold text-white transition hover:bg-[#1428a0] disabled:cursor-not-allowed disabled:bg-[#8b93c8]"
            :disabled="isLoggingOut"
            @click="confirmLogout"
          >
            {{ isLoggingOut ? '로그아웃 중' : '로그아웃' }}
          </button>
        </div>
      </section>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import CsvDataTable from '../components/profile/CsvDataTable.vue'
import CsvUploadModal from '../components/profile/CsvUploadModal.vue'
import ProfilePageSkeleton from '../components/profile/ProfilePageSkeleton.vue'
import ProfileEditModal from '../components/profile/ProfileEditModal.vue'
import ProfileInfoCard from '../components/profile/ProfileInfoCard.vue'
import ProfileWishlistCard from '../components/profile/ProfileWishlistCard.vue'
import SurveyEditModal from '../components/profile/SurveyEditModal.vue'
import SurveySummaryCard from '../components/profile/SurveySummaryCard.vue'
import { markCsvUploadComplete, SURVEY_PREFERENCE_STORAGE_KEY } from '../composables/useAnalysisAccess'
import { getApiErrorMessage } from '../services/api'
import { authService } from '../services/authService'
import { spendingService } from '../services/spendingService'
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
const uploadListError = ref('')
const isUploading = ref(false)
const isLoadingUploads = ref(false)
const isProfileModalOpen = ref(false)
const isProfileSaving = ref(false)
const isLogoutConfirmOpen = ref(false)
const isLoggingOut = ref(false)
const profileError = ref('')
const profileSuccessMessage = ref('')
const profileForm = ref({
  username: '',
  email: '',
  age_group: '30s',
})
const isSurveyModalOpen = ref(false)
const surveyError = ref('')
const surveyForm = ref({
  categories: ['food', 'shopping'],
  monthlyAmount: 2300000,
  preferredBenefit: '할인/캐시백',
})
const uploads = ref([])
let profileSuccessTimer = null

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
  '할인/캐시백',
  '포인트/마일리지',
  '식당/카페 혜택',
  '교통/택시 혜택',
  '주유 혜택',
  '온라인 쇼핑 혜택',
  '통신요금 혜택',
  '문화/여행 혜택',
]

const ageGroupOptions = [
  { value: '20s', label: '20대' },
  { value: '30s', label: '30대' },
  { value: '40s', label: '40대' },
  { value: '50s', label: '50대' },
  { value: '60s', label: '60대 이상' },
]

const user = computed(() => authStore.user || {})
const displayName = computed(() => user.value.username || user.value.email?.split('@')[0] || '김삼성')
const displayEmail = computed(() => user.value.email || 'samsung.kim@cardfit.ai')
const displayAgeGroup = computed(() => formatAgeGroupLabel(getCurrentAgeGroup()))
const wishlist = computed(() => cardStore.wishlist || [])
const wishedCards = computed(() => wishlist.value.map((wish) => wish.card).filter(Boolean).slice(0, 3))
const latestSurvey = computed(() => spendingStore.latestSurvey)
const hasManualSurvey = computed(() => Boolean(latestSurvey.value))
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
    loadSpendingUploads(),
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

async function removeUpload(uploadId) {
  uploadListError.value = ''

  try {
    await spendingService.deleteSurvey(uploadId)
    uploads.value = uploads.value.filter((upload) => upload.id !== uploadId)

    if (
      String(latestSurvey.value?.id) === String(uploadId) ||
      String(spendingStore.latestCsvSurvey?.id) === String(uploadId)
    ) {
      await spendingStore.fetchLatestSurvey().catch(() => null)
    }
  } catch (error) {
    uploadListError.value = getApiErrorMessage(error, '삭제하지 못했어요. 다시 시도해주세요.')
  }
}

function openProfileModal() {
  profileError.value = ''
  profileSuccessMessage.value = ''
  profileForm.value = {
    username: user.value.username || '',
    email: user.value.email || '',
    age_group: getCurrentAgeGroup(),
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
  const ageGroup = profileForm.value.age_group || '30s'

  if (!username) {
    profileError.value = '이름을 입력해주세요.'
    return
  }

  isProfileSaving.value = true
  profileError.value = ''

  try {
    const { data } = await authService.updateProfile({ username })
    authStore.user = data
    await saveProfileAgeGroup(ageGroup)
    completeProfileSave()
    showProfileSuccess()
  } catch (error) {
    if (authStore.accessToken === 'mock-dev-access-token') {
      authStore.user = {
        ...user.value,
        username,
        updated_at: new Date().toISOString(),
      }
      await saveProfileAgeGroup(ageGroup, { localOnly: true })
      completeProfileSave()
      showProfileSuccess()
      return
    }

    profileError.value = getApiErrorMessage(error, '수정하지 못했어요. 다시 시도해주세요.')
  } finally {
    isProfileSaving.value = false
  }
}

function completeProfileSave() {
  isProfileModalOpen.value = false
  profileError.value = ''
}

function showProfileSuccess() {
  profileSuccessMessage.value = '수정이 끝났어요.'

  if (profileSuccessTimer) {
    window.clearTimeout(profileSuccessTimer)
  }

  profileSuccessTimer = window.setTimeout(() => {
    profileSuccessMessage.value = ''
    profileSuccessTimer = null
  }, 3000)
}

async function saveProfileAgeGroup(ageGroup, options = {}) {
  const { localOnly = false } = options

  spendingStore.updateSpendingForm({ age_group: ageGroup })
  saveSurveyPreferences({ age_group: ageGroup })

  if (!latestSurvey.value?.id || latestSurvey.value.id === 'local-preview' || localOnly) {
    if (latestSurvey.value) {
      spendingStore.latestSurvey = {
        ...latestSurvey.value,
        age_group: ageGroup,
        updated_at: new Date().toISOString(),
      }
    }
    return
  }

  const { data } = await spendingService.updateSurvey(latestSurvey.value.id, { age_group: ageGroup })
  spendingStore.latestSurvey = data
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
    surveyError.value = '선호 카테고리를 선택해주세요.'
    return
  }

  if (!surveyForm.value.monthlyAmount || surveyForm.value.monthlyAmount < 10000) {
    surveyError.value = '원하는 사용 금액을 입력해주세요.'
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

  try {
    await spendingStore.createSurvey(payload, { fallbackOnError: false })
    saveSurveyPreferences()
    await loadSpendingUploads()
    closeSurveyModal()
  } catch (error) {
    surveyError.value = getApiErrorMessage(error, '설문을 저장하지 못했어요. 다시 시도해주세요.')
  }
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

    if (saved.age_group) {
      spendingStore.updateSpendingForm({ age_group: saved.age_group })
    }
  } catch (error) {
    localStorage.removeItem(SURVEY_PREFERENCE_STORAGE_KEY)
  }
}

function saveSurveyPreferences(extra = {}) {
  localStorage.setItem(
    SURVEY_PREFERENCE_STORAGE_KEY,
    JSON.stringify({
      categories: surveyForm.value.categories,
      monthlyAmount: surveyForm.value.monthlyAmount,
      preferredBenefit: surveyForm.value.preferredBenefit,
      age_group: spendingStore.spendingForm.age_group,
      ...extra,
      updatedAt: new Date().toISOString(),
    }),
  )
}

function getCurrentAgeGroup() {
  return (
    latestSurvey.value?.age_group ||
    readSavedSurveyPreferences()?.age_group ||
    spendingStore.spendingForm.age_group ||
    '30s'
  )
}

function formatAgeGroupLabel(value) {
  return ageGroupOptions.find((option) => option.value === value)?.label || '정보 없음'
}

function readSavedSurveyPreferences() {
  try {
    return JSON.parse(localStorage.getItem(SURVEY_PREFERENCE_STORAGE_KEY) || 'null')
  } catch (error) {
    localStorage.removeItem(SURVEY_PREFERENCE_STORAGE_KEY)
    return null
  }
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
    uploadError.value = 'CSV 파일만 올릴 수 있어요.'
    return
  }

  selectedCsvFile.value = file
}

async function handleCsvUpload() {
  if (!selectedCsvFile.value) {
    uploadError.value = 'CSV 파일을 선택해주세요.'
    return
  }

  isUploading.value = true
  uploadError.value = ''

  try {
    const result = await spendingStore.uploadCsv(selectedCsvFile.value)
    markCsvUploadComplete(selectedCsvFile.value.name)
    await loadSpendingUploads()
    if (result?.survey) spendingStore.latestCsvSurvey = result.survey
    closeUploadModal()
  } catch (error) {
    uploadError.value = getApiErrorMessage(
      error,
      '업로드하지 못했어요. 파일 형식을 확인해보세요.',
    )
  } finally {
    isUploading.value = false
  }
}

async function loadSpendingUploads() {
  isLoadingUploads.value = true
  uploadListError.value = ''

  try {
    const { data } = await spendingService.fetchSurveys()
    const surveys = Array.isArray(data) ? data : []
    uploads.value = surveys.filter((survey) => survey.input_type === 'csv').map(toUploadRow)
  } catch (error) {
    uploads.value = []
    uploadListError.value = getApiErrorMessage(error, '목록을 불러오지 못했어요.')
  } finally {
    isLoadingUploads.value = false
  }
}

function toUploadRow(survey) {
  const uploadedAt = formatDate(survey.created_at)
  const period = formatSurveyPeriod(survey)
  return {
    id: survey.id,
    fileName: `CSV 업로드 #${survey.id}`,
    uploadedAt,
    period,
    status: `분석 완료${survey.transaction_count ? ` (${survey.transaction_count}건)` : ''}`,
    statusTone: 'done',
  }
}

function formatSurveyPeriod(survey) {
  if (survey.transaction_start_date && survey.transaction_end_date) {
    return `${formatDate(survey.transaction_start_date)} - ${formatDate(survey.transaction_end_date)}`
  }

  return `월 ${formatCompactWon(survey.total_monthly || 0)} 기준`
}

function formatDate(value) {
  if (!value) return '-'

  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(new Date(value))
}

function openLogoutConfirm() {
  isLogoutConfirmOpen.value = true
}

function closeLogoutConfirm() {
  if (isLoggingOut.value) return
  isLogoutConfirmOpen.value = false
}

async function confirmLogout() {
  isLoggingOut.value = true

  try {
    await authStore.logout()
    isLogoutConfirmOpen.value = false
    router.push({ name: 'login' })
  } finally {
    isLoggingOut.value = false
  }
}
</script>
