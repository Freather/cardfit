<template>
  <div
    v-if="open"
    class="fixed inset-0 z-[100] flex items-center justify-center bg-black/45 px-4 py-6"
    role="dialog"
    aria-modal="true"
    aria-labelledby="csv-upload-title"
    @click.self="$emit('close')"
    @dragenter.prevent
    @dragover.prevent
    @drop.prevent
  >
    <section class="w-full max-w-[520px] rounded-lg bg-white shadow-2xl">
      <div class="flex items-start justify-between gap-4 border-b border-[#ececf2] px-6 py-5">
        <div>
          <h2 id="csv-upload-title" class="text-xl font-extrabold">CSV 파일 업로드</h2>
          <p class="mt-1 text-sm text-[#4d5870]">카드 소비 내역 CSV를 업로드하면 소비 데이터에 반영합니다.</p>
        </div>
        <button
          type="button"
          class="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-md text-[#4d5870] transition hover:bg-[#f2f3f7]"
          aria-label="모달 닫기"
          :disabled="uploading"
          @click="$emit('close')"
        >
          <svg class="h-5 w-5" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true">
            <path d="m5 5 10 10" />
            <path d="m15 5-10 10" />
          </svg>
        </button>
      </div>

      <div class="px-6 py-6">
        <label
          class="flex min-h-[190px] cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-[#cbd2e7] bg-[#f8f8fb] px-6 py-8 text-center transition hover:border-[#07158f] hover:bg-[#f3f5ff]"
          @dragover.prevent
          @drop.prevent.stop="$emit('file-drop', $event)"
        >
          <input type="file" accept=".csv,text/csv" class="sr-only" @change="$emit('file-change', $event)" />
          <span class="flex h-14 w-14 items-center justify-center rounded-full bg-[#07158f] text-white">
            <svg class="h-6 w-6" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
              <path d="M10 13V3" />
              <path d="m6.5 6.5 3.5-3.5 3.5 3.5" />
              <path d="M4 13v2.5A1.5 1.5 0 0 0 5.5 17h9a1.5 1.5 0 0 0 1.5-1.5V13" />
            </svg>
          </span>
          <span class="mt-4 text-base font-extrabold text-[#121212]">
            {{ file ? file.name : 'CSV 파일을 선택하거나 끌어다 놓기' }}
          </span>
          <span class="mt-2 text-sm text-[#6b7280]">.csv 형식만 지원합니다.</span>
        </label>

        <div
          v-if="file"
          class="mt-4 flex items-center justify-between gap-3 rounded-md border border-[#ececf2] bg-white px-4 py-3"
        >
          <div class="min-w-0">
            <p class="truncate text-sm font-bold text-[#121212]">{{ file.name }}</p>
            <p class="mt-0.5 text-xs text-[#6b7280]">{{ Math.ceil(file.size / 1024).toLocaleString('ko-KR') }} KB</p>
          </div>
          <button
            type="button"
            class="text-sm font-bold text-[#07158f] hover:text-[#111fa3]"
            :disabled="uploading"
            @click="$emit('clear-file')"
          >
            제거
          </button>
        </div>

        <p v-if="error" class="mt-4 rounded-md bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">
          {{ error }}
        </p>
      </div>

      <div class="flex justify-end gap-3 border-t border-[#ececf2] px-6 py-5">
        <button
          type="button"
          class="inline-flex h-11 items-center justify-center rounded-md border border-[#d4d8e8] bg-white px-5 text-sm font-bold text-[#4d5870] transition hover:bg-[#f7f7fa]"
          :disabled="uploading"
          @click="$emit('close')"
        >
          취소
        </button>
        <button
          type="button"
          class="inline-flex h-11 min-w-[120px] items-center justify-center rounded-md bg-[#07158f] px-5 text-sm font-extrabold text-white transition hover:bg-[#111fa3] disabled:cursor-not-allowed disabled:bg-[#8b93c8]"
          :disabled="uploading || !file"
          @click="$emit('upload')"
        >
          {{ uploading ? '업로드 중' : '업로드' }}
        </button>
      </div>
    </section>
  </div>
</template>

<script setup>
defineProps({
  open: Boolean,
  file: {
    type: Object,
    default: null,
  },
  uploading: Boolean,
  error: {
    type: String,
    default: '',
  },
})

defineEmits(['close', 'file-change', 'file-drop', 'clear-file', 'upload'])
</script>
