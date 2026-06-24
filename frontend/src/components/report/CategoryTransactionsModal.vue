<template>
  <div
    v-if="open"
    class="fixed inset-0 z-[100] flex items-center justify-center bg-black/45 px-4 py-6"
    role="dialog"
    aria-modal="true"
    aria-labelledby="category-transactions-title"
    @click.self="$emit('close')"
  >
    <section class="flex max-h-[86vh] w-full max-w-[760px] flex-col overflow-hidden rounded-xl bg-white shadow-2xl">
      <div class="flex items-start justify-between gap-4 border-b border-[#ececf2] px-6 py-5">
        <div>
          <p class="text-sm font-extrabold text-[#001278]">카테고리 소비 내역</p>
          <h2 id="category-transactions-title" class="mt-1 text-2xl font-extrabold text-gray-950">
            {{ category?.label || '카테고리' }}
          </h2>
          <p class="mt-2 text-sm text-gray-500">
            {{ periodLabel }} 동안 확인된 결제 내역입니다.
          </p>
        </div>
        <button
          type="button"
          class="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-md text-[#4d5870] transition hover:bg-[#f2f3f7]"
          aria-label="모달 닫기"
          @click="$emit('close')"
        >
          <svg class="h-5 w-5" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true">
            <path d="m5 5 10 10" />
            <path d="m15 5-10 10" />
          </svg>
        </button>
      </div>

      <div class="grid gap-3 border-b border-[#ececf2] bg-[#fbf9f8] px-6 py-4 sm:grid-cols-3">
        <div class="rounded-lg bg-white px-4 py-3">
          <p class="text-xs font-bold text-gray-500">월평균 지출</p>
          <p class="mt-1 text-lg font-extrabold text-gray-950">{{ formatCurrency(category?.total) }}</p>
        </div>
        <div class="rounded-lg bg-white px-4 py-3">
          <p class="text-xs font-bold text-gray-500">지출 비중</p>
          <p class="mt-1 text-lg font-extrabold text-gray-950">{{ formatRatio(category?.ratio) }}%</p>
        </div>
        <div class="rounded-lg bg-white px-4 py-3">
          <p class="text-xs font-bold text-gray-500">결제 건수</p>
          <p class="mt-1 text-lg font-extrabold text-gray-950">{{ transactions.length.toLocaleString('ko-KR') }}건</p>
        </div>
      </div>

      <div class="min-h-0 flex-1 overflow-y-auto px-6 py-5">
        <div v-if="loading" class="space-y-3">
          <div v-for="index in 5" :key="index" class="h-16 animate-pulse rounded-lg bg-[#f2eeee]"></div>
        </div>

        <p v-else-if="error" class="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm font-bold text-red-700">
          {{ error }}
        </p>

        <div
          v-else-if="!transactions.length"
          class="rounded-lg border border-dashed border-[#d8dbe8] bg-[#fbf9f8] px-5 py-10 text-center"
        >
          <p class="text-sm font-extrabold text-gray-700">보여줄 소비 내역이 없어요.</p>
          <p class="mt-2 text-sm text-gray-500">CSV에 이 카테고리 결제가 없을 수 있어요.</p>
        </div>

        <div v-else class="space-y-3">
          <article
            v-for="transaction in transactions"
            :key="transaction.id"
            class="flex items-center justify-between gap-4 rounded-lg border border-[#ececf2] bg-white px-4 py-4"
          >
            <div class="min-w-0">
              <p class="truncate text-sm font-extrabold text-gray-950">{{ transaction.merchant || '가맹점 정보 없음' }}</p>
              <p class="mt-1 text-xs font-semibold text-gray-500">{{ formatDate(transaction.transaction_date) }}</p>
            </div>
            <p class="shrink-0 text-base font-extrabold text-[#001278]">
              {{ formatCurrency(transaction.amount) }}
            </p>
          </article>
        </div>
      </div>

      <div class="flex justify-end border-t border-[#ececf2] px-6 py-5">
        <button
          type="button"
          class="inline-flex h-11 items-center justify-center rounded-md bg-[#001278] px-5 text-sm font-extrabold text-white transition hover:bg-[#1428a0]"
          @click="$emit('close')"
        >
          닫기
        </button>
      </div>
    </section>
  </div>
</template>

<script setup>
defineProps({
  open: Boolean,
  category: {
    type: Object,
    default: null,
  },
  transactions: {
    type: Array,
    default: () => [],
  },
  loading: Boolean,
  error: {
    type: String,
    default: '',
  },
  periodLabel: {
    type: String,
    default: '소비 데이터 기준',
  },
})

defineEmits(['close'])

function formatCurrency(value) {
  return new Intl.NumberFormat('ko-KR', {
    style: 'currency',
    currency: 'KRW',
    maximumFractionDigits: 0,
  }).format(value || 0)
}

function formatRatio(value) {
  return Number(value || 0).toLocaleString('ko-KR', {
    maximumFractionDigits: 1,
  })
}

function formatDate(value) {
  if (!value) return '-'

  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(new Date(value))
}
</script>
