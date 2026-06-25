import api from './api'

export const aiService = {
  fetchRecommendations(params = {}) {
    return api.get('/api/ai/recommend/', { params })
  },

  recommendFromSpending(payload) {
    return api.post('/api/ai/recommend/', payload)
  },

  chat(payload) {
    return api.post('/api/ai/chat/', payload)
  },
}
