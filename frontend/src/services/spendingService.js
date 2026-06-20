import api from './api'

export const spendingService = {
  fetchSurveys() {
    return api.get('/api/spending/')
  },

  createSurvey(payload) {
    return api.post('/api/spending/', payload)
  },

  fetchSurveyDetail(id) {
    return api.get(`/api/spending/${id}/`)
  },

  updateSurvey(id, payload) {
    return api.put(`/api/spending/${id}/`, payload)
  },

  deleteSurvey(id) {
    return api.delete(`/api/spending/${id}/`)
  },

  uploadCsv(file, surveyData = {}) {
    const formData = new FormData()
    formData.append('file', file)
    
    // 설문 정보 추가
    if (surveyData.age_group) formData.append('age_group', surveyData.age_group)
    if (surveyData.income_level) formData.append('income_level', surveyData.income_level)
    if (surveyData.max_annual_fee !== undefined) formData.append('max_annual_fee', surveyData.max_annual_fee)

    return api.post('/api/spending/upload-csv/', formData)
  },

  fetchLatestSurvey() {
    return api.get('/api/spending/')
  },

  fetchSpendingSummary(params = {}) {
    return api.get('/api/reports/spending-summary/', { params })
  },

  fetchCategoryBreakdown(params = {}) {
    return api.get('/api/reports/category-breakdown/', { params })
  },
}
