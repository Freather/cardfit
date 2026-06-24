<template>
  <div
    class="skeleton-block rounded-md"
    :class="customClass"
    :style="{ height, width }"
    aria-hidden="true"
  ></div>
</template>

<script setup>
defineProps({
  customClass: {
    type: String,
    default: '',
  },
  height: {
    type: String,
    default: undefined,
  },
  width: {
    type: String,
    default: undefined,
  },
})
</script>

<style scoped>
.skeleton-block {
  position: relative;
  overflow: hidden;
  background: linear-gradient(100deg, #f2f4f8 0%, #e6ebf4 45%, #f7f9fc 55%, #eef2f8 100%);
  background-size: 220% 100%;
  animation:
    skeleton-wave 1.65s ease-in-out infinite,
    skeleton-breathe 2.8s ease-in-out infinite;
}

.skeleton-block::after {
  content: '';
  position: absolute;
  inset: 0;
  transform: translateX(-120%);
  background: linear-gradient(100deg, transparent 20%, rgba(255, 255, 255, 0.72) 50%, transparent 80%);
  animation: skeleton-glint 1.9s ease-in-out infinite;
}

@keyframes skeleton-wave {
  0% {
    background-position: 120% 0;
  }
  100% {
    background-position: -120% 0;
  }
}

@keyframes skeleton-glint {
  0% {
    transform: translateX(-120%);
  }
  55%,
  100% {
    transform: translateX(120%);
  }
}

@keyframes skeleton-breathe {
  0%,
  100% {
    opacity: 0.78;
  }
  50% {
    opacity: 1;
  }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton-block,
  .skeleton-block::after {
    animation: none;
  }
}
</style>
