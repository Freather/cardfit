<template>
  <header class="bg-blue-800 text-white">
    <div class="max-w-7xl mx-auto h-16 flex items-center justify-between px-8">
      <!-- 로고 -->
      <RouterLink to="/" class="text-2xl font-bold">CardFit</RouterLink>

      <!-- 메뉴 -->
      <nav class="flex gap-10 text-sm">
        <RouterLink to="/" class="hover:text-blue-200">홈</RouterLink>
        <RouterLink to="/report" class="hover:text-blue-200" v-if="isLoggedIn">소비 분석</RouterLink>
        <RouterLink to="/cards" class="hover:text-blue-200">카드 검색</RouterLink>
        <RouterLink to="/compare" class="hover:text-blue-200">리포트</RouterLink>
      </nav>

      <!-- 우측 -->
      <div class="flex items-center gap-3">
        <template v-if="isLoggedIn">
          <RouterLink
            to="/profile"
            class="bg-blue-700 px-5 py-2 rounded-full text-sm hover:bg-blue-600 transition"
          >
            마이페이지
          </RouterLink>
          <button
            type="button"
            class="px-5 py-2 rounded-full text-sm text-blue-200 hover:text-white hover:bg-blue-700 transition"
            @click="handleLogout"
          >
            로그아웃
          </button>
        </template>
        <RouterLink
          v-else
          to="/login"
          class="bg-blue-700 px-5 py-2 rounded-full text-sm hover:bg-blue-600 transition"
        >
          로그인
        </RouterLink>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/authStore'

const authStore = useAuthStore()
const router = useRouter()
const isLoggedIn = computed(() => authStore.isAuthenticated)

async function handleLogout() {
  await authStore.logout()
  router.push({ name: 'login' })
}
</script>