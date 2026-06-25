<template>
  <Teleport to="body">
    <div
      v-if="isExpanded"
      class="fixed inset-0 z-[100] flex items-end justify-center bg-[#08113d]/42 px-3 py-4 backdrop-blur-sm md:items-center md:px-6"
      @click.self="isExpanded = false"
    >
      <section
        class="flex h-[min(860px,calc(100vh-32px))] w-full max-w-4xl flex-col overflow-hidden rounded-[22px] border border-white/70 bg-[#f3f6ff] shadow-[0_28px_90px_rgba(0,18,120,0.28)]"
        aria-label="CardFit AI 확대 채팅"
      >
        <header class="flex items-center justify-between gap-4 border-b border-[#dfe5f5] bg-white px-5 py-4">
          <div class="flex min-w-0 items-center gap-3">
            <AiAvatar size="large" />
            <div class="min-w-0">
              <p class="text-xs font-black uppercase tracking-[0.16em] text-[#6370a0]">CardFit AI Talk</p>
              <h2 class="truncate text-lg font-black text-[#111827]">피티와 소비 리포트 상담</h2>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <button
              type="button"
              class="rounded-full border border-[#d9def0] bg-white px-4 py-2 text-sm font-extrabold text-[#001278] transition hover:border-[#001278] hover:bg-[#eef2ff]"
              @click="isExpanded = false"
            >
              작게 보기
            </button>
            <button
              type="button"
              class="inline-flex h-10 w-10 items-center justify-center rounded-full bg-[#eef2ff] text-[#001278] transition hover:bg-[#dfe6ff]"
              aria-label="확대 채팅 닫기"
              @click="isExpanded = false"
            >
              <svg class="h-5 w-5" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                <path d="m5 5 10 10" />
                <path d="m15 5-10 10" />
              </svg>
            </button>
          </div>
        </header>

        <div class="grid min-h-0 flex-1 md:grid-cols-[260px_1fr]">
          <aside class="hidden border-r border-[#dfe5f5] bg-white/72 p-5 md:block">
            <div class="rounded-[18px] bg-[linear-gradient(135deg,#001278,#3152ff)] p-5 text-white shadow-[0_18px_44px_rgba(0,18,120,0.18)]">
              <AiAvatar size="large" />
              <h3 class="mt-4 text-xl font-black">안녕하세요, 피티예요.</h3>
              <p class="mt-2 text-sm leading-6 text-white/80">
                CSV 소비 리포트와 설문 정보를 같이 보면서 카드 혜택을 대화하듯 정리해드릴게요.
              </p>
            </div>
            <div class="mt-5 space-y-2">
              <button
                v-for="prompt in suggestedPrompts"
                :key="`expanded-${prompt}`"
                type="button"
                class="w-full rounded-2xl border border-[#e1e6f5] bg-white px-4 py-3 text-left text-sm font-extrabold text-[#001278] shadow-sm transition hover:-translate-y-0.5 hover:border-[#001278] hover:bg-[#f7f9ff]"
                @click="sendMessage(prompt)"
              >
                {{ prompt }}
              </button>
            </div>
          </aside>

          <div class="flex min-h-0 flex-col">
            <div ref="expandedScroll" class="flex-1 space-y-4 overflow-y-auto px-4 py-5 md:px-7">
              <ChatMessage
                v-for="message in messages"
                :key="`expanded-message-${message.id}`"
                :message="message"
              />
              <TypingMessage v-if="isSending" />
            </div>

            <form class="flex gap-2 border-t border-[#dfe5f5] bg-white p-3 md:p-4" @submit.prevent="handleSubmit">
              <input
                v-model="draft"
                type="text"
                class="min-w-0 flex-1 rounded-full border border-[#d4d8e8] bg-[#f8f9ff] px-5 py-3 text-sm outline-none transition placeholder:text-[#8b93a7] focus:border-[#001278] focus:bg-white focus:ring-2 focus:ring-[#001278]/10"
                placeholder="피티에게 궁금한 걸 물어보세요"
              />
              <button
                type="submit"
                class="inline-flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-[#001278] text-white shadow-[0_10px_24px_rgba(0,18,120,0.22)] transition hover:bg-[#1428c8] disabled:cursor-not-allowed disabled:bg-[#b8bfd8]"
                :disabled="!draft.trim()"
                aria-label="AI에게 질문 보내기"
              >
                <svg class="h-5 w-5" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true">
                  <path d="M3 10 17 3l-4 14-3-6-7-1Z" />
                  <path d="m10 11 7-8" />
                </svg>
              </button>
            </form>
          </div>
        </div>
      </section>
    </div>
  </Teleport>

  <div class="fixed bottom-5 right-5 z-[90] flex flex-col items-end gap-3 md:bottom-7 md:right-7">
    <section
      v-if="isOpen"
      class="w-[calc(100vw-32px)] max-w-[420px] overflow-hidden rounded-[24px] border border-white/70 bg-white/90 shadow-[0_26px_80px_rgba(0,18,120,0.24)] backdrop-blur-xl"
      aria-label="금융 전문 AI 채팅"
    >
      <header class="relative overflow-hidden bg-[radial-gradient(circle_at_18%_10%,rgba(255,255,255,0.34),transparent_22%),linear-gradient(135deg,#001278_0%,#2142ff_55%,#06b6d4_120%)] px-5 py-5 text-white">
        <div class="pointer-events-none absolute right-5 top-5 h-16 w-16 rounded-full bg-white/10 blur-xl" aria-hidden="true"></div>
        <div class="flex items-start justify-between gap-4">
          <div class="flex items-start gap-3">
            <AiAvatar />
            <div>
              <p class="inline-flex rounded-full bg-white/15 px-3 py-1 text-[11px] font-extrabold uppercase tracking-widest text-white/75">
                CardFit AI Talk
              </p>
              <h2 class="mt-3 text-xl font-black tracking-tight">피티와 카드 상담</h2>
            </div>
          </div>
          <div class="flex shrink-0 gap-2">
            <button
              type="button"
              class="inline-flex h-9 w-9 items-center justify-center rounded-full bg-white/10 text-white/80 transition hover:bg-white/20 hover:text-white"
              aria-label="AI 채팅 크게 보기"
              @click.stop="openExpandedChat"
            >
              <svg class="h-5 w-5" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                <path d="M7 3H3v4" />
                <path d="M13 3h4v4" />
                <path d="M17 13v4h-4" />
                <path d="M3 13v4h4" />
              </svg>
            </button>
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
        </div>
        <p class="mt-3 max-w-[280px] text-sm leading-5 text-white/82">
          카톡하듯 가볍게 물어보세요. 소비 리포트와 설문까지 같이 보고 답할게요.
        </p>
      </header>

      <div ref="compactScroll" class="max-h-[430px] space-y-3 overflow-y-auto bg-[#eaf0ff] px-4 py-4">
        <ChatMessage
          v-for="message in messages"
          :key="`compact-message-${message.id}`"
          :message="message"
        />
        <TypingMessage v-if="isSending" />

        <div class="flex flex-wrap gap-2 pt-2">
          <button
            v-for="prompt in suggestedPrompts"
            :key="`compact-${prompt}`"
            type="button"
            class="rounded-full border border-[#d9def0] bg-white/95 px-3.5 py-2 text-left text-xs font-extrabold text-[#001278] shadow-sm transition hover:-translate-y-0.5 hover:border-[#001278] hover:bg-[#fff7a8]"
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
          placeholder="피티에게 톡 보내기"
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
      <AiAvatar class="relative" />
      <span class="relative hidden text-left md:block">
        <span class="block text-xs font-bold text-white/70">CardFit Talk</span>
        <span class="block text-sm font-extrabold">피티에게 톡하기</span>
      </span>
    </button>
  </div>
</template>

<script setup>
import { computed, defineComponent, h, nextTick, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { aiService } from '../../services/aiService'

const AiAvatar = defineComponent({
  name: 'AiAvatar',
  props: {
    size: {
      type: String,
      default: 'normal',
    },
  },
  setup(props, { attrs }) {
    return () => {
      const isLarge = props.size === 'large'

      return h(
        'span',
        {
          ...attrs,
          class: [
            isLarge ? 'h-14 w-14' : 'h-11 w-11',
            'relative inline-flex shrink-0 items-center justify-center',
            attrs.class,
          ],
        },
        [
          h(
            'svg',
            {
              class: isLarge ? 'h-14 w-14' : 'h-11 w-11',
              viewBox: '0 0 44 44',
              fill: 'none',
              'aria-hidden': 'true',
            },
            [
              h('rect', {
                x: '8',
                y: '11',
                width: '28',
                height: '22',
                rx: '7',
                fill: '#001278',
              }),
              h('rect', {
                x: '11',
                y: '15',
                width: '22',
                height: '4',
                rx: '2',
                fill: '#6DDCFF',
              }),
              h('circle', { cx: '18', cy: '25', r: '2.2', fill: '#FFFFFF' }),
              h('circle', { cx: '27', cy: '25', r: '2.2', fill: '#FFFFFF' }),
              h('path', {
                d: 'M18 29c2.4 1.8 6.2 1.8 8.5 0',
                stroke: '#FFFFFF',
                'stroke-width': '2',
                'stroke-linecap': 'round',
              }),
              h('path', {
                d: 'M31 7l1.2 3.2L35.5 12l-3.3 1.2L31 16.5l-1.2-3.3L26.5 12l3.3-1.8L31 7Z',
                fill: '#FAE100',
              }),
              h('path', {
                d: 'M12 7l.7 1.8 1.8.7-1.8.7-.7 1.8-.7-1.8-1.8-.7 1.8-.7L12 7Z',
                fill: '#78E7FF',
              }),
            ],
          ),
        ],
      )
    }
  },
})

const ChatMessage = defineComponent({
  name: 'ChatMessage',
  props: {
    message: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    return () => {
      const isUser = props.message.role === 'user'

      return h(
        'div',
        {
          class: [
            'flex items-end',
            isUser ? 'justify-end' : 'justify-start',
          ],
        },
        [
          h('div', { class: ['max-w-[84%]', isUser ? 'items-end' : 'items-start'] }, [
            !isUser && h('p', { class: 'mb-1 ml-1 text-[11px] font-black text-[#66729a]' }, '피티'),
            h('div', {
              class: [
                'chat-markdown rounded-[18px] px-4 py-3 text-sm leading-6 shadow-sm',
                isUser
                  ? 'rounded-br-md bg-[#001278] text-white'
                  : 'rounded-bl-md border border-white bg-white text-[#23283a]',
              ],
              innerHTML: renderMarkdown(props.message.text || ''),
            }),
          ]),
        ],
      )
    }
  },
})

const TypingMessage = defineComponent({
  name: 'TypingMessage',
  setup() {
    return () => h('div', { class: 'flex items-end justify-start' }, [
      h('div', { class: 'min-w-[260px] overflow-hidden rounded-[18px] rounded-bl-md border border-[#dfe6ff] bg-white text-sm font-bold text-[#4d5870] shadow-sm' }, [
        h('div', { class: 'relative px-4 py-3' }, [
          h('span', { class: 'typing-scan absolute inset-x-0 top-0 h-full bg-[linear-gradient(90deg,transparent,rgba(0,18,120,0.08),transparent)]', 'aria-hidden': 'true' }),
          h('div', { class: 'relative flex items-center gap-3' }, [
            h('span', { class: 'thinking-orb relative inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-[#eef2ff]' }, [
              h('span', { class: 'absolute h-full w-full rounded-full border border-[#001278]/30' }),
              h('span', { class: 'h-3 w-3 rounded-full bg-[#001278]' }),
            ]),
            h('div', { class: 'min-w-0' }, [
              h('p', { class: 'text-sm font-black text-[#001278]' }, '피티가 답변을 만들고 있어요'),
              h('div', { class: 'mt-1 flex items-center gap-1.5 text-[11px] font-extrabold text-[#66729a]' }, [
                h('span', { class: 'typing-step typing-step-1' }, '소비 맥락 확인'),
                h('span', { class: 'text-[#b8bfd8]' }, '·'),
                h('span', { class: 'typing-step typing-step-2' }, '카드 혜택 비교'),
                h('span', { class: 'text-[#b8bfd8]' }, '·'),
                h('span', { class: 'typing-step typing-step-3' }, '답변 정리'),
              ]),
            ]),
          ]),
          h('div', { class: 'relative mt-3 grid grid-cols-3 gap-1.5', 'aria-hidden': 'true' }, [
            h('span', { class: 'typing-block typing-block-1 h-1.5 rounded-full bg-[#001278]' }),
            h('span', { class: 'typing-block typing-block-2 h-1.5 rounded-full bg-[#4f7cff]' }),
            h('span', { class: 'typing-block typing-block-3 h-1.5 rounded-full bg-[#06b6d4]' }),
          ]),
        ]),
      ]),
    ])
  },
})

const isOpen = ref(false)
const isExpanded = ref(false)
const draft = ref('')
const isSending = ref(false)
const compactScroll = ref(null)
const expandedScroll = ref(null)
const route = useRoute()
const messages = ref([
  {
    id: 1,
    role: 'assistant',
    text: '안녕하세요. 저는 **피티**예요.\n\nCSV 소비 리포트와 설문을 같이 보면서 카드 혜택을 톡하듯 쉽게 정리해드릴게요.',
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

function openExpandedChat() {
  isOpen.value = true
  isExpanded.value = true
  scrollToBottom()
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
      page_context: buildPageContext(),
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
    scrollToBottom()
  }
}

function hasAny(text, keywords) {
  const lowerText = text.toLowerCase()
  return keywords.some((keyword) => lowerText.includes(String(keyword).toLowerCase()))
}

function buildPageContext() {
  const heading = document.querySelector('main h1, h1')?.textContent?.trim() || ''
  const subheading = document.querySelector('main h2, h2')?.textContent?.trim() || ''

  return {
    route_name: route.name || '',
    path: route.path,
    full_path: route.fullPath,
    params: route.params || {},
    query: route.query || {},
    page_title: document.title || '',
    visible_heading: heading,
    visible_subheading: subheading,
    page_kind: getPageKind(route.name),
  }
}

function getPageKind(routeName) {
  const pageKindMap = {
    home: '홈/추천 시작 페이지',
    cards: '카드 검색 목록 페이지',
    'card-detail': '카드 상세 페이지',
    compare: '카드 비교 페이지',
    community: '커뮤니티 목록 페이지',
    'community-write': '커뮤니티 글쓰기 페이지',
    'community-detail': '커뮤니티 상세 페이지',
    report: '소비 리포트 페이지',
    'ai-recommendations': 'AI 카드 추천 설문/시작 페이지',
    'ai-recommendations-result': 'AI 카드 추천 결과 페이지',
    profile: '내 프로필/설문/CSV 관리 페이지',
    login: '로그인 페이지',
    signup: '회원가입 페이지',
  }

  return pageKindMap[routeName] || 'CardFit 앱 페이지'
}

function scrollToBottom() {
  nextTick(() => {
    for (const target of [compactScroll.value, expandedScroll.value]) {
      if (target) target.scrollTop = target.scrollHeight
    }
  })
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

function renderInlineMarkdown(value) {
  return escapeHtml(value)
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/`(.+?)`/g, '<code>$1</code>')
}

function renderMarkdown(value) {
  const lines = String(value || '').split('\n')
  const html = []
  let listOpen = false

  for (const line of lines) {
    const trimmed = line.trim()

    if (!trimmed) {
      if (listOpen) {
        html.push('</ul>')
        listOpen = false
      }
      html.push('<br>')
      continue
    }

    if (/^[-*]\s+/.test(trimmed)) {
      if (!listOpen) {
        html.push('<ul>')
        listOpen = true
      }
      html.push(`<li>${renderInlineMarkdown(trimmed.replace(/^[-*]\s+/, ''))}</li>`)
      continue
    }

    if (listOpen) {
      html.push('</ul>')
      listOpen = false
    }

    if (/^#{1,3}\s+/.test(trimmed)) {
      html.push(`<strong>${renderInlineMarkdown(trimmed.replace(/^#{1,3}\s+/, ''))}</strong>`)
      continue
    }

    html.push(`<p>${renderInlineMarkdown(trimmed)}</p>`)
  }

  if (listOpen) html.push('</ul>')
  return html.join('')
}

watch([messages, isOpen, isExpanded], scrollToBottom, { deep: true })

</script>

<style scoped>
.chat-markdown :deep(strong) {
  font-weight: 900;
}

.chat-markdown :deep(p + p) {
  margin-top: 0.5rem;
}

.chat-markdown :deep(ul) {
  margin: 0.35rem 0 0;
  padding-left: 1rem;
  list-style: disc;
}

.chat-markdown :deep(li + li) {
  margin-top: 0.25rem;
}

.chat-markdown :deep(code) {
  border-radius: 0.375rem;
  background: rgba(0, 18, 120, 0.08);
  padding: 0.08rem 0.3rem;
  font-size: 0.85em;
  font-weight: 800;
}

.typing-scan {
  animation: typing-scan 1.25s infinite linear;
}

.thinking-orb > span:first-child {
  animation: typing-pulse-ring 1.15s infinite ease-out;
}

.thinking-orb > span:last-child {
  animation: typing-pulse-dot 0.9s infinite ease-in-out;
}

.typing-step {
  animation: typing-step 1.8s infinite ease-in-out;
}

.typing-step-2 {
  animation-delay: 0.35s;
}

.typing-step-3 {
  animation-delay: 0.7s;
}

.typing-block {
  opacity: 0.28;
  transform-origin: left center;
  animation: typing-block 1.05s infinite ease-in-out;
}

.typing-block-2 {
  animation-delay: 0.16s;
}

.typing-block-3 {
  animation-delay: 0.32s;
}

@keyframes typing-scan {
  from {
    transform: translateX(-100%);
  }

  to {
    transform: translateX(100%);
  }
}

@keyframes typing-pulse-ring {
  0% {
    transform: scale(0.72);
    opacity: 0.9;
  }

  100% {
    transform: scale(1.35);
    opacity: 0;
  }
}

@keyframes typing-pulse-dot {
  0%,
  100% {
    transform: scale(0.82);
    opacity: 0.72;
  }

  50% {
    transform: scale(1.12);
    opacity: 1;
  }
}

@keyframes typing-step {
  0%,
  100% {
    color: #8b93a7;
  }

  35% {
    color: #001278;
  }
}

@keyframes typing-block {
  0%,
  100% {
    opacity: 0.28;
    transform: scaleX(0.48);
  }

  45% {
    opacity: 1;
    transform: scaleX(1);
  }
}
</style>
