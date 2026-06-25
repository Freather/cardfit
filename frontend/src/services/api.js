import axios from 'axios'

export const TOKEN_STORAGE_KEYS = {
  access: 'cardfit_access_token',
  refresh: 'cardfit_refresh_token',
}

const DEFAULT_ERROR_MESSAGE = '잠시 후 다시 시도해주세요.'

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

    if (error.response?.status === 401 && originalRequest && !originalRequest._retry) {
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

    normalizeApiError(error)
    return Promise.reject(error)
  },
)

export function normalizeApiError(error) {
  if (!error) return error

  error.status = error.response?.status || null
  error.isNetworkError = Boolean(error.request && !error.response)
  error.isTimeout = error.code === 'ECONNABORTED'
  error.userMessage = getApiErrorMessage(error)

  return error
}

export function getApiErrorMessage(error, fallback = DEFAULT_ERROR_MESSAGE) {
  if (!error) return fallback

  if (error.userMessage && error.userMessage !== DEFAULT_ERROR_MESSAGE) {
    return error.userMessage
  }

  if (error.code === 'ECONNABORTED') {
    return '응답이 늦어지고 있어요. 잠시 후 다시 시도해주세요.'
  }

  if (error.request && !error.response) {
    return '서버와 연결되지 않았어요. 실행 상태를 확인해보세요.'
  }

  const errorData = error.response?.data
  const parsedMessage = extractErrorMessage(errorData)
  if (parsedMessage) return parsedMessage

  if (error.response?.status === 401) {
    return '로그인이 끝났어요. 다시 로그인해주세요.'
  }

  if (error.response?.status === 403) {
    return '지금 계정으로는 할 수 없어요.'
  }

  if (error.response?.status === 404) {
    return '데이터를 찾지 못했어요.'
  }

  if (error.response?.status >= 500) {
    return '서버가 잠시 불안정해요. 다시 시도해주세요.'
  }

  return fallback
}

function extractErrorMessage(errorData) {
  if (!errorData) return ''
  if (typeof errorData === 'string') return errorData
  if (Array.isArray(errorData)) return errorData.find(Boolean) || ''
  if (typeof errorData !== 'object') return ''

  if (errorData.detail) return extractErrorMessage(errorData.detail)
  if (errorData.message) return extractErrorMessage(errorData.message)
  if (errorData.error) return extractErrorMessage(errorData.error)

  const firstError = Object.values(errorData).find(Boolean)
  return extractErrorMessage(firstError)
}

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
