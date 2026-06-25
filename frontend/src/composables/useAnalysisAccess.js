import { computed } from 'vue'

import { useSpendingStore } from '../stores/spendingStore'
import { useAuthState } from './useAuthState'

export const CSV_UPLOAD_STORAGE_KEY = 'cardfit:csv-upload-complete'
export const SURVEY_PREFERENCE_STORAGE_KEY = 'cardfit:survey-preferences'

function readJsonStorage(key) {
  try {
    return JSON.parse(localStorage.getItem(key) || 'null')
  } catch (error) {
    localStorage.removeItem(key)
    return null
  }
}

export function markCsvUploadComplete(fileName = '') {
  localStorage.setItem(
    CSV_UPLOAD_STORAGE_KEY,
    JSON.stringify({
      completed: true,
      fileName,
      updatedAt: new Date().toISOString(),
    }),
  )
}

export function hasSavedCsvUpload() {
  return Boolean(readJsonStorage(CSV_UPLOAD_STORAGE_KEY)?.completed)
}

export function hasSavedSurveyPreferences() {
  const saved = readJsonStorage(SURVEY_PREFERENCE_STORAGE_KEY)
  return Boolean(
    saved?.preferredBenefit &&
      Array.isArray(saved.categories) &&
      saved.categories.length &&
      Number(saved.monthlyAmount) > 0,
  )
}

export function useAnalysisAccess() {
  const { authStore, isLoggedIn, ensureProfile } = useAuthState()
  const spendingStore = useSpendingStore()

  const hasSurvey = computed(() => Boolean(spendingStore.analysisStatus.has_survey))
  const hasCsv = computed(() => Boolean(spendingStore.analysisStatus.has_csv))
  const canUseAnalysis = computed(() => isLoggedIn.value && hasSurvey.value && hasCsv.value)
  const missingRequirements = computed(() => {
    const requirements = []

    if (!isLoggedIn.value) requirements.push('로그인')
    if (!hasSurvey.value) requirements.push('소비 설문')
    if (!hasCsv.value) requirements.push('CSV 업로드')

    return requirements
  })

  return {
    authStore,
    spendingStore,
    isLoggedIn,
    ensureProfile,
    hasSurvey,
    hasCsv,
    canUseAnalysis,
    missingRequirements,
  }
}
