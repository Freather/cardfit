<template>
  <aside class="h-fit rounded-xl bg-white p-6 shadow-md shadow-zinc-200/80">
    <h2 class="text-base font-bold text-zinc-900">필터</h2>

    <div class="mt-6">
      <h3 class="text-sm font-bold text-zinc-800">혜택 유형</h3>
      <div class="mt-3 flex flex-wrap gap-2 lg:flex-col">
        <button
          v-for="filter in benefitFilters"
          :key="filter.label"
          type="button"
          class="w-fit rounded-full border px-4 py-1.5 text-sm transition"
          :class="
            filters.selectedBenefits.includes(filter.value)
              ? 'border-blue-600 bg-blue-50 text-blue-700'
              : 'border-zinc-200 bg-white text-zinc-600 hover:border-blue-300'
          "
          @click="toggleBenefit(filter.value)"
        >
          {{ filter.label }}
        </button>
      </div>
    </div>

    <div class="mt-7">
      <h3 class="text-sm font-bold text-zinc-800">연회비</h3>
      <label
        v-for="filter in annualFeeFilters"
        :key="filter.value"
        class="mt-3 flex items-center gap-2 text-sm text-zinc-600"
      >
        <input
          :checked="filters.selectedAnnualFee === filter.value"
          type="radio"
          name="annual-fee"
          :value="filter.value"
          class="h-4 w-4 accent-blue-600"
          @change="updateFilter('selectedAnnualFee', filter.value)"
        />
        {{ filter.label }}
      </label>
    </div>

    <div class="mt-7">
      <h3 class="text-sm font-bold text-zinc-800">카드사</h3>
      <label
        v-for="filter in companyFilters"
        :key="filter.value"
        class="mt-3 flex items-center gap-2 text-sm"
        :class="filter.value === filters.selectedCompany ? 'text-zinc-800' : 'text-zinc-600'"
      >
        <input
          :checked="filters.selectedCompany === filter.value"
          type="radio"
          name="company"
          :value="filter.value"
          class="h-4 w-4 accent-blue-600"
          @change="updateFilter('selectedCompany', filter.value)"
        />
        {{ filter.label }}
      </label>
    </div>

    <div class="mt-7">
      <h3 class="text-sm font-bold text-zinc-800">전월 실적</h3>
      <label
        v-for="filter in prevSpendingFilters"
        :key="filter.value"
        class="mt-3 flex items-center gap-2 text-sm text-zinc-600"
      >
        <input
          :checked="filters.selectedPrevSpending === filter.value"
          type="radio"
          name="prev-spending"
          :value="filter.value"
          class="h-4 w-4 accent-blue-600"
          @change="updateFilter('selectedPrevSpending', filter.value)"
        />
        {{ filter.label }}
      </label>
    </div>

    <button
      type="button"
      class="mt-6 h-11 w-full rounded-lg bg-blue-600 text-sm font-bold text-white transition hover:bg-blue-700"
      @click="$emit('reset')"
    >
      필터 초기화
    </button>
  </aside>
</template>

<script setup>
const props = defineProps({
  filters: {
    type: Object,
    required: true,
  },
  benefitFilters: {
    type: Array,
    default: () => [],
  },
  annualFeeFilters: {
    type: Array,
    default: () => [],
  },
  companyFilters: {
    type: Array,
    default: () => [],
  },
  prevSpendingFilters: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['update:filters', 'reset'])

function updateFilter(key, value) {
  emit('update:filters', {
    ...props.filters,
    [key]: value,
  })
}

function toggleBenefit(value) {
  const selectedBenefits = props.filters.selectedBenefits.includes(value)
    ? props.filters.selectedBenefits.filter((benefit) => benefit !== value)
    : [...props.filters.selectedBenefits, value]

  updateFilter('selectedBenefits', selectedBenefits)
}
</script>
