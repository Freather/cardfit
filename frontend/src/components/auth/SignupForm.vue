<template>
  <section class="w-full max-w-[460px] rounded-2xl border border-white/70 bg-white/90 p-8 shadow-[0_28px_70px_rgba(0,0,0,0.12)] backdrop-blur lg:p-10">
    <div class="mb-8">
      <p class="text-sm font-bold text-[#001278]">CardFit</p>
      <h1 class="mt-2 text-4xl font-extrabold text-[#1b1c1c]">회원가입</h1>
      <p class="mt-3 text-sm leading-6 text-[#454653]">
        소비 분석과 맞춤 카드 추천을 시작할 계정을 만들어주세요.
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
        <span class="text-sm font-semibold text-[#454653]">이름</span>
        <input
          :value="username"
          type="text"
          autocomplete="username"
          required
          class="w-full rounded-xl border border-[#c5c5d5] bg-white/80 px-4 py-4 text-base text-[#1b1c1c] outline-none transition placeholder:text-gray-400 focus:border-[#001278] focus:bg-white focus:ring-4 focus:ring-[#001278]/10"
          placeholder="이름을 입력하세요"
          @input="$emit('update:username', $event.target.value)"
        />
      </label>

      <label class="block space-y-2">
        <span class="text-sm font-semibold text-[#454653]">비밀번호</span>
        <input
          :value="password"
          type="password"
          autocomplete="new-password"
          required
          class="w-full rounded-xl border border-[#c5c5d5] bg-white/80 px-4 py-4 text-base text-[#1b1c1c] outline-none transition placeholder:text-gray-400 focus:border-[#001278] focus:bg-white focus:ring-4 focus:ring-[#001278]/10"
          placeholder="비밀번호"
          @input="$emit('update:password', $event.target.value)"
        />
      </label>

      <label class="block space-y-2">
        <span class="text-sm font-semibold text-[#454653]">비밀번호 확인</span>
        <input
          :value="passwordConfirm"
          type="password"
          autocomplete="new-password"
          required
          class="w-full rounded-xl border border-[#c5c5d5] bg-white/80 px-4 py-4 text-base text-[#1b1c1c] outline-none transition placeholder:text-gray-400 focus:border-[#001278] focus:bg-white focus:ring-4 focus:ring-[#001278]/10"
          placeholder="비밀번호 확인"
          @input="$emit('update:passwordConfirm', $event.target.value)"
        />
      </label>

      <div v-if="errorMessage" class="rounded-xl bg-[#ffdad6] p-4 text-sm text-[#93000a]">
        {{ errorMessage }}
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="w-full rounded-xl bg-[#001278] py-4 text-base font-bold text-white shadow-[0_14px_30px_rgba(0,18,120,0.25)] transition hover:bg-[#1428a0] active:scale-[0.99] disabled:cursor-not-allowed disabled:opacity-60"
      >
        {{ loading ? '가입 중...' : '회원가입' }}
      </button>
    </form>

    <p class="mt-6 text-center text-sm text-[#454653]">
      이미 계정이 있나요?
      <RouterLink :to="{ name: 'login' }" class="font-bold text-[#001278] hover:underline">
        로그인
      </RouterLink>
    </p>
  </section>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  email: {
    type: String,
    default: '',
  },
  username: {
    type: String,
    default: '',
  },
  password: {
    type: String,
    default: '',
  },
  passwordConfirm: {
    type: String,
    default: '',
  },
  loading: Boolean,
  errorMessage: {
    type: String,
    default: '',
  },
})

defineEmits([
  'update:email',
  'update:username',
  'update:password',
  'update:passwordConfirm',
  'submit',
])
</script>
