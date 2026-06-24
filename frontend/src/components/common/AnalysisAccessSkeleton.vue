<template>
  <section class="min-h-screen bg-[#fbf9f8] px-4 py-20 md:px-10 lg:px-20">
    <div class="skeleton-panel mx-auto max-w-5xl rounded-2xl border border-[#ebe6e2] bg-white p-8 shadow-[0_18px_52px_rgba(0,18,120,0.08)]">
      <div class="flex min-h-12 items-center justify-center">
        <p class="rounded-full bg-[#eef2ff] px-4 py-3 text-center text-sm font-bold text-[#001278]">{{ message }}</p>
      </div>
      <div class="mt-8 grid gap-5 md:grid-cols-[1.2fr_0.8fr]">
        <div class="space-y-4">
          <SkeletonBlock custom-class="h-9 w-72" />
          <SkeletonBlock custom-class="h-4 w-full max-w-2xl" />
          <SkeletonBlock custom-class="h-4 w-5/6 max-w-xl" />
          <div class="grid gap-3 pt-4 sm:grid-cols-2">
            <SkeletonBlock v-for="index in 4" :key="index" custom-class="h-16 rounded-lg" />
          </div>
        </div>
        <div class="space-y-3">
          <SkeletonBlock custom-class="h-24 rounded-xl" />
          <SkeletonBlock custom-class="h-24 rounded-xl" />
          <SkeletonBlock custom-class="h-24 rounded-xl" />
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import SkeletonBlock from './SkeletonBlock.vue'

defineProps({
  message: {
    type: String,
    default: '이용 가능 여부를 확인하는 중입니다...',
  },
})
</script>

<style scoped>
.skeleton-panel {
  animation: panel-rise 3s ease-in-out infinite;
}

@keyframes panel-rise {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton-panel {
    animation: none;
  }
}
</style>
