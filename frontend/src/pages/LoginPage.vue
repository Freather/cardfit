<template>
  <div class="relative min-h-[calc(100vh-72px)] overflow-hidden bg-[#fbf9f8]">
    <div class="pointer-events-none absolute inset-0">
      <div class="absolute left-[-180px] top-[-220px] h-[520px] w-[520px] rounded-full bg-[#dfe0ff]/70 blur-3xl"></div>
      <div class="absolute bottom-[-260px] right-[-180px] h-[560px] w-[560px] rounded-full bg-[#bcc3ff]/40 blur-3xl"></div>
    </div>

    <main class="relative mx-auto grid min-h-[calc(100vh-72px)] max-w-[1200px] items-center gap-12 px-5 py-14 lg:grid-cols-[1fr_440px] lg:px-8">
      <section class="hidden flex-col gap-7 lg:flex">
        <div>
          <h1 class="max-w-xl text-6xl font-extrabold leading-tight text-[#001278]">
            AI가 제안하는<br />
            나만의 맞춤 카드
          </h1>
          <p class="mt-5 whitespace-nowrap text-lg leading-8 text-[#454653]">
            소비 패턴을 분석해 혜택 계산부터 카드 추천까지 한 번에 확인하세요.
          </p>
          <p class="mt-3 text-base font-semibold text-[#1b1c1c]">
            "내 소비 패턴에 딱 맞는 카드를 찾는 가장 스마트한 방법"
          </p>
        </div>

        <div class="group relative aspect-[4/3] max-w-[620px] overflow-hidden rounded-2xl border border-white/70 bg-[#001278] shadow-[0_32px_80px_rgba(0,18,120,0.20)]">
          <img
            src="../assets/hero.png"
            alt="CardFit 서비스 미리보기"
            class="h-full w-full object-cover opacity-85 transition duration-500 group-hover:scale-[1.03]"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-[#001278]/80 via-[#001278]/20 to-transparent"></div>
          <div class="absolute left-1/2 top-1/2 flex h-44 w-80 -translate-x-1/2 -translate-y-1/2 rotate-[-5deg] flex-col justify-between rounded-3xl border border-white/35 bg-white/15 p-7 shadow-2xl backdrop-blur-md">
            <div class="flex items-center justify-between">
              <span class="text-sm font-extrabold uppercase tracking-[0.28em] text-white/85">CardFit</span>
            </div>
            <div>
              <p class="text-xl font-extrabold leading-snug text-white">
                당신이 찾던<br />
                그 카드 추천
              </p>
              <p class="mt-3 text-sm font-medium text-white/75">
                소비 패턴에 맞춘 혜택 매칭
              </p>
            </div>
          </div>
        </div>
      </section>

      <section class="mx-auto w-full max-w-[440px] rounded-2xl border border-white/70 bg-white/85 p-8 shadow-[0_28px_70px_rgba(0,0,0,0.12)] backdrop-blur lg:p-10">
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
              class="w-full rounded-xl border border-[#c5c5d5] bg-white/80 px-4 py-4 text-base text-[#1b1c1c] outline-none transition placeholder:text-gray-400 focus:border-[#001278] focus:bg-white focus:ring-4 focus:ring-[#001278]/10"
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
              class="w-full rounded-xl border border-[#c5c5d5] bg-white/80 px-4 py-4 text-base text-[#1b1c1c] outline-none transition placeholder:text-gray-400 focus:border-[#001278] focus:bg-white focus:ring-4 focus:ring-[#001278]/10"
              placeholder="비밀번호"
            />
          </label>

          <div class="flex justify-end">
            <button type="button" class="text-sm font-semibold text-[#001278] transition hover:text-[#1428a0] hover:underline">
              비밀번호 찾기
            </button>
          </div>

          <div v-if="errorMessage" class="rounded-xl bg-[#ffdad6] p-4 text-sm text-[#93000a]">
            {{ errorMessage }}
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="w-full rounded-xl bg-[#001278] py-4 text-base font-bold text-white shadow-[0_14px_30px_rgba(0,18,120,0.25)] transition hover:bg-[#1428a0] active:scale-[0.99] disabled:cursor-not-allowed disabled:opacity-60"
          >
            {{ isLoading ? '로그인 중...' : '로그인' }}
          </button>

          <router-link
            to="/signup"
            class="flex w-full justify-center rounded-xl border border-[#001278] bg-white/70 py-4 text-base font-bold text-[#001278] transition hover:bg-[#001278]/5"
          >
            회원가입
          </router-link>
        </form>

        <div v-if="isDev" class="mt-6 rounded-xl border border-dashed border-[#8f9cff] bg-[#dfe0ff]/60 p-4">
          <p class="text-sm font-bold text-[#001278]">개발용 미리보기</p>
          <p class="mt-1 text-sm leading-5 text-[#2638ad]">
            백엔드 없이 로그인 상태를 만들고 AI 리포트를 확인합니다.
          </p>
          <button
            type="button"
            class="mt-3 w-full rounded-lg bg-[#1428a0] px-4 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-[#001278]"
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
