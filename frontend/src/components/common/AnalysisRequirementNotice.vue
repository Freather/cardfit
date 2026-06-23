<template>
  <section :class="sectionClass">
    <div :class="panelClass">
      <div class="flex h-14 w-14 items-center justify-center rounded-full bg-[#eef1ff] text-[#001278]">
        <svg class="h-7 w-7" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <path d="M12 9v4" />
          <path d="M12 17h.01" />
          <path d="M10.3 4.3 2.8 17.2A2 2 0 0 0 4.5 20h15a2 2 0 0 0 1.7-2.8L13.7 4.3a2 2 0 0 0-3.4 0Z" />
        </svg>
      </div>

      <p class="mt-6 text-sm font-extrabold text-[#001278]">{{ eyebrow }}</p>
      <h1 class="mt-2 text-2xl font-extrabold text-gray-950 md:text-3xl">{{ title }}</h1>
      <p class="mt-4 max-w-xl text-sm leading-6 text-gray-600">
        {{ description }}
      </p>

      <div class="mt-7 flex flex-wrap justify-center gap-2">
        <span
          v-for="item in missingRequirements"
          :key="item"
          class="rounded-full bg-[#f2f4fb] px-4 py-2 text-sm font-bold text-[#001278]"
        >
          {{ item }} 필요
        </span>
      </div>

      <div class="mt-9 flex flex-wrap justify-center gap-3">
        <RouterLink
          v-if="needsLogin"
          :to="{ name: 'login', query: { redirect: route.fullPath } }"
          class="inline-flex h-11 items-center justify-center rounded-md bg-[#001278] px-5 text-sm font-extrabold text-white transition hover:bg-[#1428a0]"
        >
          로그인하기
        </RouterLink>
        <RouterLink
          v-else
          :to="{ name: 'profile' }"
          class="inline-flex h-11 items-center justify-center rounded-md border border-[#001278] px-5 text-sm font-extrabold text-[#001278] transition hover:bg-[#eef1ff]"
        >
          마이페이지에서 완료하기
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

const props = defineProps({
  compact: {
    type: Boolean,
    default: false,
  },
  eyebrow: {
    type: String,
    default: '분석 준비가 필요합니다',
  },
  title: {
    type: String,
    default: '서비스 이용을 위한 정보가 아직 부족합니다.',
  },
  description: {
    type: String,
    default: '소비 리포트, AI 카드 추천, 카드 비교는 로그인 후 CSV 업로드와 소비 설문을 모두 완료해야 이용할 수 있습니다.',
  },
  missingRequirements: {
    type: Array,
    default: () => [],
  },
})

const route = useRoute()
const needsLogin = computed(() => props.missingRequirements.includes('로그인'))
const sectionClass = computed(() =>
  props.compact
    ? 'border-b border-zinc-200 bg-white/70 px-5 py-12 md:px-10 lg:px-20'
    : 'min-h-screen bg-[#fbf9f8] px-4 py-12 md:px-10 lg:px-20',
)
const panelClass = computed(() =>
  props.compact
    ? 'mx-auto flex max-w-7xl flex-col items-center rounded-xl border border-[#dfe3f1] bg-white px-6 py-10 text-center shadow-[0_12px_34px_rgba(0,18,120,0.08)]'
    : 'mx-auto flex max-w-3xl flex-col items-center rounded-xl border border-[#dfe3f1] bg-white px-6 py-14 text-center shadow-[0_12px_34px_rgba(0,18,120,0.08)]',
)
</script>
