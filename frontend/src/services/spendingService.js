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

  uploadCsv(file) {
    const formData = new FormData()
    formData.append('file', file)

    return api.post('/api/spending/upload-csv/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  fetchSpendingSummary(params = {}) {
    return api.get('/api/reports/spending-summary/', { params })
  },

  fetchCategoryBreakdown(params = {}) {
    return api.get('/api/reports/category-breakdown/', { params })
  },
}
