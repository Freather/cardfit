<template>
  <main class="flex min-h-[calc(100vh-72px)] items-center justify-center bg-[#fbf9f8] px-5 py-12">
    <section class="w-full max-w-[460px] rounded-2xl border border-white/70 bg-white p-8 shadow-[0_28px_70px_rgba(0,0,0,0.12)]">
      <p class="text-sm font-black text-[#001278]">소셜 로그인</p>
      <h1 class="mt-2 text-3xl font-extrabold text-[#111827]">이메일만 입력하면 끝나요</h1>
      <p class="mt-3 text-sm leading-6 text-[#4d5870]">
        {{ providerLabel }}에서 이메일 권한을 받을 수 없어 CardFit 계정에 사용할 이메일을 직접 입력해주세요.
      </p>
      <p v-if="nickname" class="mt-3 rounded-xl bg-[#eef3ff] px-4 py-3 text-sm font-semibold text-[#001278]">
        {{ nickname }}님으로 로그인 확인 완료
      </p>

      <form class="mt-7 space-y-5" @submit.prevent="handleSubmit">
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

        <div v-if="errorMessage" class="rounded-xl bg-[#ffdad6] p-4 text-sm text-[#93000a]">
          {{ errorMessage }}
        </div>

        <button
          type="submit"
          :disabled="isSubmitting"
          class="w-full rounded-xl bg-[#001278] py-4 text-base font-bold text-white shadow-[0_14px_30px_rgba(0,18,120,0.25)] transition hover:bg-[#1428a0] active:scale-[0.99] disabled:cursor-not-allowed disabled:opacity-60"
        >
          {{ isSubmitting ? '계정 연결 중...' : '이메일로 계속하기' }}
        </button>

        <RouterLink
          :to="{ name: 'login' }"
          class="block text-center text-sm font-bold text-[#5f6575] transition hover:text-[#001278]"
        >
          로그인으로 돌아가기
        </RouterLink>
      </form>
    </section>
  </main>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'

import { getApiErrorMessage } from '../services/api'
import { authService } from '../services/authService'
import { useAuthStore } from '../stores/authStore'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const errorMessage = ref('')
const isSubmitting = ref(false)

const token = computed(() => String(route.query.token || ''))
const provider = computed(() => String(route.query.provider || 'oauth'))
const nickname = computed(() => String(route.query.nickname || ''))
const nextPath = computed(() => String(route.query.next || '/'))
const providerLabel = computed(() => (provider.value === 'kakao' ? '카카오' : '소셜 계정'))

onMounted(() => {
  if (!token.value) {
    router.replace({ name: 'login', query: { error: '소셜 로그인 정보가 없어요. 다시 로그인해주세요.' } })
  }
})

async function handleSubmit() {
  errorMessage.value = ''
  isSubmitting.value = true

  try {
    const { data } = await authService.completeOAuthEmail({
      token: token.value,
      email: email.value.trim().toLowerCase(),
      next: nextPath.value,
    })
    authStore.setTokens(data.tokens)
    await authStore.fetchProfile().catch(() => null)
    router.replace(data.next?.startsWith('/') ? data.next : '/')
  } catch (error) {
    errorMessage.value = getApiErrorMessage(error, '이메일을 연결하지 못했어요. 다시 시도해주세요.')
  } finally {
    isSubmitting.value = false
  }
}
</script>
