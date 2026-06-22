<template>
  <div class="min-h-[calc(100vh-72px)] bg-[#fbf9f8]">
    <main class="mx-auto grid min-h-[calc(100vh-72px)] max-w-[1200px] items-center gap-12 px-5 py-14 lg:grid-cols-[1fr_440px] lg:px-8">
      <section class="hidden flex-col gap-7 lg:flex">
        <div>
          <h1 class="max-w-xl text-6xl font-extrabold leading-tight text-[#001278]">
            AI가 제안하는 나만의 맞춤 카드
          </h1>
          <p class="mt-5 text-2xl font-semibold text-[#5d5f5f]">CardFit</p>
        </div>

        <div class="relative aspect-[4/3] max-w-[620px] overflow-hidden rounded-xl border border-[#c5c5d5] bg-[#001278] shadow-2xl">
          <img
            src="../assets/hero.png"
            alt="CardFit 서비스 미리보기"
            class="h-full w-full object-cover opacity-80"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-[#001278]/70 via-[#001278]/10 to-transparent"></div>
          <div class="absolute bottom-6 left-6 max-w-[82%] rounded-lg border border-white/30 bg-white/80 p-5 backdrop-blur">
            <p class="text-base font-semibold text-[#1b1c1c]">
              "내 소비 패턴에 딱 맞는 카드를 찾는 가장 스마트한 방법"
            </p>
          </div>
        </div>
      </section>

      <section class="mx-auto w-full max-w-[440px] rounded-xl border border-[#c5c5d5] bg-white p-8 shadow-xl lg:p-10">
        <div class="mb-8">
          <p class="text-sm font-bold text-[#001278] lg:hidden">CardFit</p>
          <h1 class="mt-2 text-4xl font-extrabold text-[#1b1c1c]">로그인</h1>
          <p class="mt-3 text-sm leading-6 text-[#454653]">
            서비스를 이용하려면 계정에 로그인하세요.
          </p>
        </div>

        <form class="space-y-5" @submit.prevent="handleSubmit">
          <label class="block space-y-2">
            <span class="text-sm font-semibold text-[#454653]">이메일</span>
            <input
              v-model="email"
              type="email"
              autocomplete="email"
              required
              class="w-full rounded-lg border border-[#c5c5d5] bg-[#fbf9f8] px-4 py-4 text-base text-[#1b1c1c] outline-none transition focus:border-[#001278] focus:ring-4 focus:ring-[#001278]/10"
              placeholder="example@cardfit.com"
            />
          </label>

          <label class="block space-y-2">
            <span class="text-sm font-semibold text-[#454653]">비밀번호</span>
            <input
              v-model="password"
              type="password"
              autocomplete="current-password"
              required
              class="w-full rounded-lg border border-[#c5c5d5] bg-[#fbf9f8] px-4 py-4 text-base text-[#1b1c1c] outline-none transition focus:border-[#001278] focus:ring-4 focus:ring-[#001278]/10"
              placeholder="비밀번호"
            />
          </label>

          <div class="flex justify-end">
            <button type="button" class="text-sm font-semibold text-[#001278] hover:underline">
              비밀번호 찾기
            </button>
          </div>

          <div v-if="errorMessage" class="rounded-lg bg-[#ffdad6] p-4 text-sm text-[#93000a]">
            {{ errorMessage }}
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="w-full rounded-lg bg-[#001278] py-4 text-base font-bold text-white shadow-md transition hover:bg-[#1428a0] active:scale-[0.99] disabled:cursor-not-allowed disabled:opacity-60"
          >
            {{ isLoading ? '로그인 중...' : '로그인' }}
          </button>

          <router-link
            to="/signup"
            class="flex w-full justify-center rounded-lg border border-[#001278] py-4 text-base font-bold text-[#001278] transition hover:bg-[#001278]/5"
          >
            회원가입
          </router-link>
        </form>

        <div v-if="isDev" class="mt-6 rounded-lg border border-dashed border-[#8f9cff] bg-[#dfe0ff]/50 p-4">
          <p class="text-sm font-bold text-[#001278]">개발용 미리보기</p>
          <p class="mt-1 text-sm leading-5 text-[#2638ad]">
            백엔드 없이 로그인 상태를 만들고 AI 리포트를 확인합니다.
          </p>
          <button
            type="button"
            class="mt-3 w-full rounded-lg bg-[#1428a0] px-4 py-3 text-sm font-bold text-white transition hover:bg-[#001278]"
            @click="handleMockLogin"
          >
            Mock 로그인으로 리포트 보기
          </button>
        </div>
      </section>
    </main>
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
const isDev = import.meta.env.DEV

const isLoading = computed(() => authStore.isLoading)

function getRedirectPath() {
  return route.query.redirect ? route.query.redirect.toString() : '/'
}

const handleSubmit = async () => {
  errorMessage.value = ''

  try {
    await authStore.login({ email: email.value, password: password.value })
    await authStore.fetchProfile().catch(() => {})
    router.push(getRedirectPath())
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

const handleMockLogin = () => {
  authStore.loginWithMock()
  router.push(getRedirectPath() === '/' ? '/report' : getRedirectPath())
}
</script>
