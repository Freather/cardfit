<template>
  <section
    class="rounded-2xl p-8 shadow-sm"
    :class="statusTone.wrapper"
  >
    <div class="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
      <div>
        <p class="text-sm font-extrabold" :class="statusTone.eyebrow">{{ statusEyebrow }}</p>
        <h1 class="mt-2 text-2xl font-extrabold">{{ statusTitle }}</h1>
        <p class="mt-2 max-w-2xl text-sm leading-6" :class="statusTone.description">
          {{ statusDescription }}
        </p>

        <div v-if="missingRequirements.length" class="mt-4 flex flex-wrap gap-2">
          <span
            v-for="item in missingRequirements"
            :key="item"
            class="rounded-full bg-white/15 px-3 py-1 text-xs font-bold"
          >
            {{ item }} 필요
          </span>
        </div>
      </div>

      <RouterLink
        :to="actionTo"
        class="inline-flex h-11 shrink-0 items-center justify-center rounded-lg px-5 text-sm font-extrabold shadow-sm transition"
        :class="statusTone.button"
      >
        {{ actionLabel }}
      </RouterLink>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  isLoggedIn: {
    type: Boolean,
    default: false,
  },
  hasSurvey: {
    type: Boolean,
    default: false,
  },
  hasCsv: {
    type: Boolean,
    default: false,
  },
  username: {
    type: String,
    default: '사용자',
  },
})

const missingRequirements = computed(() => {
  const items = []
  if (!props.isLoggedIn) items.push('로그인')
  if (!props.hasSurvey) items.push('소비 설문')
  if (!props.hasCsv) items.push('CSV 업로드')
  return items
})

const isReady = computed(() => props.isLoggedIn && props.hasSurvey && props.hasCsv)

const statusEyebrow = computed(() => {
  if (isReady.value) return '분석 준비 끝'
  if (!props.isLoggedIn) return '로그인해주세요'
  return '조금만 더 준비해주세요'
})

const statusTitle = computed(() => {
  if (isReady.value) return `${props.username}님의 맞춤 추천을 준비했어요`
  if (!props.isLoggedIn) return '내 소비 패턴에 맞는 카드를 찾아보세요'
  return 'CSV와 소비 설문을 준비해주세요'
})

const statusDescription = computed(() => {
  if (isReady.value) {
    return '업로드한 소비 데이터와 설문 정보를 바탕으로 혜택이 큰 카드를 추천합니다.'
  }
  if (!props.isLoggedIn) {
    return '로그인하면 설문부터 AI 추천까지 이어서 볼 수 있어요.'
  }
  return 'CSV와 소비 설문을 준비하면 리포트와 AI 추천을 볼 수 있어요.'
})

const actionLabel = computed(() => {
  if (isReady.value) return '소비 리포트 보기'
  if (!props.isLoggedIn) return '로그인하기'
  return '마이페이지에서 완료하기'
})

const actionTo = computed(() => {
  if (isReady.value) return { name: 'report' }
  if (!props.isLoggedIn) return { name: 'login' }
  return { name: 'profile' }
})

const statusTone = computed(() => {
  if (isReady.value) {
    return {
      wrapper: 'bg-[#001278] text-white',
      eyebrow: 'text-blue-100',
      description: 'text-blue-100',
      button: 'bg-white text-[#001278] hover:bg-blue-50',
    }
  }

  if (!props.isLoggedIn) {
    return {
      wrapper: 'bg-gray-900 text-white',
      eyebrow: 'text-gray-300',
      description: 'text-gray-300',
      button: 'bg-white text-gray-950 hover:bg-gray-100',
    }
  }

  return {
    wrapper: 'bg-amber-900 text-white',
    eyebrow: 'text-amber-100',
    description: 'text-amber-100',
    button: 'bg-white text-amber-950 hover:bg-amber-50',
  }
})
</script>
