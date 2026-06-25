<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { getApiErrorMessage } from '../services/api'
import { communityService } from '../services/communityService'

const router = useRouter()

const form = ref({
  category: '',
  title: '',
  content: '',
})
const errorMessage = ref('')
const isSubmitting = ref(false)
const editorRef = ref(null)
const isExampleModalOpen = ref(false)
const insertModal = ref({
  open: false,
  type: 'link',
  label: '',
  value: '',
  error: '',
})
const savedSelection = ref(null)
const toolbarState = ref({
  bold: false,
  italic: false,
  underline: false,
  orderedList: false,
  unorderedList: false,
})

const categories = [
  { value: 'review', label: '카드 추천/후기' },
  { value: 'info', label: '혜택 꿀팁' },
  { value: 'general', label: '자유게시판' },
  { value: 'question', label: '질문답변' },
]

const guidelines = [
  {
    title: '서로 존중해주세요.',
    description: '카드 사용 경험과 의견은 친절하고 배려 있게 나눠주세요.',
  },
  {
    title: '광고성 글은 피해주세요.',
    description: '반복 홍보, 과도한 자기 홍보, 무관한 링크는 제한될 수 있습니다.',
  },
  {
    title: '정확한 정보를 작성해주세요.',
    description: '금융 혜택과 카드 조건은 가능한 최신 기준으로 공유해주세요.',
  },
  {
    title: '개인정보를 남기지 마세요.',
    description: '카드번호, 계좌번호, 연락처 등 민감한 정보는 공개하지 마세요.',
  },
]

function syncEditorContent() {
  form.value.content = editorRef.value?.innerHTML || ''
}

function focusEditor() {
  editorRef.value?.focus()
}

function isSelectionInEditor() {
  const editor = editorRef.value
  const selection = window.getSelection()
  if (!editor || !selection || selection.rangeCount === 0) return false

  const range = selection.getRangeAt(0)
  return editor.contains(range.commonAncestorContainer)
}

function saveEditorSelection() {
  const selection = window.getSelection()
  if (!selection || selection.rangeCount === 0 || !isSelectionInEditor()) return

  savedSelection.value = selection.getRangeAt(0).cloneRange()
  updateToolbarState()
}

function restoreEditorSelection() {
  if (!savedSelection.value) return

  const selection = window.getSelection()
  selection.removeAllRanges()
  selection.addRange(savedSelection.value)
}

function updateToolbarState() {
  toolbarState.value = {
    bold: document.queryCommandState('bold'),
    italic: document.queryCommandState('italic'),
    underline: document.queryCommandState('underline'),
    orderedList: isSelectionInsideTag('OL'),
    unorderedList: isSelectionInsideTag('UL'),
  }
}

function isSelectionInsideTag(tagName) {
  const editor = editorRef.value
  const selection = window.getSelection()
  if (!editor || !selection || selection.rangeCount === 0) return false

  let node = selection.anchorNode
  if (node?.nodeType === Node.TEXT_NODE) node = node.parentElement

  while (node && node !== editor) {
    if (node.tagName === tagName) return true
    node = node.parentElement
  }

  return false
}

function runEditorCommand(command, value = null) {
  focusEditor()
  restoreEditorSelection()
  document.execCommand(command, false, value)
  syncEditorContent()
  saveEditorSelection()
  updateToolbarState()
}

function toolbarButtonClass(active) {
  return active
    ? 'border border-[#001278] bg-white text-[#001278] shadow-sm'
    : 'border border-transparent text-[#111827] hover:bg-white'
}

function escapeHtml(value) {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
}

function placeCursorInLastListItem(type) {
  requestAnimationFrame(() => {
    const editor = editorRef.value
    const listItems = editor?.querySelectorAll(`${type} li`)
    const lastItem = listItems?.[listItems.length - 1]
    if (!lastItem) return

    const range = document.createRange()
    range.selectNodeContents(lastItem)
    range.collapse(false)

    const selection = window.getSelection()
    selection.removeAllRanges()
    selection.addRange(range)
    focusEditor()
    saveEditorSelection()
  })
}

function placeCursorAtEnd(node) {
  requestAnimationFrame(() => {
    if (!node) return

    const range = document.createRange()
    range.selectNodeContents(node)
    range.collapse(false)

    const selection = window.getSelection()
    selection.removeAllRanges()
    selection.addRange(range)
    focusEditor()
    saveEditorSelection()
    updateToolbarState()
  })
}

function getCurrentListContext() {
  const editor = editorRef.value
  const selection = window.getSelection()
  if (!editor || !selection || selection.rangeCount === 0) return null

  let node = selection.anchorNode
  if (node?.nodeType === Node.TEXT_NODE) node = node.parentElement

  let listItem = null
  let list = null

  while (node && node !== editor) {
    if (node.tagName === 'LI' && !listItem) listItem = node
    if (node.tagName === 'OL' || node.tagName === 'UL') {
      list = node
      break
    }
    node = node.parentElement
  }

  if (!list) return null

  return {
    list,
    listItem,
    itemIndex: listItem ? Array.from(list.children).indexOf(listItem) : 0,
    type: list.tagName.toLowerCase(),
  }
}

function buildListWithItems(type, items) {
  if (!items.length) return null

  const list = document.createElement(type)
  items.forEach((item) => list.appendChild(item.cloneNode(true)))
  return list
}

function replaceCurrentListItem(context, replacementNode, cursorNode = replacementNode) {
  const items = Array.from(context.list.children)
  const beforeList = buildListWithItems(context.type, items.slice(0, context.itemIndex))
  const afterList = buildListWithItems(context.type, items.slice(context.itemIndex + 1))
  const nodes = [beforeList, replacementNode, afterList].filter(Boolean)

  context.list.replaceWith(...nodes)
  syncEditorContent()
  placeCursorAtEnd(cursorNode)
}

function unwrapList(context) {
  if (!context.listItem) return

  const paragraph = document.createElement('p')
  paragraph.innerHTML = context.listItem.innerHTML.trim() ? context.listItem.innerHTML : '<br>'
  replaceCurrentListItem(context, paragraph)
}

function convertList(context, type) {
  if (!context.listItem) return

  const nextList = document.createElement(type)
  const nextItem = context.listItem.cloneNode(true)
  nextList.appendChild(nextItem)
  replaceCurrentListItem(context, nextList, nextItem)
}

function insertList(type) {
  focusEditor()
  restoreEditorSelection()

  const selection = window.getSelection()
  const context = getCurrentListContext()

  if (context) {
    if (context.type === type) {
      unwrapList(context)
    } else {
      convertList(context, type)
    }
    return
  }

  if (!selection || selection.rangeCount === 0) {
    document.execCommand('insertHTML', false, `<${type}><li><br></li></${type}>`)
    syncEditorContent()
    placeCursorInLastListItem(type)
    updateToolbarState()
    return
  }

  const selectedText = selection.toString().trim()
  const items = selectedText
    ? selectedText.split(/\n+/).map((line) => line.trim()).filter(Boolean)
    : []
  const html = items.length
    ? `<${type}>${items.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</${type}>`
    : `<${type}><li><br></li></${type}>`

  document.execCommand('insertHTML', false, html)
  syncEditorContent()
  if (!items.length) placeCursorInLastListItem(type)
  else saveEditorSelection()
  updateToolbarState()
}

function openInsertModal(type) {
  saveEditorSelection()
  const selectedText = type === 'link' ? window.getSelection()?.toString()?.trim() || '' : ''
  insertModal.value = {
    open: true,
    type,
    label: selectedText,
    value: '',
    error: '',
  }
}

function closeInsertModal() {
  insertModal.value.open = false
  insertModal.value.error = ''
  insertModal.value.label = ''
  insertModal.value.value = ''
}

function normalizeUrl(value) {
  const trimmed = value.trim()
  if (!trimmed) return ''
  if (/^https?:\/\//i.test(trimmed)) return trimmed
  return `https://${trimmed}`
}

function confirmInsertModal() {
  const url = normalizeUrl(insertModal.value.value)

  if (!url) {
    insertModal.value.error = '주소를 입력해주세요.'
    return
  }

  if (insertModal.value.type === 'link') {
    const label = insertModal.value.label.trim()
    if (!label) {
      insertModal.value.error = '게시글에 보일 이름을 입력해주세요.'
      return
    }

    runEditorCommand(
      'insertHTML',
      `<a href="${escapeHtml(url)}" target="_blank" rel="noreferrer noopener">${escapeHtml(label)}</a>`,
    )
  } else {
    runEditorCommand('insertImage', url)
  }

  closeInsertModal()
}

function getEditorText() {
  return editorRef.value?.innerText?.trim() || ''
}

async function submitPost() {
  syncEditorContent()

  if (!form.value.category) {
    errorMessage.value = '카테고리를 선택해주세요.'
    return
  }

  if (!form.value.title.trim()) {
    errorMessage.value = '제목을 입력해주세요.'
    return
  }

  if (!getEditorText()) {
    errorMessage.value = '내용을 입력해주세요.'
    return
  }

  errorMessage.value = ''
  isSubmitting.value = true

  try {
    const { data } = await communityService.createPost({
      category: form.value.category,
      title: form.value.title.trim(),
      content: form.value.content,
    })

    router.push({ name: 'community-detail', params: { id: data.id } })
  } catch (error) {
    errorMessage.value = getApiErrorMessage(error, '글을 올리지 못했어요. 다시 시도해주세요.')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <section class="min-h-screen bg-[#faf8f7] px-5 py-10 text-[#111827] lg:px-8">
    <div class="mx-auto max-w-[1120px]">
      <div>
        <h1 class="text-3xl font-extrabold tracking-tight">게시글 작성</h1>
        <p class="mt-2 text-sm text-[#4d5870]">CardFit 커뮤니티에 나만의 카드 생활 팁을 공유해보세요.</p>
      </div>

      <div class="mt-9 grid gap-8 lg:grid-cols-[1fr_310px]">
        <main class="rounded-lg border border-[#d7dbea] bg-white p-6 shadow-sm">
          <form @submit.prevent="submitPost">
            <label class="grid gap-2">
              <span class="text-xs font-extrabold uppercase tracking-wide text-[#30374d]">카테고리</span>
              <select
                v-model="form.category"
                class="h-12 rounded-md border border-[#cfd4e5] bg-[#f7f5f5] px-4 text-sm font-semibold text-[#30374d] outline-none transition focus:border-[#001278] focus:ring-2 focus:ring-[#001278]/10"
              >
                <option value="">카테고리를 선택하세요</option>
                <option v-for="category in categories" :key="category.value" :value="category.value">
                  {{ category.label }}
                </option>
              </select>
            </label>

            <label class="mt-5 grid gap-2">
              <span class="text-xs font-extrabold uppercase tracking-wide text-[#30374d]">제목</span>
              <input
                v-model="form.title"
                type="text"
                class="h-12 rounded-md border border-[#cfd4e5] bg-[#f7f5f5] px-4 text-sm font-semibold text-[#111827] outline-none transition placeholder:text-[#8b93a7] focus:border-[#001278] focus:ring-2 focus:ring-[#001278]/10"
                placeholder="제목을 입력하세요"
              />
            </label>

            <section class="mt-5 overflow-hidden rounded-md border border-[#cfd4e5]">
              <div class="flex h-11 items-center gap-1 border-b border-[#cfd4e5] bg-[#efeded] px-3">
                <button
                  type="button"
                  class="h-8 w-8 rounded text-sm font-extrabold transition"
                  :class="toolbarButtonClass(toolbarState.bold)"
                  aria-label="굵게"
                  title="굵게"
                  @mousedown.prevent
                  @click="runEditorCommand('bold')"
                >
                  B
                </button>
                <button
                  type="button"
                  class="h-8 w-8 rounded text-sm italic transition"
                  :class="toolbarButtonClass(toolbarState.italic)"
                  aria-label="기울임"
                  title="기울임"
                  @mousedown.prevent
                  @click="runEditorCommand('italic')"
                >
                  I
                </button>
                <button
                  type="button"
                  class="h-8 w-8 rounded text-sm underline transition"
                  :class="toolbarButtonClass(toolbarState.underline)"
                  aria-label="밑줄"
                  title="밑줄"
                  @mousedown.prevent
                  @click="runEditorCommand('underline')"
                >
                  U
                </button>
                <button
                  type="button"
                  data-toolbar="ordered"
                  class="h-8 w-8 rounded text-sm font-bold transition"
                  :class="toolbarButtonClass(toolbarState.orderedList)"
                  aria-label="번호 목록"
                  title="번호 목록"
                  @mousedown.prevent
                  @click="insertList('ol')"
                >
                  ≡
                </button>
                <button
                  type="button"
                  data-toolbar="unordered"
                  class="h-8 w-8 rounded text-sm font-bold transition"
                  :class="toolbarButtonClass(toolbarState.unorderedList)"
                  aria-label="글머리 목록"
                  title="글머리 목록"
                  @mousedown.prevent
                  @click="insertList('ul')"
                >
                  •
                </button>
                <button
                  type="button"
                  class="h-8 w-8 rounded border border-transparent text-sm font-bold transition hover:bg-white"
                  aria-label="이미지 삽입"
                  title="이미지 삽입"
                  @mousedown.prevent
                  @click="openInsertModal('image')"
                >
                  ▣
                </button>
                <button
                  type="button"
                  class="h-8 w-8 rounded border border-transparent text-sm font-bold transition hover:bg-white"
                  aria-label="링크 삽입"
                  title="링크 삽입"
                  @mousedown.prevent
                  @click="openInsertModal('link')"
                >
                  🔗
                </button>
              </div>
              <div
                ref="editorRef"
                contenteditable="true"
                class="min-h-[320px] w-full bg-[#fbfafa] px-4 py-4 text-sm leading-7 outline-none empty:before:text-[#8b93a7] empty:before:content-['내용을_입력하세요...']"
                @input="syncEditorContent(); saveEditorSelection()"
                @keyup="saveEditorSelection"
                @mouseup="saveEditorSelection"
                @focus="updateToolbarState"
                @blur="syncEditorContent"
              />
            </section>

            <p v-if="errorMessage" class="mt-4 rounded-md bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">
              {{ errorMessage }}
            </p>

            <div class="mt-8 flex justify-end gap-3">
              <button
                type="button"
                class="h-11 rounded-md px-5 text-sm font-extrabold text-[#001278] transition hover:bg-[#eef1ff]"
                @click="router.push({ name: 'community' })"
              >
                취소
              </button>
              <button
                type="submit"
                class="h-11 rounded-md bg-[#001278] px-6 text-sm font-extrabold text-white transition hover:bg-[#1428a0] disabled:cursor-not-allowed disabled:bg-[#8b93c8]"
                :disabled="isSubmitting"
              >
                {{ isSubmitting ? '등록 중...' : '게시글 등록' }}
              </button>
            </div>
          </form>
        </main>

        <aside class="grid content-start gap-7">
          <section class="rounded-lg border border-[#d7dbea] bg-white p-6 shadow-sm">
            <h2 class="flex items-center gap-2 text-base font-extrabold">
              <span class="inline-flex h-5 w-5 items-center justify-center rounded-full border border-[#001278] text-xs text-[#001278]">i</span>
              작성 가이드
            </h2>

            <div class="mt-5 grid gap-5">
              <div v-for="guide in guidelines" :key="guide.title" class="flex gap-3">
                <span class="mt-0.5 inline-flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-[#eef1ff] text-xs font-extrabold text-[#001278]">
                  ✓
                </span>
                <div>
                  <p class="text-sm font-extrabold">{{ guide.title }}</p>
                  <p class="mt-1 text-xs leading-5 text-[#4d5870]">{{ guide.description }}</p>
                </div>
              </div>
            </div>
          </section>

          <section class="overflow-hidden rounded-lg bg-[#1d31b4] text-white shadow-lg">
            <div class="min-h-[170px] bg-[radial-gradient(circle_at_88%_70%,rgba(255,255,255,0.18),transparent_22%),linear-gradient(145deg,#001278_0%,#1d31b4_100%)] p-6">
              <h2 class="text-lg font-extrabold">작성 팁</h2>
              <p class="mt-3 text-sm leading-6 text-white/80">
                카드명, 전월 실적, 할인 한도처럼 비교 가능한 정보를 넣으면 더 많은 공감을 받을 수 있어요.
              </p>
              <button
                type="button"
                class="mt-5 h-9 rounded-md bg-white px-4 text-sm font-extrabold text-[#001278] transition hover:bg-[#eef1ff]"
                @click="isExampleModalOpen = true"
              >
                예시 보기
              </button>
            </div>
          </section>

          <section class="overflow-hidden rounded-lg bg-[#17323a] text-white shadow-lg">
            <div class="flex min-h-[170px] items-end bg-[linear-gradient(135deg,rgba(0,18,120,0.35),rgba(0,0,0,0.35)),radial-gradient(circle_at_70%_20%,rgba(255,255,255,0.24),transparent_18%)] p-6">
              <p class="text-lg font-extrabold leading-7">당신의 카드 경험이<br />다른 사용자에게 도움이 됩니다.</p>
            </div>
          </section>
        </aside>
      </div>
    </div>

    <div
      v-if="isExampleModalOpen"
      class="fixed inset-0 z-[100] flex items-center justify-center bg-black/45 px-4 py-6"
      role="dialog"
      aria-modal="true"
      aria-labelledby="example-post-title"
      @click.self="isExampleModalOpen = false"
    >
      <section class="w-full max-w-[620px] rounded-lg bg-white p-7 shadow-2xl">
        <div class="flex items-start justify-between gap-4">
          <div>
            <p class="text-sm font-extrabold text-[#001278]">인기 게시글 예시</p>
            <h2 id="example-post-title" class="mt-2 text-2xl font-extrabold leading-tight">
              삼성카드 taptap O 실제 사용기 - 스타벅스 50%의 위엄
            </h2>
          </div>
          <button
            type="button"
            class="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-md text-[#4d5870] transition hover:bg-[#f2f3f7]"
            aria-label="모달 닫기"
            @click="isExampleModalOpen = false"
          >
            <svg class="h-5 w-5" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true">
              <path d="m5 5 10 10" />
              <path d="m15 5-10 10" />
            </svg>
          </button>
        </div>

        <div class="mt-5 flex flex-wrap items-center gap-4 border-b border-[#ececf2] pb-5 text-sm text-[#4d5870]">
          <span class="font-bold">카드고수김씨</span>
          <span>2024.03.25 21:45</span>
          <span class="ml-auto">조회 1,242</span>
          <span class="font-bold text-[#001278]">추천 48</span>
        </div>

        <div class="mt-6 text-sm leading-7 text-[#30374d]">
          <p>
            안녕하세요. 오늘은 카페와 교통 지출이 많은 분들에게 잘 맞는 삼성카드 taptap O 사용기를 공유합니다.
            핵심은 카드명, 전월 실적, 할인율, 월 할인 한도를 함께 적어주는 것입니다.
          </p>

          <div class="mt-5 rounded-md bg-[#f6f3f2] p-5">
            <h3 class="font-extrabold text-[#111827]">주요 혜택 정리</h3>
            <ul class="mt-3 grid gap-2">
              <li>• 스타벅스 50% 할인 또는 커피전문점 30% 할인</li>
              <li>• 대중교통, 택시 10% 할인</li>
              <li>• 쇼핑 7% 할인 및 1% 적립</li>
              <li>• 전월 실적 30만원 이상부터 혜택 적용</li>
            </ul>
          </div>

          <p class="mt-5">
            실제로 한 달 동안 사용해보니 커피와 교통비 지출이 꾸준한 사람에게 체감 혜택이 컸습니다.
            이런 식으로 구체적인 조건과 사용 경험을 같이 적으면 읽는 사람이 판단하기 쉬워요.
          </p>
        </div>

        <div class="mt-7 flex justify-end">
          <button
            type="button"
            class="h-10 rounded-md bg-[#001278] px-5 text-sm font-extrabold text-white transition hover:bg-[#1428a0]"
            @click="isExampleModalOpen = false"
          >
            확인
          </button>
        </div>
      </section>
    </div>

    <div
      v-if="insertModal.open"
      class="fixed inset-0 z-[110] flex items-center justify-center bg-black/45 px-4 py-6"
      role="dialog"
      aria-modal="true"
      aria-labelledby="insert-modal-title"
      @click.self="closeInsertModal"
    >
      <section class="w-full max-w-[460px] rounded-lg bg-white shadow-2xl">
        <div class="flex items-start justify-between gap-4 border-b border-[#ececf2] px-6 py-5">
          <div>
            <h2 id="insert-modal-title" class="text-xl font-extrabold">
              {{ insertModal.type === 'link' ? '링크 삽입' : '이미지 삽입' }}
            </h2>
            <p class="mt-1 text-sm text-[#4d5870]">
              {{ insertModal.type === 'link' ? '게시글에 보일 이름과 연결할 주소를 입력해주세요.' : '이미지 주소를 입력해주세요.' }}
            </p>
          </div>
          <button
            type="button"
            class="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-md text-[#4d5870] transition hover:bg-[#f2f3f7]"
            aria-label="모달 닫기"
            @click="closeInsertModal"
          >
            <svg class="h-5 w-5" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true">
              <path d="m5 5 10 10" />
              <path d="m15 5-10 10" />
            </svg>
          </button>
        </div>

        <form class="px-6 py-6" @submit.prevent="confirmInsertModal">
          <label v-if="insertModal.type === 'link'" class="grid gap-2">
            <span class="text-sm font-extrabold text-[#30374d]">
              게시글에서 보일 이름
            </span>
            <input
              v-model="insertModal.label"
              type="text"
              class="h-12 rounded-md border border-[#d4d8e8] px-4 text-sm font-semibold text-[#111827] outline-none transition placeholder:text-[#8b93a7] focus:border-[#001278] focus:ring-2 focus:ring-[#001278]/10"
              placeholder="예: 삼성카드 taptap O 공식 안내"
              autofocus
            />
          </label>

          <label class="grid gap-2" :class="insertModal.type === 'link' ? 'mt-4' : ''">
            <span class="text-sm font-extrabold text-[#30374d]">
              {{ insertModal.type === 'link' ? '링크 주소' : '이미지 주소' }}
            </span>
            <input
              v-model="insertModal.value"
              type="url"
              class="h-12 rounded-md border border-[#d4d8e8] px-4 text-sm font-semibold text-[#111827] outline-none transition placeholder:text-[#8b93a7] focus:border-[#001278] focus:ring-2 focus:ring-[#001278]/10"
              :placeholder="insertModal.type === 'link' ? 'https://example.com' : 'https://example.com/image.png'"
              :autofocus="insertModal.type !== 'link'"
            />
          </label>

          <p v-if="insertModal.error" class="mt-4 rounded-md bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">
            {{ insertModal.error }}
          </p>

          <div class="mt-7 flex justify-end gap-3 border-t border-[#ececf2] pt-5">
            <button
              type="button"
              class="inline-flex h-11 items-center justify-center rounded-md border border-[#d4d8e8] bg-white px-5 text-sm font-bold text-[#4d5870] transition hover:bg-[#f7f7fa]"
              @click="closeInsertModal"
            >
              취소
            </button>
            <button
              type="submit"
              class="inline-flex h-11 min-w-[100px] items-center justify-center rounded-md bg-[#001278] px-5 text-sm font-extrabold text-white transition hover:bg-[#1428a0]"
            >
              삽입
            </button>
          </div>
        </form>
      </section>
    </div>
  </section>
</template>

<style scoped>
[contenteditable] :deep(i),
[contenteditable] :deep(em) {
  display: inline-block;
  font-style: italic;
  transform: skewX(-8deg);
}

[contenteditable] :deep(ol),
[contenteditable] :deep(ul) {
  margin: 0.5rem 0;
  padding-left: 1.5rem;
}

[contenteditable] :deep(ol) {
  list-style: decimal;
}

[contenteditable] :deep(ul) {
  list-style: disc;
}

[contenteditable] :deep(a) {
  display: inline;
  border-radius: 4px;
  background: rgba(0, 18, 120, 0.08);
  color: #001278;
  font-weight: 800;
  text-decoration: underline;
  text-decoration-thickness: 1.5px;
  text-underline-offset: 3px;
}

[contenteditable] :deep(a)::after {
  content: '↗';
  margin-left: 2px;
  font-size: 0.8em;
  text-decoration: none;
}

[data-toolbar='ordered'],
[data-toolbar='unordered'] {
  font-size: 0;
}

[data-toolbar='ordered']::before,
[data-toolbar='unordered']::before {
  font-size: 13px;
  line-height: 1;
}

[data-toolbar='ordered']::before {
  content: '1.';
}

[data-toolbar='unordered']::before {
  content: '•';
  font-size: 18px;
}
</style>
