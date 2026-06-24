import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

import { defaultSpendingForm, spendingCategories } from '../data/spendingCategoryData'
import { spendingService } from '../services/spendingService'

export const useSpendingStore = defineStore('spending', () => {
  const spendingForm = ref({ ...defaultSpendingForm })
  const latestSurvey = ref(null)
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
      latestSurvey.value = data?.survey || latestSurvey.value
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
      latestSurvey.value = Array.isArray(data) && data.length ? data[0] : null
      return latestSurvey.value
    } catch (err) {
      error.value = err
      latestSurvey.value = null
      throw err
    } finally {
      isLoading.value = false
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
    reportData,
    isLoading,
    error,
    totalMonthly,
    updateSpendingForm,
    resetSpendingForm,
    createSurvey,
    uploadCsv,
    fetchLatestSurvey,
    fetchReportData,
  }
})
