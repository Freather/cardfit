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
          <RouterLink
            to="/profile"
            class="hidden rounded-lg px-4 py-2 text-sm font-semibold text-[#5d5f5f] transition hover:bg-[#f0eded] hover:text-[#001278] sm:inline-flex"
          >
            마이페이지
          </RouterLink>
          <button
            type="button"
            class="rounded-lg border border-[#001278] px-4 py-2 text-sm font-semibold text-[#001278] transition hover:bg-[#001278] hover:text-white"
            @click="handleLogout"
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
</template>

<script setup>
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useAuthState } from '../../composables/useAuthState'

const { authStore, isLoggedIn } = useAuthState()
const router = useRouter()
const route = useRoute()

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

async function handleLogout() {
  await authStore.logout()
  router.push({ name: 'login' })
}
</script>
