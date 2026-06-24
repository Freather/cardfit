<template>
  <section class="skeleton-surface rounded-xl border border-[#e0e0e0] bg-white p-6 shadow-[0_4px_12px_rgba(0,0,0,0.05)]">
    <div class="flex min-h-12 items-center">
      <p class="rounded-full bg-[#eef2ff] px-4 py-3 text-sm font-bold text-[#001278]">{{ message }}</p>
    </div>
    <div class="mt-6 grid gap-5 lg:grid-cols-[1.4fr_0.8fr]">
      <SkeletonBlock custom-class="h-52 rounded-xl" />
      <SkeletonBlock custom-class="h-52 rounded-xl" />
    </div>
    <div class="mt-6 grid gap-6 lg:grid-cols-[0.82fr_1fr]">
      <div class="flex justify-center rounded-xl bg-[#fbf9f8] p-8">
        <SkeletonBlock custom-class="h-72 w-72 rounded-full" />
      </div>
      <div class="space-y-4 rounded-xl bg-[#fbf9f8] p-8">
        <SkeletonBlock custom-class="h-7 w-40" />
        <SkeletonBlock v-for="index in 5" :key="index" custom-class="h-20 rounded-xl" />
      </div>
    </div>
  </section>
</template>

<script setup>
import SkeletonBlock from '../common/SkeletonBlock.vue'

defineProps({
  message: {
    type: String,
    default: '소비 리포트를 불러오는 중입니다...',
  },
})
</script>

<style scoped>
.skeleton-surface {
  animation: surface-float 3.1s ease-in-out infinite;
}

@keyframes surface-float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-3px);
  }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton-surface {
    animation: none;
  }
}
</style>
