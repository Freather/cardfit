<template>
  <div class="mx-auto grid max-w-[1160px] gap-7 lg:grid-cols-[330px_1fr]">
    <aside class="grid content-start gap-5">
      <section class="skeleton-surface rounded-2xl border border-[#ebe6e2] bg-white p-6 shadow-[0_18px_52px_rgba(0,18,120,0.08)]">
        <div class="flex min-h-12 items-center">
          <p class="rounded-full bg-[#eef2ff] px-4 py-3 text-sm font-bold text-[#001278]">마이페이지 정보를 불러오는 중입니다...</p>
        </div>
        <div class="mt-6 flex items-center gap-4">
          <SkeletonBlock custom-class="h-16 w-16 rounded-full" />
          <div class="flex-1 space-y-3">
            <SkeletonBlock custom-class="h-5 w-32" />
            <SkeletonBlock custom-class="h-4 w-44" />
          </div>
        </div>
        <div class="mt-6 grid gap-3">
          <SkeletonBlock custom-class="h-11 rounded-lg" />
          <SkeletonBlock custom-class="h-11 rounded-lg" />
        </div>
      </section>

      <section class="rounded-2xl border border-[#ebe6e2] bg-white p-6 shadow-[0_18px_52px_rgba(0,18,120,0.08)]">
        <SkeletonBlock custom-class="h-6 w-28" />
        <div class="mt-5 grid gap-3">
          <SkeletonBlock v-for="index in 3" :key="index" custom-class="h-20 rounded-xl" />
        </div>
      </section>
    </aside>

    <main class="grid content-start gap-7">
      <section class="rounded-2xl border border-[#ebe6e2] bg-white p-6 shadow-[0_18px_52px_rgba(0,18,120,0.08)]">
        <SkeletonBlock custom-class="h-6 w-36" />
        <div class="mt-5 grid gap-4 md:grid-cols-3">
          <SkeletonBlock v-for="index in 3" :key="index" custom-class="h-28 rounded-xl" />
        </div>
      </section>

      <section class="rounded-2xl border border-[#ebe6e2] bg-white p-6 shadow-[0_18px_52px_rgba(0,18,120,0.08)]">
        <div class="flex items-center justify-between gap-4">
          <SkeletonBlock custom-class="h-6 w-32" />
          <SkeletonBlock custom-class="h-11 w-28 rounded-lg" />
        </div>
        <div class="mt-5 grid gap-3">
          <SkeletonBlock v-for="index in 4" :key="index" custom-class="h-14 rounded-lg" />
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import SkeletonBlock from '../common/SkeletonBlock.vue'
</script>

<style scoped>
.skeleton-surface {
  animation: surface-float 3s ease-in-out infinite;
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
