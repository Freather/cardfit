<template>
  <section class="border-b border-zinc-200 bg-white/70 px-5 py-12 md:px-10 lg:px-20">
    <div class="mx-auto max-w-7xl rounded-xl border border-blue-100 bg-white p-8 shadow-sm">
      <div class="flex gap-6">
        <div class="flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-indigo-100 text-2xl text-blue-900">
          ✨
        </div>
        <div>
          <h2 class="text-lg font-bold text-blue-950">AI 맞춤 추천 사유</h2>
          <p class="mt-2 text-sm leading-6 text-zinc-600">
            최근 3개월 소비 데이터를 분석한 결과,
            <strong class="font-bold text-blue-950">{{ keywords.join(', ') }}</strong>
            영역의 지출 비중이 높게 나타났습니다. 이 카드는 해당 카테고리에서 혜택을 제공해 현재 사용 중인 카드 대비
            <strong class="font-bold text-blue-950">월 평균 15,400원의 추가 혜택</strong>
            을 받을 수 있습니다.
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  keywords: {
    type: Array,
    default: () => [],
  },
})
</script>
