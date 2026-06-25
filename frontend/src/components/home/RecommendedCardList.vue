<template>
  <section>
    <div class="mb-6 flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
      <div>
        <h2 class="text-xl font-extrabold text-gray-950">카드 추천 라인업</h2>
        <p class="mt-1 text-sm text-gray-500">다양한 혜택의 카드를 먼저 둘러보세요.</p>
      </div>
      <RouterLink
        :to="{ name: 'cards' }"
        class="text-sm font-bold text-[#001278] underline-offset-4 hover:underline"
      >
        전체 카드 보기
      </RouterLink>
    </div>

    <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
      <article
        v-for="card in cards"
        :key="card.id"
        class="flex min-h-[360px] flex-col justify-between rounded-2xl border border-gray-200 bg-white p-6 shadow-sm"
      >
        <div>
          <div class="relative mb-5 flex h-40 w-full items-center justify-center overflow-hidden rounded-xl bg-gray-100">
            <img
              v-if="card.image_url"
              :src="card.image_url"
              :alt="card.name"
              class="h-full w-full object-contain p-2"
            />
            <span v-else class="text-xs text-gray-400">카드 이미지</span>
          </div>

          <h3 class="text-lg font-extrabold text-gray-950">{{ card.name }}</h3>
          <p class="mt-2 line-clamp-3 min-h-[60px] text-sm leading-5 text-gray-500">{{ card.desc }}</p>
          <p v-if="card.benefit" class="mt-4 text-sm font-extrabold text-[#001278]">
            {{ card.benefit }}
          </p>
        </div>

        <RouterLink
          :to="{ name: 'card-detail', params: { id: card.id } }"
          class="mt-6 inline-flex h-11 w-full items-center justify-center rounded-xl border border-[#001278] text-sm font-bold text-[#001278] transition hover:bg-[#eef1ff]"
        >
          자세히 보기
        </RouterLink>
      </article>
    </div>
  </section>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  cards: {
    type: Array,
    default: () => [],
  },
})
</script>
