<template>
  <main class="min-h-[calc(100vh-72px)] bg-[#fbf9f8] px-5 py-14">
    <div class="mx-auto grid max-w-[1120px] items-center gap-12 lg:grid-cols-[0.92fr_460px]">
      <section class="hidden lg:block">
        <p class="text-sm font-extrabold uppercase tracking-[0.28em] text-[#001278]">CardFit</p>
        <h1 class="mt-5 max-w-xl text-5xl font-extrabold leading-tight text-[#001278]">
          소비 데이터를 연결하고<br />
          더 정확한 추천을 받아보세요
        </h1>
        <p class="mt-5 max-w-xl text-base leading-7 text-[#454653]">
          CSV 업로드와 소비 설문을 기반으로 내 지출 패턴에 맞는 카드 혜택을 계산합니다.
        </p>

        <div class="mt-10 grid max-w-xl gap-4">
          <article
            v-for="item in signupBenefits"
            :key="item.title"
            class="rounded-xl border border-[#d9dcef] bg-white/70 p-5 shadow-sm"
          >
            <p class="text-sm font-extrabold text-[#001278]">{{ item.title }}</p>
            <p class="mt-2 text-sm leading-6 text-[#454653]">{{ item.description }}</p>
          </article>
        </div>
      </section>

      <SignupForm
        v-model:email="email"
        v-model:username="username"
        v-model:password="password"
        v-model:password-confirm="passwordConfirm"
        :loading="isLoading"
        :error-message="errorMessage"
        @submit="handleSubmit"
      />
    </div>
  </main>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import SignupForm from '../components/auth/SignupForm.vue'
import { useAuthStore } from '../stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const username = ref('')
const password = ref('')
const passwordConfirm = ref('')
const errorMessage = ref('')

const isLoading = computed(() => authStore.isLoading)

onMounted(() => {
  if (authStore.isAuthenticated) {
    router.replace({ name: 'home' })
  }
})

const signupBenefits = [
  {
    title: '소비 리포트',
    description: '카테고리별 지출 비중과 월별 소비 흐름을 한눈에 확인할 수 있습니다.',
  },
  {
    title: 'AI 카드 추천',
    description: '설문과 CSV 데이터를 바탕으로 예상 혜택이 큰 카드를 추천합니다.',
  },
  {
    title: '카드 비교',
    description: '관심 있는 카드를 최대 3개까지 담아 혜택과 조건을 비교할 수 있습니다.',
  },
]

async function handleSubmit() {
  errorMessage.value = ''

  if (password.value !== passwordConfirm.value) {
    errorMessage.value = '비밀번호와 비밀번호 확인이 일치하지 않습니다.'
    return
  }

  try {
    await authStore.register({
      email: email.value,
      username: username.value,
      password: password.value,
      password_confirm: passwordConfirm.value,
    })
    await authStore.fetchProfile().catch(() => null)
    router.push({ name: 'home' })
  } catch (error) {
    errorMessage.value = getSignupErrorMessage(error)
  }
}

function getSignupErrorMessage(error) {
  const fallback = '회원가입에 실패했습니다. 다시 시도해주세요.'
  const errorData = error?.response?.data

  if (!errorData) return fallback
  if (errorData.detail) return errorData.detail
  if (typeof errorData !== 'object') return fallback

  const firstError = Object.values(errorData)[0]
  if (Array.isArray(firstError) && firstError[0]) return firstError[0]
  if (typeof firstError === 'string') return firstError

  return fallback
}
</script>
