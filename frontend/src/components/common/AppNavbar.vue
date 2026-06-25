<template>
  <header class="sticky top-0 z-50 border-b border-[#dcdddd] bg-[#fbf9f8]/95 backdrop-blur">
    <div class="mx-auto flex h-[72px] max-w-[1200px] items-center justify-between px-5 lg:px-8">
      <div class="flex items-center gap-10">
        <RouterLink to="/" class="text-2xl font-extrabold text-[#001278]">CardFit</RouterLink>

        <nav class="hidden items-center gap-8 text-base md:flex">
          <RouterLink
            v-for="item in navItems"
            :key="item.to"
            :to="item.to"
            class="border-b-2 pb-1 font-semibold transition"
            :class="isActive(item.to) ? 'border-[#001278] text-[#001278]' : 'border-transparent text-[#5d5f5f] hover:text-[#001278]'"
          >
            {{ item.label }}
          </RouterLink>
        </nav>
      </div>

      <div class="flex items-center gap-3">
        <template v-if="isLoggedIn">
          <span
            class="hidden rounded-full border border-[#d9def0] bg-white px-3 py-1.5 text-xs font-extrabold text-[#001278] shadow-sm sm:inline-flex"
            aria-live="polite"
          >
            자동 로그아웃 {{ remainingIdleTimeLabel }}
          </span>
          <RouterLink
            to="/profile"
            class="hidden rounded-lg px-4 py-2 text-sm font-semibold text-[#5d5f5f] transition hover:bg-[#f0eded] hover:text-[#001278] sm:inline-flex"
          >
            마이페이지
          </RouterLink>
          <button
            type="button"
            class="rounded-lg border border-[#001278] px-4 py-2 text-sm font-semibold text-[#001278] transition hover:bg-[#001278] hover:text-white"
            @click="openLogoutConfirm"
          >
            로그아웃
          </button>
        </template>
        <RouterLink
          v-else
          to="/login"
          class="rounded-lg bg-[#001278] px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-[#1428a0]"
        >
          로그인
        </RouterLink>
      </div>
    </div>

  </header>

  <Teleport to="body">
    <div
      v-if="isLogoutConfirmOpen"
      class="fixed inset-0 z-[100] flex items-center justify-center bg-black/45 px-4 py-6"
      role="dialog"
      aria-modal="true"
      aria-labelledby="logout-confirm-title"
      @click.self="closeLogoutConfirm"
    >
      <section class="w-full max-w-[420px] rounded-lg bg-white shadow-2xl">
        <div class="border-b border-[#ececf2] px-6 py-5">
          <p class="text-sm font-extrabold text-[#001278]">로그아웃 확인</p>
          <h2 id="logout-confirm-title" class="mt-1 text-xl font-extrabold text-[#111827]">
            로그아웃할까요?
          </h2>
          <p class="mt-2 text-sm leading-6 text-[#4d5870]">
            현재 계정에서 나가면 다시 로그인해야 서비스를 이용할 수 있어요.
          </p>
        </div>

        <div class="flex justify-end gap-3 px-6 py-5">
          <button
            type="button"
            class="inline-flex h-11 items-center justify-center rounded-md border border-[#d4d8e8] bg-white px-5 text-sm font-bold text-[#4d5870] transition hover:bg-[#f7f7fa]"
            :disabled="isLoggingOut"
            @click="closeLogoutConfirm"
          >
            취소
          </button>
          <button
            type="button"
            class="inline-flex h-11 min-w-[104px] items-center justify-center rounded-md bg-[#001278] px-5 text-sm font-extrabold text-white transition hover:bg-[#1428a0] disabled:cursor-not-allowed disabled:bg-[#8b93c8]"
            :disabled="isLoggingOut"
            @click="confirmLogout"
          >
            {{ isLoggingOut ? '로그아웃 중' : '로그아웃' }}
          </button>
        </div>
      </section>
    </div>
  </Teleport>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useAuthState } from '../../composables/useAuthState'

const IDLE_TIMEOUT_SECONDS = 600
const ACTIVITY_EVENTS = ['pointerdown', 'keydown', 'scroll', 'touchstart', 'mousemove']

const { authStore, isLoggedIn } = useAuthState()
const router = useRouter()
const route = useRoute()
const isLogoutConfirmOpen = ref(false)
const isLoggingOut = ref(false)
const lastActivityAt = ref(Date.now())
const now = ref(Date.now())
let idleTimer = null
let lastActivityUpdateAt = 0

const remainingIdleSeconds = computed(() => {
  if (!isLoggedIn.value) return IDLE_TIMEOUT_SECONDS

  const elapsedSeconds = Math.floor((now.value - lastActivityAt.value) / 1000)
  return Math.max(0, IDLE_TIMEOUT_SECONDS - elapsedSeconds)
})
const remainingIdleTimeLabel = computed(() => {
  const minutes = Math.floor(remainingIdleSeconds.value / 60)
  const seconds = remainingIdleSeconds.value % 60
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
})

const navItems = [
  { label: '추천 홈', to: '/' },
  { label: '소비 리포트', to: '/report' },
  { label: 'AI 카드 추천', to: '/ai-recommendations' },
  { label: '카드 검색', to: '/cards' },
  { label: '카드 비교', to: '/compare' },
  { label: '커뮤니티', to: '/community' },
]

function isActive(path) {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}

function openLogoutConfirm() {
  isLogoutConfirmOpen.value = true
}

function closeLogoutConfirm() {
  if (isLoggingOut.value) return
  isLogoutConfirmOpen.value = false
}

function markUserActivity() {
  if (!isLoggedIn.value) return

  const currentTime = Date.now()
  if (currentTime - lastActivityUpdateAt < 1000) return

  lastActivityUpdateAt = currentTime
  lastActivityAt.value = currentTime
  now.value = currentTime
}

function startIdleTimer() {
  stopIdleTimer()
  lastActivityAt.value = Date.now()
  now.value = Date.now()
  lastActivityUpdateAt = 0

  idleTimer = window.setInterval(() => {
    now.value = Date.now()

    if (remainingIdleSeconds.value <= 0 && !isLoggingOut.value) {
      confirmLogout()
    }
  }, 1000)

  ACTIVITY_EVENTS.forEach((eventName) => {
    window.addEventListener(eventName, markUserActivity, { passive: true })
  })
}

function stopIdleTimer() {
  if (idleTimer) {
    window.clearInterval(idleTimer)
    idleTimer = null
  }

  ACTIVITY_EVENTS.forEach((eventName) => {
    window.removeEventListener(eventName, markUserActivity)
  })
}

async function confirmLogout() {
  isLoggingOut.value = true

  try {
    await authStore.logout()
    isLogoutConfirmOpen.value = false
    router.push({ name: 'login' })
  } finally {
    isLoggingOut.value = false
  }
}

watch(
  isLoggedIn,
  (loggedIn) => {
    if (loggedIn) {
      startIdleTimer()
    } else {
      stopIdleTimer()
      isLogoutConfirmOpen.value = false
    }
  },
  { immediate: true },
)

onMounted(() => {
  if (isLoggedIn.value) startIdleTimer()
})

onBeforeUnmount(stopIdleTimer)
</script>
