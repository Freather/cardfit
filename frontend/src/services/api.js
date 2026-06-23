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
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest?._retry) {
      const refreshToken = localStorage.getItem(TOKEN_STORAGE_KEYS.refresh)

      if (refreshToken) {
        originalRequest._retry = true

        try {
          const { data } = await axios.post(
            `${api.defaults.baseURL}/api/accounts/token/refresh/`,
            { refresh: refreshToken },
          )

          saveTokens({
            access: data.access,
            refresh: data.refresh || refreshToken,
          })

          originalRequest.headers = originalRequest.headers || {}
          originalRequest.headers.Authorization = `Bearer ${data.access}`
          return api(originalRequest)
        } catch {
          clearTokens()
        }
      }
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
