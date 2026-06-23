<template>
  <section class="rounded-lg border border-[#d4d8e8] bg-white px-8 py-10">
    <div class="flex min-h-[210px] flex-col items-center justify-center text-center">
      <h1 class="text-xl font-extrabold">{{ name }}</h1>
      <p class="mt-2 text-sm text-[#3b4766]">{{ email }}</p>

      <button
        type="button"
        class="mt-11 inline-flex items-center gap-2 text-sm font-bold text-[#06198f]"
        @click="$emit('edit')"
      >
        <svg class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path d="M14.7 2.3a1 1 0 0 1 1.4 0l1.6 1.6a1 1 0 0 1 0 1.4L7.3 15.7 3 17l1.3-4.3L14.7 2.3Z" />
        </svg>
        회원정보 수정
      </button>
    </div>

    <div class="mt-5 flex items-center justify-between border-t border-[#ececf2] pt-8">
      <button type="button" class="text-sm text-[#4d5870]" @click="$emit('logout')">로그아웃</button>
      <button
        type="button"
        class="inline-flex h-8 w-8 items-center justify-center rounded-md text-[#111827] transition hover:bg-[#f2f3f7]"
        aria-label="로그아웃"
        @click="$emit('logout')"
      >
        <svg class="h-4 w-4" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
          <path d="M7.5 16.5H4.8A1.8 1.8 0 0 1 3 14.7V5.3a1.8 1.8 0 0 1 1.8-1.8h2.7" />
          <path d="M12 6.5 15.5 10 12 13.5" />
          <path d="M15.5 10H7.2" />
        </svg>
      </button>
    </div>
  </section>
</template>

<script setup>
defineProps({
  name: {
    type: String,
    required: true,
  },
  email: {
    type: String,
    required: true,
  },
})

defineEmits(['edit', 'logout'])
</script>
