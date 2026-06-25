import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

import { defaultSpendingForm, spendingCategories } from '../data/spendingCategoryData'
import { spendingService } from '../services/spendingService'

export const useSpendingStore = defineStore('spending', () => {
  const spendingForm = ref({ ...defaultSpendingForm })
  const latestSurvey = ref(null)
  const latestCsvSurvey = ref(null)
  const analysisStatus = ref({
    has_survey: false,
    has_csv: false,
    latest_survey_id: null,
    latest_csv_id: null,
  })
  const reportData = ref(null)
  const isLoading = ref(false)
  const error = ref(null)

  const totalMonthly = computed(() => {
    return spendingCategories.reduce(
      (total, category) => total + Number(spendingForm.value[category.key] || 0),
      0,
    )
  })

  function updateSpendingForm(payload) {
    spendingForm.value = { ...spendingForm.value, ...payload }
  }

  function resetSpendingForm() {
    spendingForm.value = { ...defaultSpendingForm }
  }

  async function createSurvey(payload = spendingForm.value, options = {}) {
    const { fallbackOnError = true } = options
    isLoading.value = true
    error.value = null

    try {
      const { data } = await spendingService.createSurvey(payload)
      latestSurvey.value = data
      analysisStatus.value = {
        ...analysisStatus.value,
        has_survey: true,
        latest_survey_id: data?.id || analysisStatus.value.latest_survey_id,
      }
      return data
    } catch (err) {
      error.value = err
      if (!fallbackOnError) {
        throw err
      }

      latestSurvey.value = {
        id: 'local-preview',
        ...payload,
        total_monthly: totalMonthly.value,
      }
      return latestSurvey.value
    } finally {
      isLoading.value = false
    }
  }

  async function uploadCsv(file) {
    isLoading.value = true
    error.value = null

    try {
      const surveyData = {
        age_group: spendingForm.value.age_group,
        income_level: spendingForm.value.income_level,
        max_annual_fee: spendingForm.value.max_annual_fee,
      }
      const response = await spendingService.uploadCsv(file, surveyData)
      const data = response?.data ?? null
      latestCsvSurvey.value = data?.survey || latestCsvSurvey.value
      analysisStatus.value = {
        ...analysisStatus.value,
        has_csv: true,
        latest_csv_id: data?.survey?.id || analysisStatus.value.latest_csv_id,
      }
      return data
    } catch (err) {
      error.value = err
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function fetchLatestSurvey() {
    isLoading.value = true
    error.value = null

    try {
      const { data } = await spendingService.fetchLatestSurvey()
      const surveys = Array.isArray(data) ? data : []
      latestSurvey.value = surveys.find((survey) => survey.input_type === 'manual') || null
      latestCsvSurvey.value = surveys.find((survey) => survey.input_type === 'csv') || null
      analysisStatus.value = {
        has_survey: Boolean(latestSurvey.value),
        has_csv: Boolean(latestCsvSurvey.value),
        latest_survey_id: latestSurvey.value?.id || null,
        latest_csv_id: latestCsvSurvey.value?.id || null,
      }
      return latestSurvey.value
    } catch (err) {
      error.value = err
      latestSurvey.value = null
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function fetchAnalysisStatus() {
    try {
      const { data } = await spendingService.fetchStatus()
      analysisStatus.value = {
        has_survey: Boolean(data?.has_survey),
        has_csv: Boolean(data?.has_csv),
        latest_survey_id: data?.latest_survey_id || null,
        latest_csv_id: data?.latest_csv_id || null,
      }
      return analysisStatus.value
    } catch (err) {
      error.value = err
      analysisStatus.value = {
        has_survey: Boolean(latestSurvey.value),
        has_csv: Boolean(latestCsvSurvey.value),
        latest_survey_id: latestSurvey.value?.id || null,
        latest_csv_id: latestCsvSurvey.value?.id || null,
      }
      throw err
    }
  }

  async function fetchReportData(params = {}) {
    isLoading.value = true
    error.value = null

    try {
      const { data } = await spendingService.fetchCategoryBreakdown(params)
      reportData.value = data
      return data
    } catch (err) {
      error.value = err
      reportData.value = {
        total: totalMonthly.value,
        breakdown: spendingCategories.map((category) => ({
          category: category.category,
          total: Number(spendingForm.value[category.key] || 0),
          count: 0,
          ratio: totalMonthly.value
            ? Math.round((Number(spendingForm.value[category.key] || 0) / totalMonthly.value) * 1000) /
              10
            : 0,
        })),
      }
      return reportData.value
    } finally {
      isLoading.value = false
    }
  }

  return {
    spendingForm,
    latestSurvey,
    latestCsvSurvey,
    analysisStatus,
    reportData,
    isLoading,
    error,
    totalMonthly,
    updateSpendingForm,
    resetSpendingForm,
    createSurvey,
    uploadCsv,
    fetchLatestSurvey,
    fetchAnalysisStatus,
    fetchReportData,
  }
})
