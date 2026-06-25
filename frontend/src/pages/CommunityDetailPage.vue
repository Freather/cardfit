<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

import { getApiErrorMessage } from '../services/api'
import { communityService } from '../services/communityService'
import { useAuthStore } from '../stores/authStore'

const props = defineProps({
  id: {
    type: [String, Number],
    default: null,
  },
})

const router = useRouter()
const authStore = useAuthStore()
const post = ref(null)
const comments = ref([])
const popularPosts = ref([])
const isLoading = ref(false)
const isSaving = ref(false)
const isEditingPost = ref(false)
const errorMessage = ref('')
const loginMessage = ref('')
const shareMessage = ref('')
const newComment = ref('')
const deleteConfirm = ref({
  open: false,
  type: '',
  target: null,
})
const editPostForm = ref({
  title: '',
  content: '',
})

const isLoggedIn = computed(() => authStore.isAuthenticated)
const isPostOwner = computed(() => Boolean(post.value?.is_author))
const visibleComments = computed(() => comments.value)

async function loadPost() {
  if (!props.id) return

  isLoading.value = true
  errorMessage.value = ''

  try {
    await communityService.incrementPostView(props.id).catch(() => null)
    const [{ data }, commentsResponse] = await Promise.all([
      communityService.fetchPost(props.id),
      communityService.fetchComments(props.id).catch(() => ({ data: [] })),
    ])

    post.value = normalizePost(data)
    comments.value = (commentsResponse.data || []).map(normalizeComment)
    editPostForm.value = {
      title: post.value.title,
      content: post.value.content,
    }
  } catch (error) {
    post.value = null
    errorMessage.value = getApiErrorMessage(error, '글을 불러오지 못했어요.')
  } finally {
    isLoading.value = false
  }
}

async function loadPopularPosts() {
  try {
    const { data } = await communityService.fetchPopularPosts()
    popularPosts.value = (Array.isArray(data) ? data : []).map(normalizePost).slice(0, 5)
  } catch {
    popularPosts.value = []
  }
}

async function savePostEdit() {
  if (!post.value || isSaving.value) return
  const title = editPostForm.value.title.trim()
  const content = editPostForm.value.content.trim()

  if (!title || !content) {
    loginMessage.value = '제목과 내용을 입력해주세요.'
    return
  }

  isSaving.value = true
  loginMessage.value = ''

  try {
    const { data } = await communityService.updatePost(post.value.id, { title, content })
    post.value = normalizePost(data)
    isEditingPost.value = false
  } catch (error) {
    loginMessage.value = getApiErrorMessage(error, '글을 고치지 못했어요. 다시 시도해주세요.')
  } finally {
    isSaving.value = false
  }
}

async function deletePost() {
  if (!post.value || isSaving.value) return
  openDeleteConfirm('post')
}

async function performPostDelete() {
  if (!post.value || isSaving.value) return
  isSaving.value = true

  try {
    await communityService.deletePost(post.value.id)
    router.push({ name: 'community' })
  } catch (error) {
    loginMessage.value = getApiErrorMessage(error, '글을 삭제하지 못했어요. 다시 시도해주세요.')
  } finally {
    isSaving.value = false
  }
}

async function togglePostLike() {
  if (!isLoggedIn.value) {
    loginMessage.value = '로그인하면 추천할 수 있어요.'
    return
  }
  if (!post.value || isPostOwner.value) return

  try {
    const { data } = await communityService.togglePostLike(post.value.id)
    post.value = {
      ...post.value,
      isLiked: Boolean(data.liked),
      likes: Number(data.likes_count || 0),
    }
    loginMessage.value = ''
  } catch (error) {
    loginMessage.value = getApiErrorMessage(error, '추천하지 못했어요. 다시 시도해주세요.')
  }
}

async function addComment() {
  if (!isLoggedIn.value) {
    loginMessage.value = '로그인하면 댓글을 쓸 수 있어요.'
    return
  }

  const content = newComment.value.trim()
  if (!content || !post.value) return

  try {
    const { data } = await communityService.createComment(post.value.id, { content })
    comments.value = [...comments.value, normalizeComment(data)]
    newComment.value = ''
    post.value.comments += 1
    loginMessage.value = ''
  } catch (error) {
    loginMessage.value = getApiErrorMessage(error, '댓글을 올리지 못했어요. 다시 시도해주세요.')
  }
}

function startCommentEdit(comment) {
  comment.editContent = comment.content
  comment.isEditing = true
}

async function saveCommentEdit(comment) {
  const content = comment.editContent?.trim()
  if (!content || !post.value) return

  try {
    const { data } = await communityService.updateComment(post.value.id, comment.id, { content })
    Object.assign(comment, normalizeComment(data))
  } catch (error) {
    loginMessage.value = getApiErrorMessage(error, '댓글을 고치지 못했어요. 다시 시도해주세요.')
  }
}

async function deleteComment(comment) {
  if (!post.value) return
  openDeleteConfirm('comment', comment)
}

async function performCommentDelete(comment) {
  if (!post.value || !comment) return
  try {
    await communityService.deleteComment(post.value.id, comment.id)
    comments.value = comments.value.filter((item) => item.id !== comment.id)
    post.value.comments = Math.max(0, post.value.comments - 1)
  } catch (error) {
    loginMessage.value = getApiErrorMessage(error, '댓글을 삭제하지 못했어요. 다시 시도해주세요.')
  }
}

function openDeleteConfirm(type, target = null) {
  deleteConfirm.value = {
    open: true,
    type,
    target,
  }
}

function closeDeleteConfirm() {
  if (isSaving.value) return
  deleteConfirm.value = {
    open: false,
    type: '',
    target: null,
  }
}

async function confirmDelete() {
  const { type, target } = deleteConfirm.value

  if (type === 'post') {
    await performPostDelete()
    return
  }

  if (type === 'comment') {
    await performCommentDelete(target)
    closeDeleteConfirm()
  }
}

async function toggleCommentLike(comment) {
  if (!isLoggedIn.value) {
    loginMessage.value = '로그인하면 추천할 수 있어요.'
    return
  }
  if (!post.value || comment.is_author) return

  try {
    const { data } = await communityService.toggleCommentLike(post.value.id, comment.id)
    comment.isLiked = Boolean(data.liked)
    comment.likes = Number(data.likes_count || 0)
    loginMessage.value = ''
  } catch (error) {
    loginMessage.value = getApiErrorMessage(error, '댓글을 추천하지 못했어요.')
  }
}

async function sharePost() {
  const url = window.location.href
  try {
    await navigator.clipboard.writeText(url)
  } catch {
    const textarea = document.createElement('textarea')
    textarea.value = url
    document.body.appendChild(textarea)
    textarea.select()
    document.execCommand('copy')
    document.body.removeChild(textarea)
  }

  shareMessage.value = '링크를 복사했어요.'
  window.setTimeout(() => {
    shareMessage.value = ''
  }, 1800)
}

function normalizePost(raw = {}) {
  return {
    id: raw.id,
    categoryLabel: getCategoryLabel(raw.category),
    title: raw.title || '제목 없음',
    content: raw.content || '',
    author: formatAuthor(raw),
    createdAt: formatDate(raw.created_at),
    views: raw.views_count || 0,
    likes: raw.likes_count || 0,
    comments: raw.comments_count || 0,
    isLiked: Boolean(raw.is_liked),
    is_author: Boolean(raw.is_author),
  }
}

function normalizeComment(raw = {}) {
  return {
    id: raw.id,
    author: formatAuthor(raw),
    createdAt: formatDate(raw.created_at),
    content: raw.content || '',
    likes: Number(raw.likes_count || 0),
    isLiked: Boolean(raw.is_liked),
    is_author: Boolean(raw.is_author),
    isEditing: false,
    editContent: '',
  }
}

function getCategoryLabel(category) {
  return {
    review: '카드 추천/후기',
    info: '혜택 꿀팁',
    general: '자유게시판',
    question: '질문답변',
  }[category] || '자유게시판'
}

function formatAuthor(item = {}) {
  if (item.username) return item.username
  return item.user_email ? item.user_email.split('@')[0] : '익명'
}

function formatDate(value) {
  if (!value) return ''
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value))
}

function formatNumber(value) {
  return Number(value || 0).toLocaleString('ko-KR')
}

watch(
  () => props.id,
  async () => {
    isEditingPost.value = false
    loginMessage.value = ''
    await loadPost()
  },
)

onMounted(async () => {
  await Promise.all([loadPost(), loadPopularPosts()])
})
</script>

<template>
  <section class="min-h-screen bg-[#faf8f7] px-5 py-8 text-[#111827] lg:px-8">
    <div v-if="isLoading" class="mx-auto max-w-[760px] rounded-lg border border-[#d7dbea] bg-white p-10 text-center shadow-sm">
      <p class="text-sm font-bold text-[#4d5870]">게시글을 불러오는 중입니다...</p>
    </div>

    <div v-else-if="errorMessage || !post" class="mx-auto max-w-[760px] rounded-lg border border-[#d7dbea] bg-white p-10 text-center shadow-sm">
      <h1 class="text-2xl font-extrabold">글을 찾지 못했어요.</h1>
      <p class="mt-3 text-sm text-[#4d5870]">{{ errorMessage }}</p>
      <button
        type="button"
        class="mt-6 inline-flex h-11 items-center justify-center rounded-md bg-[#001278] px-6 text-sm font-extrabold text-white"
        @click="router.push({ name: 'community' })"
      >
        목록으로 돌아가기
      </button>
    </div>

    <div v-else class="mx-auto grid max-w-[1180px] gap-8 lg:grid-cols-[1fr_300px]">
      <main class="grid gap-8">
        <article class="rounded-lg border border-[#e3e5ee] bg-white p-8 shadow-sm">
          <div class="flex flex-col gap-4 border-b border-[#ececf2] pb-7">
            <div class="flex items-center justify-between gap-4">
              <span class="text-sm font-extrabold text-[#001278]">{{ post.categoryLabel }}</span>
              <div v-if="isPostOwner" class="flex gap-2">
                <button class="rounded-md border border-[#d7dbea] px-3 py-1.5 text-xs font-bold text-[#4d5870]" @click="isEditingPost = true">
                  수정
                </button>
                <button class="rounded-md border border-red-200 px-3 py-1.5 text-xs font-bold text-red-600" @click="deletePost">
                  삭제
                </button>
              </div>
            </div>

            <template v-if="isEditingPost">
              <input
                v-model="editPostForm.title"
                class="rounded-md border border-[#d7dbea] px-4 py-3 text-2xl font-extrabold outline-none focus:border-[#001278]"
              />
              <textarea
                v-model="editPostForm.content"
                rows="8"
                class="rounded-md border border-[#d7dbea] px-4 py-3 text-sm leading-7 outline-none focus:border-[#001278]"
              />
              <div class="flex justify-end gap-2">
                <button class="h-10 rounded-md border border-[#d7dbea] px-4 text-sm font-bold" @click="isEditingPost = false">취소</button>
                <button class="h-10 rounded-md bg-[#001278] px-4 text-sm font-extrabold text-white" :disabled="isSaving" @click="savePostEdit">저장</button>
              </div>
            </template>

            <template v-else>
              <h1 class="text-3xl font-extrabold leading-tight">{{ post.title }}</h1>
              <div class="flex flex-wrap items-center gap-5 text-sm text-[#4d5870]">
                <span class="font-bold">{{ post.author }}</span>
                <span>{{ post.createdAt }}</span>
                <span class="ml-auto inline-flex items-center gap-1">조회 {{ formatNumber(post.views) }}</span>
                <span class="inline-flex items-center gap-1 text-red-600">추천 {{ formatNumber(post.likes) }}</span>
              </div>
            </template>
          </div>

          <div v-if="!isEditingPost" class="py-8">
            <div class="community-content text-base leading-8 text-[#30374d]" v-html="post.content"></div>

            <div class="mt-12 flex justify-center gap-5">
              <button
                v-if="!isPostOwner"
                type="button"
                class="inline-flex h-14 w-32 flex-col items-center justify-center rounded-md border text-sm font-bold transition"
                :class="
                  post.isLiked
                    ? 'border-[#001278] bg-[#eef1ff] text-[#001278] shadow-sm'
                    : 'border-[#d7dbea] text-[#4d5870] hover:border-[#001278] hover:text-[#001278]'
                "
                @click="togglePostLike"
              >
                <svg
                  class="h-5 w-5"
                  viewBox="0 0 20 20"
                  :fill="post.isLiked ? 'currentColor' : 'none'"
                  stroke="currentColor"
                  stroke-width="1.8"
                  aria-hidden="true"
                >
                  <path d="M10 17s-6.5-3.9-6.5-8.3A3.7 3.7 0 0 1 10 6.2a3.7 3.7 0 0 1 6.5 2.5C16.5 13.1 10 17 10 17Z" />
                </svg>
                <span class="mt-1">{{ post.isLiked ? '추천 취소' : '추천' }} {{ formatNumber(post.likes) }}</span>
              </button>
              <button
                type="button"
                class="inline-flex h-14 w-32 flex-col items-center justify-center rounded-md border border-[#d7dbea] text-sm font-bold text-[#4d5870] transition hover:border-[#001278] hover:text-[#001278]"
                @click="sharePost"
              >
                공유하기
              </button>
            </div>
            <p v-if="shareMessage" class="mt-4 text-center text-sm font-bold text-[#001278]">{{ shareMessage }}</p>
            <p v-if="loginMessage" class="mt-4 text-center text-sm font-bold text-[#001278]">{{ loginMessage }}</p>
          </div>
        </article>

        <section>
          <h2 class="text-lg font-extrabold">댓글 <span class="text-[#001278]">{{ visibleComments.length }}</span></h2>
          <div class="mt-4 rounded-lg border border-[#e3e5ee] bg-white p-5 shadow-sm">
            <textarea
              v-model="newComment"
              rows="4"
              class="w-full resize-none rounded-md border-0 text-sm leading-6 outline-none placeholder:text-[#8b93a7]"
              placeholder="댓글을 입력하세요."
            />
            <div class="mt-3 flex justify-end">
              <button class="h-9 rounded-md bg-[#001278] px-5 text-sm font-extrabold text-white" @click="addComment">등록하기</button>
            </div>
          </div>

          <div class="mt-6 grid gap-4">
            <article v-for="comment in visibleComments" :key="comment.id" class="rounded-lg border border-[#e3e5ee] bg-white p-5 shadow-sm">
              <div class="flex items-start justify-between gap-4">
                <div class="min-w-0 flex-1">
                  <div class="flex items-center gap-2 text-xs">
                    <span class="font-extrabold">{{ comment.author }}</span>
                    <span class="text-[#8b93a7]">{{ comment.createdAt }}</span>
                  </div>
                  <textarea
                    v-if="comment.isEditing"
                    v-model="comment.editContent"
                    rows="3"
                    class="mt-3 w-full rounded-md border border-[#d7dbea] px-3 py-2 text-sm outline-none focus:border-[#001278]"
                  />
                  <p v-else class="mt-3 text-sm leading-6 text-[#30374d]">{{ comment.content }}</p>
                </div>
                <div v-if="comment.is_author" class="flex shrink-0 items-center gap-2">
                  <button v-if="!comment.isEditing" class="text-xs font-bold text-[#4d5870]" @click="startCommentEdit(comment)">수정</button>
                  <button v-if="!comment.isEditing" class="text-xs font-bold text-red-600" @click="deleteComment(comment)">삭제</button>
                  <button v-if="comment.isEditing" class="text-xs font-bold text-[#001278]" @click="saveCommentEdit(comment)">저장</button>
                  <button v-if="comment.isEditing" class="text-xs font-bold text-[#4d5870]" @click="comment.isEditing = false">취소</button>
                </div>
                <button
                  v-else
                  class="inline-flex shrink-0 items-center gap-1 rounded-full px-2.5 py-1 text-xs font-bold transition"
                  :class="
                    comment.isLiked
                      ? 'bg-[#eef1ff] text-[#001278]'
                      : 'text-[#4d5870] hover:bg-[#f2f3f7] hover:text-[#001278]'
                  "
                  @click="toggleCommentLike(comment)"
                >
                  <svg
                    class="h-3.5 w-3.5"
                    viewBox="0 0 20 20"
                    :fill="comment.isLiked ? 'currentColor' : 'none'"
                    stroke="currentColor"
                    stroke-width="1.9"
                    aria-hidden="true"
                  >
                    <path d="M10 17s-6.5-3.9-6.5-8.3A3.7 3.7 0 0 1 10 6.2a3.7 3.7 0 0 1 6.5 2.5C16.5 13.1 10 17 10 17Z" />
                  </svg>
                  {{ formatNumber(comment.likes) }}
                </button>
              </div>
            </article>
            <p v-if="!visibleComments.length" class="rounded-lg border border-dashed border-[#d7dbea] bg-white p-8 text-center text-sm text-[#6b7280]">
              아직 댓글이 없어요.
            </p>
          </div>
        </section>
      </main>

      <aside class="grid content-start gap-7">
        <section class="rounded-lg border border-[#e3e5ee] bg-white p-5 shadow-sm">
          <h2 class="text-sm font-extrabold text-[#001278]">인기 게시글</h2>
          <div class="mt-5 grid gap-6">
            <RouterLink
              v-for="popular in popularPosts"
              :key="popular.id"
              :to="{ name: 'community-detail', params: { id: popular.id } }"
              class="block text-sm font-bold leading-6 text-[#111827] transition hover:text-[#001278]"
            >
              {{ popular.title }}
              <span class="mt-1 block text-xs font-medium text-[#8b93a7]">조회 {{ formatNumber(popular.views) }} · 추천 {{ formatNumber(popular.likes) }}</span>
            </RouterLink>
            <p v-if="!popularPosts.length" class="text-sm text-[#8b93a7]">아직 인기 글이 없어요.</p>
          </div>
        </section>

        <RouterLink
          :to="{ name: 'ai-recommendations' }"
          class="group overflow-hidden rounded-lg bg-[#001278] text-white shadow-lg transition hover:-translate-y-0.5 hover:shadow-xl"
          aria-label="AI 카드 추천 페이지로 이동"
        >
          <div class="flex min-h-[210px] flex-col justify-end bg-[radial-gradient(circle_at_25%_15%,rgba(255,255,255,0.35),transparent_16%),linear-gradient(145deg,#06145c_0%,#001278_55%,#0f2ccc_100%)] p-6">
            <p class="text-xs font-extrabold uppercase tracking-widest text-white/70">AI Recommendation</p>
            <h2 class="mt-3 text-2xl font-extrabold leading-tight">내 소비에 맞는<br />카드 추천 받기</h2>
            <span class="mt-4 inline-flex text-sm font-extrabold text-white/80 transition group-hover:text-white">
              AI 카드 추천으로 이동
            </span>
          </div>
        </RouterLink>
      </aside>
    </div>

    <div
      v-if="deleteConfirm.open"
      class="fixed inset-0 z-[100] flex items-center justify-center bg-black/45 px-4 py-6"
      role="dialog"
      aria-modal="true"
      aria-labelledby="delete-confirm-title"
      @click.self="closeDeleteConfirm"
    >
      <section class="w-full max-w-[420px] rounded-lg bg-white shadow-2xl">
        <div class="border-b border-[#ececf2] px-6 py-5">
          <p class="text-sm font-extrabold text-red-600">삭제 확인</p>
          <h2 id="delete-confirm-title" class="mt-1 text-xl font-extrabold text-[#111827]">
            {{ deleteConfirm.type === 'post' ? '게시글을 삭제할까요?' : '댓글을 삭제할까요?' }}
          </h2>
          <p class="mt-2 text-sm leading-6 text-[#4d5870]">
            삭제하면 되돌릴 수 없어요. 계속할까요?
          </p>
        </div>

        <div class="flex justify-end gap-3 px-6 py-5">
          <button
            type="button"
            class="inline-flex h-11 items-center justify-center rounded-md border border-[#d4d8e8] bg-white px-5 text-sm font-bold text-[#4d5870] transition hover:bg-[#f7f7fa]"
            :disabled="isSaving"
            @click="closeDeleteConfirm"
          >
            취소
          </button>
          <button
            type="button"
            class="inline-flex h-11 min-w-[104px] items-center justify-center rounded-md bg-red-600 px-5 text-sm font-extrabold text-white transition hover:bg-red-700 disabled:cursor-not-allowed disabled:bg-red-300"
            :disabled="isSaving"
            @click="confirmDelete"
          >
            {{ isSaving ? '삭제 중' : '삭제' }}
          </button>
        </div>
      </section>
    </div>
  </section>
</template>

<style scoped>
.community-content :deep(p) {
  margin: 0.5rem 0;
}

.community-content :deep(ol),
.community-content :deep(ul) {
  margin: 0.75rem 0;
  padding-left: 1.5rem;
}

.community-content :deep(ol) {
  list-style: decimal;
}

.community-content :deep(ul) {
  list-style: disc;
}

.community-content :deep(a) {
  color: #001278;
  font-weight: 700;
  text-decoration: underline;
}

.community-content :deep(img) {
  max-width: 100%;
  border-radius: 0.75rem;
}
</style>
