import api from './api'

export const authService = {
  getOAuthStartUrl(provider, next = '/') {
    const baseUrl = String(api.defaults.baseURL || '').replace(/\/$/, '')
    const params = new URLSearchParams({ next })
    return `${baseUrl}/api/accounts/oauth/${provider}/?${params.toString()}`
  },

  register(payload) {
    return api.post('/api/accounts/register/', payload)
  },

  login(payload) {
    return api.post('/api/accounts/login/', payload)
  },

  logout(refresh) {
    return api.post('/api/accounts/logout/', { refresh })
  },

  refreshToken(refresh) {
    return api.post('/api/accounts/token/refresh/', { refresh })
  },

  fetchProfile() {
    return api.get('/api/accounts/profile/')
  },

  updateProfile(payload) {
    return api.put('/api/accounts/profile/', payload)
  },

  selectCard(selectedCard) {
    return api.put('/api/accounts/select-card/', { selected_card: selectedCard })
  },
}
