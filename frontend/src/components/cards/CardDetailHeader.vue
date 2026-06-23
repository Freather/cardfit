<template>
  <section class="border-b border-zinc-200 bg-[#fbfaf9]">
    <div class="relative mx-auto grid max-w-7xl gap-12 px-5 py-14 md:px-10 lg:grid-cols-[430px_1fr] lg:px-20">
      <RouterLink
        :to="{ name: 'cards' }"
        class="absolute right-5 top-6 text-sm font-semibold text-zinc-500 transition hover:text-blue-800 md:right-10 lg:right-20"
      >
        목록으로
      </RouterLink>

      <div class="flex justify-center lg:justify-start">
        <div class="relative flex h-[330px] w-[390px] rotate-[-6deg] items-center justify-center overflow-hidden rounded-xl bg-zinc-100 shadow-2xl shadow-zinc-300">
          <img
            v-if="card.image_url && !imageError"
            :src="card.image_url"
            :alt="card.card_name"
            class="h-full w-full object-contain p-4"
            @error="imageError = true"
          />
          <div
            v-else
            class="flex h-full w-full flex-col items-start justify-end p-8"
            style="background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 60%, #3b82f6 100%)"
          >
            <p class="text-xs font-semibold uppercase tracking-widest text-white/60">
              {{ card.card_company || 'CardFit' }}
            </p>
            <p class="mt-2 text-lg font-bold leading-tight text-white">{{ card.card_name }}</p>
          </div>
        </div>
      </div>

      <div class="flex flex-col justify-center">
        <p class="text-xs font-semibold uppercase tracking-[0.32em] text-blue-900">Premium Choice</p>
        <h1 class="mt-4 text-4xl font-extrabold tracking-tight text-black md:text-5xl">
          {{ card.card_name }}
        </h1>
        <p class="mt-4 max-w-2xl text-sm leading-6 text-zinc-500">
          사용자의 소비 패턴을 AI가 분석하여 가장 높은 혜택을 제공하는 맞춤형 프리미엄 카드입니다.
        </p>

        <div class="mt-8 grid max-w-2xl grid-cols-3 border-y border-zinc-200 py-5">
          <div>
            <p class="text-sm text-zinc-500">연회비</p>
            <p class="mt-1 font-bold text-blue-950">{{ formatWon(card.annual_fee) }}원</p>
          </div>
          <div>
            <p class="text-sm text-zinc-500">기준 실적</p>
            <p class="mt-1 font-bold text-blue-950">{{ formatPrevSpending(card.min_prev_month_spending) }}</p>
          </div>
          <div>
            <p class="text-sm text-zinc-500">카드 종류</p>
            <p class="mt-1 font-bold text-blue-950">{{ card.card_type_display || card.card_type || '-' }}</p>
          </div>
        </div>

        <div class="mt-8 flex flex-wrap items-center gap-1">
          <button
            type="button"
            :aria-pressed="isWished"
            :disabled="wishlistLoading"
            :aria-label="isWished ? '찜 해제' : '찜하기'"
            class="inline-flex h-12 w-28 items-center justify-center gap-2 rounded-md border text-sm font-bold shadow-sm transition disabled:cursor-not-allowed disabled:opacity-60"
            :class="
              isWished
                ? 'border-rose-200 bg-rose-50 text-rose-600 hover:bg-rose-100'
                : 'border-zinc-200 bg-white text-zinc-400 hover:border-rose-200 hover:text-rose-500'
            "
            @click="$emit('toggle-wishlist')"
          >
            <svg
              viewBox="0 0 24 24"
              class="h-5 w-5"
              :fill="isWished ? 'currentColor' : 'none'"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              aria-hidden="true"
            >
              <path d="M20.8 4.6c-1.6-1.5-4.1-1.5-5.7 0L12 7.7 8.9 4.6c-1.6-1.5-4.1-1.5-5.7 0-1.7 1.6-1.7 4.2 0 5.8L12 19l8.8-8.6c1.7-1.6 1.7-4.2 0-5.8Z" />
            </svg>
            {{ isWished ? '찜 해제' : '찜하기' }}
          </button>

          <div class="flex flex-wrap items-center gap-3 lg:ml-2">
            <a
              :href="card.apply_url || '#'"
              target="_blank"
              rel="noreferrer"
              class="inline-flex h-12 items-center justify-center rounded-md bg-blue-950 px-6 text-sm font-bold text-white shadow-md transition hover:bg-blue-900"
            >
              공식 발급 신청
            </a>
            <button
              type="button"
              class="h-12 px-5 text-sm font-semibold text-zinc-500 transition hover:text-blue-800"
              @click="$emit('add-compare')"
            >
              비교 추가
            </button>
          </div>
        </div>

        <div class="mt-2 min-h-5 text-sm font-bold">
          <div
            v-if="wishlistMessage"
            :class="messageToneClass(wishlistMessageTone)"
          >
            {{ wishlistMessage }}
          </div>
          <div
            v-else-if="compareMessage"
            class="flex flex-wrap items-center gap-2"
            :class="messageToneClass(compareMessageTone)"
          >
            <span>{{ compareMessage }}</span>
            <RouterLink
              v-if="compareMessageTone !== 'error'"
              :to="{ name: 'compare' }"
              class="underline underline-offset-4"
            >
              비교 페이지로 이동
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, watch } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  card: {
    type: Object,
    required: true,
  },
  isWished: {
    type: Boolean,
    default: false,
  },
  wishlistLoading: {
    type: Boolean,
    default: false,
  },
  wishlistMessage: {
    type: String,
    default: '',
  },
  wishlistMessageTone: {
    type: String,
    default: 'info',
  },
  compareMessage: {
    type: String,
    default: '',
  },
  compareMessageTone: {
    type: String,
    default: 'info',
  },
})

defineEmits(['toggle-wishlist', 'add-compare'])

const imageError = ref(false)

watch(
  () => props.card?.id,
  () => {
    imageError.value = false
  },
)

function formatWon(value) {
  return new Intl.NumberFormat('ko-KR').format(Number(value || 0))
}

function formatPrevSpending(value) {
  if (!value) return '조건 없음'
  return `${Math.floor(Number(value) / 10000)}만원 이상`
}

function messageToneClass(tone) {
  if (tone === 'error') return 'text-red-600'
  if (tone === 'success') return 'text-emerald-700'
  return 'text-blue-800'
}
</script>
