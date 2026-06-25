<template>
  <section class="flex min-h-[calc(100vh-72px)] items-center justify-center bg-[#fbf9f8] px-5 py-12">
    <div class="w-full max-w-[420px] rounded-2xl border border-white/70 bg-white p-8 text-center shadow-[0_28px_70px_rgba(0,0,0,0.12)]">
      <p class="text-sm font-black text-[#001278]">소셜 로그인</p>
      <h1 class="mt-2 text-2xl font-extrabold text-[#111827]">{{ title }}</h1>
      <p class="mt-3 text-sm leading-6 text-[#4d5870]">{{ message }}</p>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { useAuthStore } from '../stores/authStore'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const status = ref('loading')

const title = computed(() => (status.value === 'error' ? '로그인하지 못했어요' : '로그인 처리 중입니다'))
const message = computed(() =>
  status.value === 'error'
    ? '잠시 후 다시 시도하거나 일반 로그인을 이용해주세요.'
    : '계정 정보를 확인하고 있어요.',
)

onMounted(async () => {
  const access = String(route.query.access || '')
  const refresh = String(route.query.refresh || '')
  const error = String(route.query.error || '')
  const next = String(route.query.next || '/')

  if (error || !access || !refresh) {
    status.value = 'error'
    window.setTimeout(() => {
      router.replace({ name: 'login', query: error ? { error } : {} })
    }, 1400)
    return
  }

  authStore.setTokens({ access, refresh })
  await authStore.fetchProfile().catch(() => null)
  router.replace(next.startsWith('/') ? next : '/')
})
</script>
