<template>
  <section class="min-h-screen bg-[#faf9f8]">
    <div class="skeleton-surface border-b border-zinc-200 bg-[#fbfaf9]">
      <div class="mx-auto grid max-w-7xl gap-12 px-5 py-14 md:px-10 lg:grid-cols-[430px_1fr] lg:px-20">
        <SkeletonBlock custom-class="h-[330px] w-full max-w-[390px] rounded-xl shadow-sm" />
        <div class="flex flex-col justify-center">
          <div class="flex min-h-12 items-center">
            <p class="rounded-full bg-[#eef2ff] px-4 py-3 text-sm font-bold text-blue-900">카드 정보를 불러오는 중입니다...</p>
          </div>
          <SkeletonBlock custom-class="mt-5 h-12 w-3/4" />
          <SkeletonBlock custom-class="mt-5 h-4 w-full max-w-2xl" />
          <SkeletonBlock custom-class="mt-2 h-4 w-5/6 max-w-xl" />
          <div class="mt-8 grid max-w-2xl grid-cols-3 gap-4">
            <SkeletonBlock v-for="index in 3" :key="index" custom-class="h-16 rounded-lg" />
          </div>
          <div class="mt-8 flex gap-3">
            <SkeletonBlock custom-class="h-12 w-28" />
            <SkeletonBlock custom-class="h-12 w-36" />
          </div>
        </div>
      </div>
    </div>

    <div class="mx-auto max-w-7xl px-5 py-10 md:px-10 lg:px-20">
      <SkeletonBlock custom-class="h-48 rounded-xl" />
      <div class="mt-8 grid gap-5 md:grid-cols-3">
        <SkeletonBlock v-for="index in 3" :key="index" custom-class="h-44 rounded-xl" />
      </div>
    </div>
  </section>
</template>

<script setup>
import SkeletonBlock from '../common/SkeletonBlock.vue'
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
    transform: translateY(-3px);
  }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton-surface {
    animation: none;
  }
}
</style>
