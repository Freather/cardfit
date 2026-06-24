<template>
  <section class="overflow-hidden rounded-lg border border-[#d4d8e8] bg-white">
    <div class="flex items-center justify-between px-6 py-6">
      <h2 class="text-xl font-extrabold">소비 데이터 관리</h2>
      <button
        type="button"
        class="inline-flex items-center gap-2 text-sm font-bold text-[#07158f] transition hover:text-[#111fa3]"
        @click="$emit('open-upload')"
      >
        <svg class="h-4 w-4" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
          <path d="M10 13V3" />
          <path d="m6.5 6.5 3.5-3.5 3.5 3.5" />
          <path d="M4 13v2.5A1.5 1.5 0 0 0 5.5 17h9a1.5 1.5 0 0 0 1.5-1.5V13" />
        </svg>
        신규 CSV 업로드
      </button>
    </div>

    <div class="overflow-x-auto">
      <table class="w-full min-w-[680px] border-collapse text-left text-sm">
        <thead>
          <tr class="border-y border-[#ececf2] bg-[#f5f2f2] text-[#30374d]">
            <th class="px-6 py-5 font-extrabold">파일명</th>
            <th class="px-6 py-5 font-extrabold">업로드 일시</th>
            <th class="px-6 py-5 font-extrabold">데이터 기간</th>
            <th class="px-6 py-5 font-extrabold">상태</th>
            <th class="px-6 py-5 text-center font-extrabold">관리</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="upload in uploads" :key="upload.id" class="border-b border-[#ececf2] last:border-b-0">
            <td class="px-6 py-6 font-medium">{{ upload.fileName }}</td>
            <td class="px-6 py-6 text-[#3b4766]">{{ upload.uploadedAt }}</td>
            <td class="px-6 py-6 text-[#3b4766]">{{ upload.period }}</td>
            <td class="px-6 py-6">
              <span
                class="inline-flex rounded-full px-3 py-1 text-xs font-extrabold"
                :class="upload.statusTone === 'done' ? 'bg-[#06429f] text-white' : 'bg-[#d9dce7] text-[#4c5368]'"
              >
                {{ upload.status }}
              </span>
            </td>
            <td class="px-6 py-6 text-center">
              <button
                type="button"
                class="inline-flex h-8 w-8 items-center justify-center rounded-md text-[#3b4766] transition hover:bg-[#f2f3f7] hover:text-red-600"
                :aria-label="`${upload.fileName} 삭제`"
                @click="$emit('remove-upload', upload.id)"
              >
                <svg class="h-4 w-4" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true">
                  <path d="M4 6h12" />
                  <path d="M8 6V4h4v2" />
                  <path d="M6 6l.7 10h6.6L14 6" />
                  <path d="M9 9v4" />
                  <path d="M11 9v4" />
                </svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="loading" class="px-6 py-10 text-center text-sm font-bold text-[#4d5870]">
        소비 데이터 목록을 불러오는 중입니다...
      </div>
      <div v-else-if="error" class="px-6 py-10 text-center text-sm font-bold text-red-600">
        {{ error }}
      </div>
      <div v-else-if="!uploads.length" class="px-6 py-10 text-center text-sm font-bold text-[#6b7280]">
        아직 소비 데이터가 없어요. CSV를 올려주세요.
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  uploads: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: '',
  },
})

defineEmits(['open-upload', 'remove-upload'])
</script>
