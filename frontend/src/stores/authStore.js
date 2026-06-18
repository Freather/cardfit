import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

import { authService } from '../services/authService'
import { clearTokens, getStoredTokens, saveTokens } from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  const storedTokens = getStoredTokens()
  const user = ref(null)
  const accessToken = ref(storedTokens.access)
  const refreshToken = ref(storedTokens.refresh)
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

    if (tokenForLogout) {
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
    login,
    register,
    fetchProfile,
    logout,
  }
})
