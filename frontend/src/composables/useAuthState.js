import { computed } from 'vue'

import { useAuthStore } from '../stores/authStore'

export function useAuthState() {
  const authStore = useAuthStore()

  const isLoggedIn = computed(() => authStore.isAuthenticated)
  const user = computed(() => authStore.user || null)
  const displayName = computed(() => user.value?.username || user.value?.email || '사용자')
  const displayEmail = computed(() => user.value?.email || '')

  async function ensureProfile() {
    if (!isLoggedIn.value) return null
    if (authStore.user) return authStore.user

    return authStore.fetchProfile().catch(() => null)
  }

  return {
    authStore,
    isLoggedIn,
    user,
    displayName,
    displayEmail,
    ensureProfile,
  }
}
