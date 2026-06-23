<template>
  <div
    v-if="open"
    class="fixed inset-0 z-[100] flex items-center justify-center bg-black/45 px-4 py-6"
    role="dialog"
    aria-modal="true"
    aria-labelledby="profile-edit-title"
    @click.self="$emit('close')"
  >
    <section class="w-full max-w-[480px] rounded-lg bg-white shadow-2xl">
      <div class="flex items-start justify-between gap-4 border-b border-[#ececf2] px-6 py-5">
        <div>
          <h2 id="profile-edit-title" class="text-xl font-extrabold">회원정보 수정</h2>
          <p class="mt-1 text-sm text-[#4d5870]">마이페이지에 표시되는 기본 정보를 수정합니다.</p>
        </div>
        <button
          type="button"
          class="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-md text-[#4d5870] transition hover:bg-[#f2f3f7]"
          aria-label="모달 닫기"
          :disabled="saving"
          @click="$emit('close')"
        >
          <svg class="h-5 w-5" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true">
            <path d="m5 5 10 10" />
            <path d="m15 5-10 10" />
          </svg>
        </button>
      </div>

      <form class="px-6 py-6" @submit.prevent="$emit('save')">
        <div class="grid gap-5">
          <label class="grid gap-2">
            <span class="text-sm font-extrabold text-[#30374d]">이름</span>
            <input
              :value="form.username"
              type="text"
              class="h-12 rounded-md border border-[#d4d8e8] px-4 text-sm font-semibold text-[#121212] outline-none transition focus:border-[#07158f] focus:ring-2 focus:ring-[#07158f]/10"
              placeholder="이름을 입력하세요"
              autocomplete="name"
              @input="updateField('username', $event.target.value)"
            />
          </label>

          <label class="grid gap-2">
            <span class="text-sm font-extrabold text-[#30374d]">이메일</span>
            <input
              :value="form.email"
              type="email"
              class="h-12 cursor-not-allowed rounded-md border border-[#d4d8e8] bg-[#f5f2f2] px-4 text-sm font-semibold text-[#6b7280] outline-none"
              readonly
            />
          </label>
        </div>

        <p v-if="error" class="mt-4 rounded-md bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">
          {{ error }}
        </p>

        <div class="mt-7 flex justify-end gap-3 border-t border-[#ececf2] pt-5">
          <button
            type="button"
            class="inline-flex h-11 items-center justify-center rounded-md border border-[#d4d8e8] bg-white px-5 text-sm font-bold text-[#4d5870] transition hover:bg-[#f7f7fa]"
            :disabled="saving"
            @click="$emit('close')"
          >
            취소
          </button>
          <button
            type="submit"
            class="inline-flex h-11 min-w-[120px] items-center justify-center rounded-md bg-[#07158f] px-5 text-sm font-extrabold text-white transition hover:bg-[#111fa3] disabled:cursor-not-allowed disabled:bg-[#8b93c8]"
            :disabled="saving"
          >
            {{ saving ? '저장 중' : '저장' }}
          </button>
        </div>
      </form>
    </section>
  </div>
</template>

<script setup>
const props = defineProps({
  open: Boolean,
  form: {
    type: Object,
    required: true,
  },
  saving: Boolean,
  error: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['close', 'save', 'update:form'])

function updateField(field, value) {
  emit('update:form', {
    ...props.form,
    [field]: value,
  })
}
</script>
