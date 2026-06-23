<template>
  <section class="rounded-lg border border-[#d4d8e8] bg-white px-6 py-6">
    <div class="flex items-start justify-between gap-4">
      <div>
        <h2 class="text-lg font-extrabold">최근 소비 설문 요약</h2>
        <p class="mt-1 text-sm text-[#3b4766]">마지막 참여: {{ updatedAt }}</p>
      </div>
      <RouterLink
        :to="{ name: 'report' }"
        class="inline-flex h-11 w-11 items-center justify-center rounded-md bg-[#f5f2f3] text-[#07158f] transition hover:bg-[#eceafa]"
        aria-label="소비 리포트 보기"
      >
        <svg class="h-5 w-5" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
          <path d="M4 17V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v13" />
          <path d="M7 13V9" />
          <path d="M10 13V6" />
          <path d="M13 13v-3" />
          <path d="M3 17h14" />
        </svg>
      </RouterLink>
    </div>

    <div class="mt-6 grid gap-5 md:grid-cols-3">
      <div class="rounded-md bg-[#f5f2f2] px-6 py-6">
        <p class="text-sm text-[#3b4766]">메인 소비 카테고리</p>
        <p class="mt-2 text-base font-extrabold text-[#07158f]">{{ mainCategory }}</p>
      </div>
      <div class="rounded-md bg-[#f5f2f2] px-6 py-6">
        <p class="text-sm text-[#3b4766]">평균 월 지출액</p>
        <p class="mt-2 text-base font-extrabold text-[#07158f]">{{ monthlyTotalLabel }}</p>
      </div>
      <div class="rounded-md bg-[#f5f2f2] px-6 py-6">
        <p class="text-sm text-[#3b4766]">선호 혜택</p>
        <p class="mt-2 text-base font-extrabold text-[#07158f]">{{ preferredBenefit }}</p>
      </div>
    </div>

    <button
      type="button"
      class="mt-7 inline-flex h-[72px] w-full items-center justify-center gap-3 rounded-lg bg-[#07158f] text-base font-extrabold text-white shadow-[0_8px_16px_rgba(7,21,143,0.2)] transition hover:bg-[#111fa3]"
      @click="$emit('open-survey')"
    >
      <svg class="h-5 w-5" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
        <path d="M10 3v3" />
        <path d="M10 14v3" />
        <path d="M17 10h-3" />
        <path d="M6 10H3" />
        <path d="m14.95 5.05-2.12 2.12" />
        <path d="m7.17 12.83-2.12 2.12" />
        <path d="m14.95 14.95-2.12-2.12" />
        <path d="m7.17 7.17-2.12-2.12" />
      </svg>
      소비 설문 재입력
    </button>
  </section>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  updatedAt: {
    type: String,
    required: true,
  },
  mainCategory: {
    type: String,
    required: true,
  },
  monthlyTotalLabel: {
    type: String,
    required: true,
  },
  preferredBenefit: {
    type: String,
    required: true,
  },
})

defineEmits(['open-survey'])
</script>
