import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

import { authService } from '../services/authService'
import { clearTokens, getStoredTokens, saveTokens } from '../services/api'

const MOCK_ACCESS_TOKEN = 'mock-dev-access-token'
const MOCK_REFRESH_TOKEN = 'mock-dev-refresh-token'
const MOCK_USER = {
  id: 'mock-user',
  email: 'demo@cardfit.local',
  username: '데모 사용자',
  selected_card_id: null,
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
}

export const useAuthStore = defineStore('auth', () => {
  const storedTokens = getStoredTokens()
  const accessToken = ref(storedTokens.access)
  const refreshToken = ref(storedTokens.refresh)
  const isMockSession = computed(() => import.meta.env.DEV && accessToken.value === MOCK_ACCESS_TOKEN)
  const user = ref(import.meta.env.DEV && storedTokens.access === MOCK_ACCESS_TOKEN ? MOCK_USER : null)
  const isLoading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => Boolean(accessToken.value))

  function setAuth(payload) {
    user.value = payload?.user || user.value
    accessToken.value = payload?.tokens?.access || accessToken.value
    refreshToken.value = payload?.tokens?.refresh || refreshToken.value

    saveTokens({
      access: accessToken.value,
      refresh: refreshToken.value,
    })
  }

  async function login(credentials) {
    isLoading.value = true
    error.value = null

    try {
      const { data } = await authService.login(credentials)
      setAuth(data)
      return data
    } catch (err) {
      error.value = err
      throw err
    } finally {
      isLoading.value = false
    }
  }

  function loginWithMock() {
    if (!import.meta.env.DEV) return null

    const payload = {
      user: MOCK_USER,
      tokens: {
        access: MOCK_ACCESS_TOKEN,
        refresh: MOCK_REFRESH_TOKEN,
      },
    }
    setAuth(payload)
    return payload
  }

  async function register(payload) {
    isLoading.value = true
    error.value = null

    try {
      const { data } = await authService.register(payload)
      setAuth(data)
      return data
    } catch (err) {
      error.value = err
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function fetchProfile() {
    if (!isAuthenticated.value) return null
    if (isMockSession.value) {
      user.value = MOCK_USER
      return user.value
    }

    const { data } = await authService.fetchProfile()
    user.value = data
    return data
  }

  async function logout() {
    const tokenForLogout = refreshToken.value

    user.value = null
    accessToken.value = null
    refreshToken.value = null
    clearTokens()

    if (tokenForLogout && tokenForLogout !== MOCK_REFRESH_TOKEN) {
      try {
        await authService.logout(tokenForLogout)
      } catch {
        // Local logout should still succeed if the backend is unavailable.
      }
    }
  }

  return {
    user,
    accessToken,
    refreshToken,
    isLoading,
    error,
    isAuthenticated,
    loginWithMock,
    login,
    register,
    fetchProfile,
    logout,
  }
})
