import axios from 'axios'

export const TOKEN_STORAGE_KEYS = {
  access: 'cardfit_access_token',
  refresh: 'cardfit_refresh_token',
}

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  headers: {
    Accept: 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const accessToken = localStorage.getItem(TOKEN_STORAGE_KEYS.access)

  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`
  }

  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token refresh or forced logout can be added here after API policy is finalized.
    }

    return Promise.reject(error)
  },
)

export function saveTokens(tokens) {
  if (tokens?.access) {
    localStorage.setItem(TOKEN_STORAGE_KEYS.access, tokens.access)
  }

  if (tokens?.refresh) {
    localStorage.setItem(TOKEN_STORAGE_KEYS.refresh, tokens.refresh)
  }
}

export function clearTokens() {
  localStorage.removeItem(TOKEN_STORAGE_KEYS.access)
  localStorage.removeItem(TOKEN_STORAGE_KEYS.refresh)
}

export function getStoredTokens() {
  return {
    access: localStorage.getItem(TOKEN_STORAGE_KEYS.access),
    refresh: localStorage.getItem(TOKEN_STORAGE_KEYS.refresh),
  }
}

export default api
