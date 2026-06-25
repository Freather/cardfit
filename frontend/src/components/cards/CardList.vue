<template>
  <div>
    <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <p class="text-sm font-bold text-zinc-900">총 {{ cards.length }}개 카드</p>
      <label class="flex items-center gap-2 self-start text-sm text-zinc-500 sm:self-auto">
        정렬:
        <select
          :value="sortOption"
          class="rounded-md bg-transparent text-zinc-700 outline-none"
          @change="$emit('update:sortOption', $event.target.value)"
        >
          <option value="popular">인기순</option>
          <option value="benefit">혜택순</option>
          <option value="fee">연회비 낮은순</option>
        </select>
      </label>
    </div>

    <div class="mt-4 grid gap-6 md:grid-cols-2">
      <CardItem
        v-for="card in cards"
        :key="card.id"
        :card="card"
        :failed="failedImageIds.has(card.id)"
        @image-error="$emit('image-error', $event)"
      />
    </div>

    <div
      v-if="cards.length === 0"
      class="mt-4 rounded-xl bg-white p-10 text-center text-sm text-zinc-500 shadow-md shadow-zinc-200/80"
    >
      조건에 맞는 카드가 없어요.
    </div>
  </div>
</template>

<script setup>
import CardItem from './CardItem.vue'

defineProps({
  cards: {
    type: Array,
    default: () => [],
  },
  sortOption: {
    type: String,
    default: 'popular',
  },
  failedImageIds: {
    type: Object,
    default: () => new Set(),
  },
})

defineEmits(['update:sortOption', 'image-error'])
</script>
