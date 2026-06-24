<template>
  <div class="relative min-h-[calc(100vh-72px)] overflow-hidden bg-[#fbf9f8]">
    <main class="relative mx-auto grid min-h-[calc(100vh-72px)] max-w-[1200px] items-center gap-12 px-5 py-14 lg:grid-cols-[1fr_440px] lg:px-8">
      <section class="hidden flex-col gap-7 lg:flex">
        <div>
          <h1 class="max-w-xl text-6xl font-extrabold leading-tight text-[#001278]">
            AI가 제안하는<br />
            나만의 맞춤 카드
          </h1>
          <p class="mt-5 whitespace-nowrap text-lg leading-8 text-[#454653]">
            소비 패턴 분석부터 혜택 계산, 카드 추천까지 한 번에 확인하세요.
          </p>
          <p class="mt-3 text-base font-semibold text-[#1b1c1c]">
            "내 소비 패턴에 맞는 카드를 찾는 가장 빠른 방법"
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
                당신을 위한<br />
                카드 추천
              </p>
              <p class="mt-3 text-sm font-medium text-white/75">
                소비 패턴에 맞춘 혜택 매칭
              </p>
            </div>
          </div>
        </div>
      </section>

      <LoginForm
        v-model:email="email"
        v-model:password="password"
        :loading="isLoading"
        :error-message="errorMessage"
        @submit="handleSubmit"
      />
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import LoginForm from '../components/auth/LoginForm.vue'
import { getApiErrorMessage } from '../services/api'
import { useAuthStore } from '../stores/authStore'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const errorMessage = ref('')

const isLoading = computed(() => authStore.isLoading)

onMounted(() => {
  if (authStore.isAuthenticated) {
    router.replace(getRedirectPath())
  }
})

function getRedirectPath() {
  return route.query.redirect ? route.query.redirect.toString() : '/'
}

async function handleSubmit() {
  errorMessage.value = ''

  try {
    await authStore.login({ email: email.value, password: password.value })
    await authStore.fetchProfile().catch(() => null)
    router.push(getRedirectPath())
  } catch (error) {
    errorMessage.value = getApiErrorMessage(
      error,
      '로그인에 실패했습니다. 이메일과 비밀번호를 확인해 주세요.',
    )
  }
}

</script>
