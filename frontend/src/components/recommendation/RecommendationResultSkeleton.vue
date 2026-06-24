<template>
  <section class="min-h-screen bg-[#fbf9f8] px-4 py-10 md:px-10 lg:px-20">
    <div class="mx-auto max-w-6xl">
      <header class="max-w-3xl">
        <div class="flex min-h-12 items-center">
          <p class="rounded-full bg-[#eef2ff] px-4 py-3 text-sm font-bold text-[#001278]">{{ message }}</p>
        </div>
        <SkeletonBlock custom-class="mt-4 h-10 w-72" />
        <SkeletonBlock custom-class="mt-4 h-4 w-full max-w-2xl" />
        <SkeletonBlock custom-class="mt-2 h-4 w-4/5 max-w-xl" />
      </header>

      <div class="mt-12 grid gap-8 lg:grid-cols-[1.35fr_0.9fr]">
        <article class="skeleton-surface rounded-xl border border-[#e5e0dd] bg-white p-8 shadow-[0_18px_52px_rgba(0,18,120,0.08)]">
          <div class="grid gap-8 md:grid-cols-[1fr_0.92fr]">
            <SkeletonBlock custom-class="h-72 rounded-lg" />
            <div class="flex flex-col justify-center">
              <SkeletonBlock custom-class="h-8 w-56 rounded-full" />
              <SkeletonBlock custom-class="mt-6 h-4 w-28" />
              <SkeletonBlock custom-class="mt-3 h-10 w-72" />
              <SkeletonBlock custom-class="mt-5 h-4 w-full" />
              <SkeletonBlock custom-class="mt-2 h-4 w-5/6" />
              <SkeletonBlock custom-class="mt-8 h-32 w-full rounded-lg" />
            </div>
          </div>

          <div class="my-8 h-px bg-[#ece7e3]"></div>
          <div class="grid gap-4 sm:grid-cols-3">
            <SkeletonBlock v-for="index in 3" :key="index" custom-class="h-36 rounded-lg" />
          </div>
        </article>

        <aside class="space-y-7">
          <section>
            <SkeletonBlock custom-class="h-7 w-40" />
            <div class="mt-5 space-y-5">
              <SkeletonBlock v-for="index in 3" :key="index" custom-class="h-24 rounded-lg" />
            </div>
          </section>
          <section class="rounded-lg border border-[#ebe5e0] bg-white p-5">
            <SkeletonBlock custom-class="h-6 w-36" />
            <div class="mt-5 space-y-4">
              <SkeletonBlock v-for="index in 3" :key="index" custom-class="h-5 w-full" />
            </div>
          </section>
        </aside>
      </div>
    </div>
  </section>
</template>

<script setup>
import SkeletonBlock from '../common/SkeletonBlock.vue'

defineProps({
  message: {
    type: String,
    default: 'AI가 소비 데이터와 설문을 분석하는 중입니다...',
  },
})
</script>

<style scoped>
.skeleton-surface {
  animation: surface-float 3.2s ease-in-out infinite;
}

@keyframes surface-float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton-surface {
    animation: none;
  }
}
</style>
