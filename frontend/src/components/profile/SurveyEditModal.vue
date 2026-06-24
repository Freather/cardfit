<template>
  <div
    v-if="open"
    class="fixed inset-0 z-[100] flex items-center justify-center bg-black/45 px-4 py-6"
    role="dialog"
    aria-modal="true"
    aria-labelledby="survey-edit-title"
    @click.self="$emit('close')"
  >
    <section class="max-h-[92vh] w-full max-w-[680px] overflow-y-auto rounded-lg bg-white shadow-2xl">
      <div class="flex items-start justify-between gap-4 border-b border-[#ececf2] px-6 py-5">
        <div>
          <h2 id="survey-edit-title" class="text-xl font-extrabold">소비 설문 입력</h2>
          <p class="mt-1 text-sm text-[#4d5870]">
            CSV는 실제 소비 내역, 설문은 선호 카테고리와 원하는 혜택을 구분해서 반영합니다.
          </p>
        </div>
        <button
          type="button"
          class="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-md text-[#4d5870] transition hover:bg-[#f2f3f7]"
          aria-label="모달 닫기"
          @click="$emit('close')"
        >
          <svg class="h-5 w-5" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true">
            <path d="m5 5 10 10" />
            <path d="m15 5-10 10" />
          </svg>
        </button>
      </div>

      <div class="grid gap-8 px-6 py-6">
        <section>
          <h3 class="text-base font-extrabold">1. 선호 소비 카테고리</h3>
          <p class="mt-1 text-sm text-[#6b7280]">내가 혜택을 받고 싶은 영역을 선택해주세요. 여러 개 선택할 수 있습니다.</p>
          <div class="mt-4 grid gap-3 sm:grid-cols-2">
            <button
              v-for="option in categoryOptions"
              :key="option.value"
              type="button"
              class="flex h-12 items-center justify-between rounded-md border px-4 text-sm font-bold transition"
              :class="
                form.categories.includes(option.value)
                  ? 'border-[#07158f] bg-[#eef1ff] text-[#07158f]'
                  : 'border-[#d4d8e8] bg-white text-[#30374d] hover:border-[#07158f]'
              "
              @click="toggleCategory(option.value)"
            >
              {{ option.label }}
              <span
                class="flex h-5 w-5 items-center justify-center rounded-full border text-[11px]"
                :class="
                  form.categories.includes(option.value)
                    ? 'border-[#07158f] bg-[#07158f] text-white'
                    : 'border-[#c7cce0] text-transparent'
                "
              >
                ✓
              </span>
            </button>
          </div>
        </section>

        <section>
          <h3 class="text-base font-extrabold">2. 원하는 사용 금액</h3>
          <p class="mt-1 text-sm text-[#6b7280]">
            실제 소비 내역은 CSV로 분석하고, 이 금액은 카드 추천 조건과 선호 범위를 잡는 데 사용합니다.
          </p>
          <div class="mt-4 rounded-lg border border-[#d4d8e8] bg-[#f8f8fb] p-5">
            <input
              :value="form.monthlyAmount"
              type="range"
              min="100000"
              max="5000000"
              step="10000"
              class="w-full accent-[#07158f]"
              @input="updateField('monthlyAmount', Number($event.target.value))"
            />
            <div class="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <p class="text-sm font-bold text-[#4d5870]">10만원 - 500만원</p>
              <label class="flex items-center gap-2">
                <input
                  :value="form.monthlyAmount"
                  inputmode="numeric"
                  pattern="[0-9]*"
                  class="h-11 w-40 rounded-md border border-[#d4d8e8] bg-white px-3 text-right text-sm font-extrabold text-[#07158f] outline-none focus:border-[#07158f] focus:ring-2 focus:ring-[#07158f]/10"
                  @input="handleMonthlyInput"
                />
                <span class="text-sm font-bold text-[#30374d]">원</span>
              </label>
            </div>
            <p class="mt-3 text-right text-xl font-extrabold text-[#07158f]">
              {{ formatCompactWon(form.monthlyAmount) }}
            </p>
          </div>
        </section>

        <section>
          <h3 class="text-base font-extrabold">3. 선호 혜택</h3>
          <div class="mt-4 grid gap-3 sm:grid-cols-2">
            <label
              v-for="benefit in benefitOptions"
              :key="benefit"
              class="flex h-12 cursor-pointer items-center gap-3 rounded-md border px-4 text-sm font-bold transition"
              :class="
                form.preferredBenefit === benefit
                  ? 'border-[#07158f] bg-[#eef1ff] text-[#07158f]'
                  : 'border-[#d4d8e8] bg-white text-[#30374d] hover:border-[#07158f]'
              "
            >
              <input
                :checked="form.preferredBenefit === benefit"
                type="radio"
                name="preferred-benefit"
                :value="benefit"
                class="h-4 w-4 accent-[#07158f]"
                @change="updateField('preferredBenefit', benefit)"
              />
              {{ benefit }}
            </label>
          </div>
        </section>

        <p v-if="error" class="rounded-md bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">
          {{ error }}
        </p>
      </div>

      <div class="flex justify-end gap-3 border-t border-[#ececf2] px-6 py-5">
        <button
          type="button"
          class="inline-flex h-11 items-center justify-center rounded-md border border-[#d4d8e8] bg-white px-5 text-sm font-bold text-[#4d5870] transition hover:bg-[#f7f7fa]"
          @click="$emit('close')"
        >
          취소
        </button>
        <button
          type="button"
          class="inline-flex h-11 min-w-[120px] items-center justify-center rounded-md bg-[#07158f] px-5 text-sm font-extrabold text-white transition hover:bg-[#111fa3]"
          @click="$emit('save')"
        >
          저장
        </button>
      </div>
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
  categoryOptions: {
    type: Array,
    default: () => [],
  },
  benefitOptions: {
    type: Array,
    default: () => [],
  },
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

function toggleCategory(category) {
  const categories = props.form.categories.includes(category)
    ? props.form.categories.filter((item) => item !== category)
    : [...props.form.categories, category]

  updateField('categories', categories)
}

function handleMonthlyInput(event) {
  const numericValue = event.target.value.replace(/\D/g, '')
  updateField('monthlyAmount', numericValue ? Number(numericValue) : 0)
}

function formatCompactWon(value) {
  const amount = Number(value || 0)
  if (amount >= 10000) return `${Math.round(amount / 10000)}만원`
  return `${amount.toLocaleString('ko-KR')}원`
}
</script>
