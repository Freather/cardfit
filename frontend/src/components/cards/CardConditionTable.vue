<template>
  <section class="bg-[#f7f5f3] px-5 py-16 md:px-10 lg:px-20">
    <div class="mx-auto max-w-7xl">
      <h2 class="text-3xl font-extrabold text-black">유의사항 및 세부 조건</h2>

      <div class="mt-10 overflow-hidden rounded-xl border border-zinc-200 bg-white">
        <table class="w-full border-collapse text-left text-sm">
          <thead class="bg-zinc-100 text-zinc-900">
            <tr>
              <th class="w-56 px-6 py-4 font-bold">구분</th>
              <th class="px-6 py-4 font-bold">세부 내용</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in rows" :key="row.label" class="border-t border-zinc-200">
              <th class="bg-zinc-50 px-6 py-5 font-semibold text-zinc-700">{{ row.label }}</th>
              <td class="px-6 py-5 leading-6 text-zinc-600">{{ row.value }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  rows: {
    type: Array,
    default: () => [],
  },
})
</script>
