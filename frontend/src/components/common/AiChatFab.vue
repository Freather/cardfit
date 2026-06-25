<template>
  <div class="fixed bottom-5 right-5 z-[90] flex flex-col items-end gap-3 md:bottom-7 md:right-7">
    <section
      v-if="isOpen"
      class="w-[calc(100vw-32px)] max-w-[400px] overflow-hidden rounded-[24px] border border-white/70 bg-white/85 shadow-[0_26px_80px_rgba(0,18,120,0.24)] backdrop-blur-xl"
      aria-label="금융 전문 AI 채팅"
    >
      <header class="relative overflow-hidden bg-[radial-gradient(circle_at_18%_10%,rgba(255,255,255,0.34),transparent_22%),linear-gradient(135deg,#001278_0%,#2142ff_55%,#06b6d4_120%)] px-5 py-5 text-white">
        <div class="absolute right-5 top-5 h-16 w-16 rounded-full bg-white/10 blur-xl" aria-hidden="true"></div>
        <div class="flex items-start justify-between gap-4">
          <div>
            <p class="inline-flex rounded-full bg-white/15 px-3 py-1 text-[11px] font-extrabold uppercase tracking-widest text-white/75">
              CardFit AI
            </p>
            <h2 class="mt-3 text-xl font-black tracking-tight">금융 전문 AI</h2>
          </div>
          <button
            type="button"
            class="inline-flex h-9 w-9 items-center justify-center rounded-full bg-white/10 text-white/80 transition hover:bg-white/20 hover:text-white"
            aria-label="AI 채팅 닫기"
            @click="isOpen = false"
          >
            <svg class="h-5 w-5" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
              <path d="m5 5 10 10" />
              <path d="m15 5-10 10" />
            </svg>
          </button>
        </div>
        <p class="mt-3 max-w-[280px] text-sm leading-5 text-white/82">
          카드 혜택부터 소비 습관까지 쉽게 풀어드릴게요.
        </p>
      </header>

      <div class="max-h-[410px] space-y-3 overflow-y-auto bg-gradient-to-b from-[#f7f8ff] to-[#fbf9f8] px-4 py-4">
        <div
          v-for="message in messages"
          :key="message.id"
          class="flex"
          :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
        >
          <p
            class="max-w-[82%] whitespace-pre-line rounded-[18px] px-4 py-3 text-sm leading-5 shadow-sm"
            :class="
              message.role === 'user'
                ? 'rounded-br-md bg-[#001278] text-white'
                : 'rounded-bl-md border border-white bg-white/95 text-[#23283a]'
            "
          >
            {{ message.text }}
          </p>
        </div>

        <div v-if="isSending" class="flex justify-start">
          <p class="max-w-[82%] rounded-[18px] rounded-bl-md border border-white bg-white/95 px-4 py-3 text-sm leading-5 text-[#6b7280] shadow-sm">
            답변을 만들고 있어요...
          </p>
        </div>

        <div class="flex flex-wrap gap-2 pt-2">
          <button
            v-for="prompt in suggestedPrompts"
            :key="prompt"
            type="button"
            class="rounded-full border border-[#d9def0] bg-white/90 px-3.5 py-2 text-left text-xs font-extrabold text-[#001278] shadow-sm transition hover:-translate-y-0.5 hover:border-[#001278] hover:bg-[#eef1ff]"
            @click="sendMessage(prompt)"
          >
            {{ prompt }}
          </button>
        </div>
      </div>

      <form class="flex gap-2 border-t border-white bg-white/90 p-3 backdrop-blur" @submit.prevent="handleSubmit">
        <input
          v-model="draft"
          type="text"
          class="min-w-0 flex-1 rounded-full border border-[#d4d8e8] bg-[#f8f9ff] px-4 py-3 text-sm outline-none transition placeholder:text-[#8b93a7] focus:border-[#001278] focus:bg-white focus:ring-2 focus:ring-[#001278]/10"
          placeholder="궁금한 걸 물어보세요"
        />
        <button
          type="submit"
          class="inline-flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-[#001278] text-white shadow-[0_10px_24px_rgba(0,18,120,0.22)] transition hover:bg-[#1428c8] disabled:cursor-not-allowed disabled:bg-[#b8bfd8]"
          :disabled="!draft.trim()"
          aria-label="AI에게 질문 보내기"
        >
          <svg class="h-5 w-5" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true">
            <path d="M3 10 17 3l-4 14-3-6-7-1Z" />
            <path d="m10 11 7-8" />
          </svg>
        </button>
      </form>
    </section>

    <button
      type="button"
      class="group relative flex h-16 items-center gap-3 overflow-hidden rounded-full bg-[linear-gradient(135deg,#001278_0%,#3152ff_55%,#00c2ff_130%)] px-5 text-white shadow-[0_18px_44px_rgba(0,18,120,0.34)] transition hover:-translate-y-0.5 hover:shadow-[0_24px_52px_rgba(0,18,120,0.4)] focus:outline-none focus:ring-4 focus:ring-[#001278]/20"
      :aria-expanded="isOpen"
      aria-label="금융 전문 AI 채팅 열기"
      @click="isOpen = !isOpen"
    >
      <span class="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(255,255,255,0.36),transparent_24%)]" aria-hidden="true"></span>
      <span class="relative flex h-10 w-10 items-center justify-center rounded-full bg-white/18 ring-1 ring-white/20">
        <svg class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true">
          <path d="M12 3a7 7 0 0 0-7 7v3a4 4 0 0 0 4 4h1l2 3 2-3h1a4 4 0 0 0 4-4v-3a7 7 0 0 0-7-7Z" />
          <path d="M9 10h.01" />
          <path d="M15 10h.01" />
          <path d="M9.5 13a4 4 0 0 0 5 0" />
        </svg>
      </span>
      <span class="relative hidden text-left md:block">
        <span class="block text-xs font-bold text-white/70">AI Chat</span>
        <span class="block text-sm font-extrabold">금융 AI에게 물어보기</span>
      </span>
    </button>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

import { aiService } from '../../services/aiService'

const isOpen = ref(false)
const draft = ref('')
const isSending = ref(false)
const messages = ref([
  {
    id: 1,
    role: 'assistant',
    text: '안녕하세요. 카드 혜택과 소비 분석을 쉽게 알려드릴게요.',
  },
])
const defaultPrompts = [
  '내 소비에 맞는 카드는?',
  '전월 실적 쉽게 알려줘',
  '연회비는 어떻게 비교해?',
]
const promptGroups = {
  spending: [
    '식비가 많으면 어떤 카드가 좋아?',
    '쇼핑 혜택은 뭘 봐야 해?',
    '소비 리포트는 어떻게 읽어?',
  ],
  performance: [
    '전월 실적 채우는 팁 알려줘',
    '실적 조건 낮은 카드가 좋아?',
    '실적 제외 항목도 있어?',
  ],
  annualFee: [
    '연회비 아끼는 기준은?',
    '혜택이 연회비보다 큰지 봐줘',
    '무료 카드가 더 나을 때는?',
  ],
  compare: [
    '두 카드 비교 기준 알려줘',
    '월 혜택이 큰 카드가 무조건 좋아?',
    '내 소비랑 맞는 점수는 뭐야?',
  ],
}

const suggestedPrompts = computed(() => {
  const lastUserMessage = [...messages.value].reverse().find((message) => message.role === 'user')?.text || ''
  const lastAssistantMessage = [...messages.value].reverse().find((message) => message.role === 'assistant')?.text || ''
  const context = `${lastUserMessage} ${lastAssistantMessage}`

  if (hasAny(context, ['전월', '실적', '조건'])) return promptGroups.performance
  if (hasAny(context, ['연회비', '무료', '1년', '비용'])) return promptGroups.annualFee
  if (hasAny(context, ['비교', '점수', '추천', '랭킹'])) return promptGroups.compare
  if (hasAny(context, ['소비', '식비', '쇼핑', '교통', '통신', '리포트'])) return promptGroups.spending

  return defaultPrompts
})

function handleSubmit() {
  sendMessage(draft.value)
}

async function sendMessage(text) {
  const question = text.trim()
  if (!question || isSending.value) return

  const nextMessages = [
    ...messages.value,
    {
      id: Date.now(),
      role: 'user',
      text: question,
    },
  ]
  messages.value = nextMessages
  draft.value = ''
  isSending.value = true

  try {
    const payload = {
      messages: nextMessages.map((message) => ({
        role: message.role,
        content: message.text,
      })),
    }
    const { data } = await aiService.chat(payload)
    messages.value = [
      ...nextMessages,
      {
        id: Date.now() + 1,
        role: 'assistant',
        text: data?.reply || '답변을 만들지 못했어요. 다시 시도해주세요.',
      },
    ]
  } catch (error) {
    messages.value = [
      ...nextMessages,
      {
        id: Date.now() + 1,
        role: 'assistant',
        text: '지금은 답변을 만들지 못했어요.\n잠시 후 다시 시도해주세요.',
      },
    ]
  } finally {
    isSending.value = false
  }
}

function hasAny(text, keywords) {
  const lowerText = text.toLowerCase()
  return keywords.some((keyword) => lowerText.includes(String(keyword).toLowerCase()))
}

</script>
