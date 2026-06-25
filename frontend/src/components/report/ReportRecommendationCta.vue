<template>
  <section class="py-10 text-center">
    <h2 class="text-xl font-bold text-gray-950">내 소비에 맞는 카드를 확인해보세요.</h2>
    <p class="mt-2 text-sm text-gray-500">
      CardFit AI가 소비 패턴에 맞는 혜택을 계산했어요.
    </p>
    <RouterLink
      :to="{ name: 'ai-recommendations' }"
      class="mt-6 inline-flex h-14 min-w-56 items-center justify-center rounded-full bg-[#001278] px-8 text-base font-bold text-white shadow-lg transition hover:bg-[#1428a0]"
    >
      추천 카드 보기
    </RouterLink>
  </section>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>
