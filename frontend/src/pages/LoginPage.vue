<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="w-full max-w-md space-y-8">
      <div class="bg-white py-10 px-8 shadow-xl rounded-3xl border border-gray-200">
        <div class="space-y-3 text-center">
          <p class="text-sm font-semibold text-blue-600 uppercase tracking-[0.25em]">CardFit</p>
          <h1 class="text-3xl font-bold text-gray-900">로그인</h1>
          <p class="text-sm text-gray-500">나만의 소비 패턴 기반 카드 추천과 리포트를 확인하세요.</p>
        </div>

        <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
          <div class="rounded-2xl shadow-sm -space-y-px">
            <div>
              <label for="email" class="sr-only">이메일</label>
              <input
                id="email"
                type="email"
                autocomplete="email"
                v-model="email"
                required
                class="appearance-none rounded-t-2xl relative block w-full px-5 py-4 border border-gray-300 placeholder-gray-400 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="이메일"
              />
            </div>
            <div>
              <label for="password" class="sr-only">비밀번호</label>
              <input
                id="password"
                type="password"
                autocomplete="current-password"
                v-model="password"
                required
                class="appearance-none rounded-b-2xl relative block w-full px-5 py-4 border border-gray-300 placeholder-gray-400 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="비밀번호"
              />
            </div>
          </div>

          <div v-if="errorMessage" class="rounded-xl bg-red-50 border border-red-200 p-4 text-sm text-red-700">
            {{ errorMessage }}
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="group relative w-full flex justify-center py-4 px-6 border border-transparent text-sm font-semibold rounded-2xl text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition disabled:opacity-50"
          >
            {{ isLoading ? '로그인 중...' : '로그인' }}
          </button>
        </form>

        <p class="mt-6 text-center text-sm text-gray-500">
          아직 계정이 없으신가요?
          <router-link to="/signup" class="font-semibold text-blue-600 hover:text-blue-700">회원가입</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const errorMessage = ref('')

const isLoading = computed(() => authStore.isLoading)

const handleSubmit = async () => {
  errorMessage.value = ''

  try {
    await authStore.login({ email: email.value, password: password.value })
    await authStore.fetchProfile().catch(() => {})
    const redirect = route.query.redirect ? route.query.redirect.toString() : '/'
    router.push(redirect)
  } catch (error) {
    let message = '로그인에 실패했습니다. 다시 시도해 주세요.'
    
    const errorData = error?.response?.data
    if (errorData) {
      if (errorData.detail) {
        message = errorData.detail
      } else if (typeof errorData === 'object') {
        const firstError = Object.values(errorData)[0]
        if (Array.isArray(firstError) && firstError[0]) {
          message = firstError[0]
        } else if (typeof firstError === 'string') {
          message = firstError
        }
      }
    }
    
    errorMessage.value = message
  }
}
</script>
