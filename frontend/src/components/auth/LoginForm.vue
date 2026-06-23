<template>
  <section class="mx-auto w-full max-w-[440px] rounded-2xl border border-white/70 bg-white/85 p-8 shadow-[0_28px_70px_rgba(0,0,0,0.12)] backdrop-blur lg:p-10">
    <div class="mb-8">
      <p class="text-sm font-bold text-[#001278] lg:hidden">CardFit</p>
      <h1 class="mt-2 text-4xl font-extrabold text-[#1b1c1c]">로그인</h1>
      <p class="mt-3 text-sm leading-6 text-[#454653]">
        서비스를 이용하려면 계정으로 로그인해주세요.
      </p>
    </div>

    <form class="space-y-5" @submit.prevent="$emit('submit')">
      <label class="block space-y-2">
        <span class="text-sm font-semibold text-[#454653]">이메일</span>
        <input
          :value="email"
          type="email"
          autocomplete="email"
          required
          class="w-full rounded-xl border border-[#c5c5d5] bg-white/80 px-4 py-4 text-base text-[#1b1c1c] outline-none transition placeholder:text-gray-400 focus:border-[#001278] focus:bg-white focus:ring-4 focus:ring-[#001278]/10"
          placeholder="example@cardfit.com"
          @input="$emit('update:email', $event.target.value)"
        />
      </label>

      <label class="block space-y-2">
        <span class="text-sm font-semibold text-[#454653]">비밀번호</span>
        <input
          :value="password"
          type="password"
          autocomplete="current-password"
          required
          class="w-full rounded-xl border border-[#c5c5d5] bg-white/80 px-4 py-4 text-base text-[#1b1c1c] outline-none transition placeholder:text-gray-400 focus:border-[#001278] focus:bg-white focus:ring-4 focus:ring-[#001278]/10"
          placeholder="비밀번호"
          @input="$emit('update:password', $event.target.value)"
        />
      </label>

      <div class="flex justify-end">
        <button type="button" class="text-sm font-semibold text-[#001278] transition hover:text-[#1428a0] hover:underline">
          비밀번호 찾기
        </button>
      </div>

      <div v-if="errorMessage" class="rounded-xl bg-[#ffdad6] p-4 text-sm text-[#93000a]">
        {{ errorMessage }}
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="w-full rounded-xl bg-[#001278] py-4 text-base font-bold text-white shadow-[0_14px_30px_rgba(0,18,120,0.25)] transition hover:bg-[#1428a0] active:scale-[0.99] disabled:cursor-not-allowed disabled:opacity-60"
      >
        {{ loading ? '로그인 중...' : '로그인' }}
      </button>

      <RouterLink
        :to="{ name: 'signup' }"
        class="flex w-full justify-center rounded-xl border border-[#001278] bg-white/70 py-4 text-base font-bold text-[#001278] transition hover:bg-[#001278]/5"
      >
        회원가입
      </RouterLink>
    </form>

  </section>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  email: {
    type: String,
    default: '',
  },
  password: {
    type: String,
    default: '',
  },
  loading: Boolean,
  errorMessage: {
    type: String,
    default: '',
  },
})

defineEmits(['update:email', 'update:password', 'submit'])
</script>
