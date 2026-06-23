<template>
  <section class="rounded-xl border border-dashed border-[#cfd4e5] bg-white px-6 py-16 text-center">
    <h2 class="text-xl font-extrabold text-[#001278]">비교할 카드가 없습니다.</h2>
    <p class="mt-3 text-sm text-gray-500">카드 상세 페이지에서 비교 추가 버튼을 눌러 담아주세요.</p>
    <RouterLink
      :to="{ name: 'cards' }"
      class="mt-6 inline-flex h-11 items-center justify-center rounded-lg bg-[#001278] px-5 text-sm font-bold text-white transition hover:bg-[#1428a0]"
    >
      카드 검색으로 이동
    </RouterLink>
  </section>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>
