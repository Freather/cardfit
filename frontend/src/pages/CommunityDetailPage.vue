<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

import { useAuthStore } from '../stores/authStore'

const props = defineProps({
  id: {
    type: [String, Number],
    default: 1,
  },
})

const router = useRouter()
const authStore = useAuthStore()

const posts = [
  {
    id: 1,
    categoryLabel: '삼성카드',
    title: '삼성카드 taptap O 실제 사용기 - 스타벅스 50%의 위엄',
    author: '카드고수김씨',
    ownerEmail: 'demo@cardfit.local',
    createdAt: '2024.03.25 21:45',
    views: 1242,
    likes: 48,
    content:
      '안녕하세요. 오늘은 사회초년생부터 베테랑 직장인까지 모두에게 사랑받는 삼성카드 taptap O의 6개월 실사용 후기를 가져왔습니다. 특히 카페를 좋아하시는 분들이라면 주목하셔야 할 혜택이 많습니다.',
  },
  {
    id: 2,
    categoryLabel: '혜택 꿀팁',
    title: '공항 라운지 이용 가능한 체크카드 총정리 (2024년 최신)',
    author: '여행전문가',
    ownerEmail: 'travel@cardfit.local',
    createdAt: '2024.03.25 18:20',
    views: 3501,
    likes: 156,
    content: '공항 라운지 혜택은 전월 실적과 이용 횟수 조건을 같이 봐야 합니다. 자주 여행하는 분들을 위해 핵심 카드만 골라봤습니다.',
  },
  {
    id: 3,
    categoryLabel: '자유게시판',
    title: '이번 달 카드값 실화인가요... 다들 절약 어떻게 하시나요?',
    author: '절약왕김두리',
    ownerEmail: 'save@cardfit.local',
    createdAt: '2024.03.25 15:10',
    views: 856,
    likes: 12,
    content: '고정비를 줄이는 게 생각보다 어렵네요. 카드 혜택을 잘 쓰면서도 지출을 줄이는 방법이 궁금합니다.',
  },
  {
    id: 4,
    categoryLabel: '질문답변',
    title: '사회초년생 첫 신용카드 추천 부탁드려요! (연봉 3,500 기준)',
    author: '신입사원A',
    ownerEmail: 'newbie@cardfit.local',
    createdAt: '2024.03.25 12:05',
    views: 2110,
    likes: 22,
    content: '첫 신용카드를 만들려고 합니다. 연회비가 너무 비싸지 않고 생활비 혜택이 좋은 카드가 있을까요?',
  },
  {
    id: 5,
    categoryLabel: '카드 추천/후기',
    title: '삼성 iD On 카드의 숨겨진 혜택 찾아냈습니다.',
    author: '데이터마니아',
    ownerEmail: 'data@cardfit.local',
    createdAt: '2024.03.25 09:30',
    views: 5820,
    likes: 102,
    content: '삼성 iD On 카드는 기본 혜택 외에도 사용 패턴에 따라 꽤 괜찮은 구간이 있습니다. 월별 소비가 일정한 분들에게 잘 맞습니다.',
  },
]

const popularPosts = [
  { id: 1, title: '무실적 카드의 끝판왕, 현대 제로 실사용 비교' },
  { id: 2, title: '혜택 구조가 좋은 추천 카드 TOP 5' },
  { id: 4, title: '대학생 첫 신용카드 어떤 게 좋을까요?' },
]

const currentPost = computed(() => {
  return posts.find((post) => String(post.id) === String(props.id)) || posts[0]
})
const isLoggedIn = computed(() => authStore.isAuthenticated)
const currentUserEmail = computed(() => authStore.user?.email || null)
const isPostOwner = computed(() => currentPost.value.ownerEmail === currentUserEmail.value)
const postLikes = ref(currentPost.value.likes)
const didLikePost = ref(false)
const isEditingPost = ref(false)
const postDeleted = ref(false)
const shareMessage = ref('')
const loginMessage = ref('')
const editPostForm = ref({
  title: currentPost.value.title,
  content: currentPost.value.content,
})

watch(
  () => props.id,
  () => {
    postLikes.value = currentPost.value.likes
    didLikePost.value = false
    isEditingPost.value = false
    postDeleted.value = false
    editPostForm.value = {
      title: currentPost.value.title,
      content: currentPost.value.content,
    }
  },
)

const comments = ref([
  {
    id: 1,
    author: '카드초보아빠',
    ownerEmail: 'dad@cardfit.local',
    createdAt: '14시간 전',
    content: '스타 50% 진짜 대단하네요. 전월 실적 제외가 쉬운 편인가요?',
    likes: 4,
    didLike: false,
    isEditing: false,
  },
  {
    id: 2,
    author: '혜택브레이커',
    ownerEmail: 'demo@cardfit.local',
    createdAt: '3시간 전',
    content: '공과금 실적 포함 안되는 카드 많던데 이건 어디서 확인해야겠네요. 좋은 후기 감사합니다!',
    likes: 12,
    didLike: false,
    isEditing: false,
  },
])
const newComment = ref('')

const visibleComments = computed(() => comments.value.filter((comment) => !comment.deleted))

function formatNumber(value) {
  return Number(value).toLocaleString('ko-KR')
}

function isCommentOwner(comment) {
  return isLoggedIn.value && comment.ownerEmail === currentUserEmail.value
}

function savePostEdit() {
  currentPost.value.title = editPostForm.value.title.trim() || currentPost.value.title
  currentPost.value.content = editPostForm.value.content.trim() || currentPost.value.content
  isEditingPost.value = false
}

function deletePost() {
  postDeleted.value = true
}

function togglePostLike() {
  if (!isLoggedIn.value) {
    loginMessage.value = '로그인 후 추천할 수 있습니다.'
    return
  }
  if (isPostOwner.value) return
  didLikePost.value = !didLikePost.value
  postLikes.value += didLikePost.value ? 1 : -1
  loginMessage.value = ''
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

  shareMessage.value = '링크가 복사되었습니다.'
  window.setTimeout(() => {
    shareMessage.value = ''
  }, 1800)
}

function addComment() {
  if (!isLoggedIn.value) {
    loginMessage.value = '로그인 후 댓글을 작성할 수 있습니다.'
    return
  }

  const content = newComment.value.trim()
  if (!content) return

  comments.value = [
    {
      id: Date.now(),
      author: authStore.user?.username || '나',
      ownerEmail: currentUserEmail.value,
      createdAt: '방금 전',
      content,
      likes: 0,
      didLike: false,
      isEditing: false,
    },
    ...comments.value,
  ]
  newComment.value = ''
  loginMessage.value = ''
}

function startCommentEdit(comment) {
  comment.editContent = comment.content
  comment.isEditing = true
}

function saveCommentEdit(comment) {
  const content = comment.editContent?.trim()
  if (content) comment.content = content
  comment.isEditing = false
}

function deleteComment(comment) {
  comment.deleted = true
}

function toggleCommentLike(comment) {
  if (!isLoggedIn.value) {
    loginMessage.value = '로그인 후 추천할 수 있습니다.'
    return
  }
  if (isCommentOwner(comment)) return
  comment.didLike = !comment.didLike
  comment.likes += comment.didLike ? 1 : -1
  loginMessage.value = ''
}
</script>

<template>
  <section class="min-h-screen bg-[#faf8f7] px-5 py-8 text-[#111827] lg:px-8">
    <div v-if="postDeleted" class="mx-auto max-w-[760px] rounded-lg border border-[#d7dbea] bg-white p-10 text-center shadow-sm">
      <h1 class="text-2xl font-extrabold">삭제된 게시글입니다.</h1>
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
              <span class="text-sm font-extrabold text-[#001278]">{{ currentPost.categoryLabel }}</span>
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
                rows="5"
                class="rounded-md border border-[#d7dbea] px-4 py-3 text-sm leading-7 outline-none focus:border-[#001278]"
              />
              <div class="flex justify-end gap-2">
                <button class="h-10 rounded-md border border-[#d7dbea] px-4 text-sm font-bold" @click="isEditingPost = false">취소</button>
                <button class="h-10 rounded-md bg-[#001278] px-4 text-sm font-extrabold text-white" @click="savePostEdit">저장</button>
              </div>
            </template>

            <template v-else>
              <h1 class="text-3xl font-extrabold leading-tight">{{ currentPost.title }}</h1>
              <div class="flex flex-wrap items-center gap-5 text-sm text-[#4d5870]">
                <span class="font-bold">{{ currentPost.author }}</span>
                <span>{{ currentPost.createdAt }}</span>
                <span class="ml-auto inline-flex items-center gap-1">조회 {{ formatNumber(currentPost.views) }}</span>
                <span class="inline-flex items-center gap-1 text-red-600">좋아요 {{ postLikes }}</span>
              </div>
            </template>
          </div>

          <div v-if="!isEditingPost" class="py-8">
            <p class="text-base leading-8 text-[#30374d]">{{ currentPost.content }}</p>

            <div class="mx-auto mt-8 flex h-[220px] max-w-[390px] flex-col justify-between rounded-lg bg-[#2634aa] p-7 text-white shadow-xl">
              <div class="flex items-center justify-between">
                <span class="text-lg font-extrabold">Samsung Card</span>
                <span class="rounded bg-white/20 px-2 py-1 text-xs font-bold">Card</span>
              </div>
              <div>
                <p class="text-xl font-extrabold">taptap O</p>
                <p class="mt-3 text-xs text-white/70">4518 **** **** 8274</p>
              </div>
            </div>

            <h2 class="mt-9 text-lg font-extrabold">주요 혜택 정리 (Takeaway)</h2>
            <ul class="mt-4 grid gap-3 rounded-md bg-[#f6f3f2] p-5 text-sm text-[#30374d]">
              <li class="flex gap-3"><span class="font-extrabold text-[#001278]">✓</span> 스타벅스 50% 할인 또는 커피 전문점 30% 할인</li>
              <li class="flex gap-3"><span class="font-extrabold text-[#001278]">✓</span> 대중교통, 택시 10% 할인</li>
              <li class="flex gap-3"><span class="font-extrabold text-[#001278]">✓</span> 쇼핑 7% 할인 및 1% 적립</li>
              <li class="flex gap-3"><span class="font-extrabold text-[#001278]">✓</span> CGV, 롯데시네마 5,000원 할인</li>
            </ul>

            <p class="mt-8 text-base leading-8 text-[#30374d]">
              제가 가장 강력하게 추천드리는 이유는 실사용 구간이 넓다는 점입니다. 매일 쓰는 카페와 교통 지출이 많은 분이라면
              체감 혜택이 꽤 크게 느껴질 거예요. 본인 소비 패턴에 맞게 전월 실적 조건을 함께 확인해보세요.
            </p>

            <div class="mt-12 flex justify-center gap-5">
              <button
                v-if="!isPostOwner"
                type="button"
                class="inline-flex h-14 w-32 flex-col items-center justify-center rounded-md border text-sm font-bold transition"
                :class="
                  didLikePost
                    ? 'border-[#001278] bg-[#eef1ff] text-[#001278] shadow-sm'
                    : 'border-[#d7dbea] text-[#4d5870] hover:border-[#001278] hover:text-[#001278]'
                "
                @click="togglePostLike"
              >
                <svg
                  class="h-5 w-5"
                  viewBox="0 0 20 20"
                  :fill="didLikePost ? 'currentColor' : 'none'"
                  stroke="currentColor"
                  stroke-width="1.8"
                  aria-hidden="true"
                >
                  <path d="M10 17s-6.5-3.9-6.5-8.3A3.7 3.7 0 0 1 10 6.2a3.7 3.7 0 0 1 6.5 2.5C16.5 13.1 10 17 10 17Z" />
                </svg>
                <span class="mt-1">{{ didLikePost ? '추천 취소' : '추천' }}</span>
              </button>
              <button
                type="button"
                class="inline-flex h-14 w-32 flex-col items-center justify-center rounded-md border border-[#d7dbea] text-sm font-bold text-[#4d5870] transition hover:border-[#001278] hover:text-[#001278]"
                @click="sharePost"
              >
                ⤴
                <span class="mt-1">공유하기</span>
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
              placeholder="카드 사용기에 대한 궁금한 점을 남겨보세요."
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
                <div class="flex shrink-0 items-center gap-2">
                  <template v-if="isCommentOwner(comment)">
                    <button v-if="!comment.isEditing" class="text-xs font-bold text-[#4d5870]" @click="startCommentEdit(comment)">수정</button>
                    <button v-if="!comment.isEditing" class="text-xs font-bold text-red-600" @click="deleteComment(comment)">삭제</button>
                    <button v-if="comment.isEditing" class="text-xs font-bold text-[#001278]" @click="saveCommentEdit(comment)">저장</button>
                    <button v-if="comment.isEditing" class="text-xs font-bold text-[#4d5870]" @click="comment.isEditing = false">취소</button>
                  </template>
                  <button
                    v-else
                    class="inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-bold transition"
                    :class="
                      comment.didLike
                        ? 'bg-[#eef1ff] text-[#001278]'
                        : 'text-[#4d5870] hover:bg-[#f2f3f7] hover:text-[#001278]'
                    "
                    @click="toggleCommentLike(comment)"
                  >
                    <svg
                      class="h-3.5 w-3.5"
                      viewBox="0 0 20 20"
                      :fill="comment.didLike ? 'currentColor' : 'none'"
                      stroke="currentColor"
                      stroke-width="1.9"
                      aria-hidden="true"
                    >
                      <path d="M10 17s-6.5-3.9-6.5-8.3A3.7 3.7 0 0 1 10 6.2a3.7 3.7 0 0 1 6.5 2.5C16.5 13.1 10 17 10 17Z" />
                    </svg>
                    {{ comment.likes }}
                  </button>
                </div>
              </div>
            </article>
          </div>
        </section>
      </main>

      <aside class="grid content-start gap-7">
        <section class="rounded-lg border border-[#e3e5ee] bg-white p-5 shadow-sm">
          <h2 class="text-sm font-extrabold text-[#001278]">인기 게시글</h2>
          <div class="mt-5 grid gap-6">
            <RouterLink
              v-for="post in popularPosts"
              :key="post.id"
              :to="{ name: 'community-detail', params: { id: post.id } }"
              class="block text-sm font-bold leading-6 text-[#111827] transition hover:text-[#001278]"
            >
              {{ post.title }}
              <span class="mt-1 block text-xs font-medium text-[#8b93a7]">조회 1.2k · 추천 34</span>
            </RouterLink>
          </div>
        </section>

        <RouterLink
          :to="{ name: 'card-detail', params: { id: 2 } }"
          class="group overflow-hidden rounded-lg bg-[#001278] text-white shadow-lg transition hover:-translate-y-0.5 hover:shadow-xl"
          aria-label="삼성 iD On 카드 상세 페이지로 이동"
        >
          <div class="flex min-h-[210px] flex-col justify-end bg-[radial-gradient(circle_at_25%_15%,rgba(255,255,255,0.35),transparent_16%),linear-gradient(145deg,#06145c_0%,#001278_55%,#0f2ccc_100%)] p-6">
            <p class="text-xs font-extrabold uppercase tracking-widest text-white/70">Ad Recommendation</p>
            <h2 class="mt-3 text-2xl font-extrabold leading-tight">삼성 iD On 카드<br />혜택 총정리</h2>
            <span class="mt-4 inline-flex text-sm font-extrabold text-white/80 transition group-hover:text-white">
              카드 상세 보기
            </span>
          </div>
        </RouterLink>

        <section class="rounded-lg border border-[#e3e5ee] bg-white p-5 shadow-sm">
          <p class="text-sm font-extrabold text-[#001278]">카드 추천 챗봇</p>
          <p class="mt-2 text-sm leading-6 text-[#4d5870]">나에게 맞는 카드를 AI가 분석해드립니다.</p>
          <RouterLink
            :to="{ name: 'ai-recommendations' }"
            class="mt-5 inline-flex h-10 w-full items-center justify-center rounded-md bg-[#001278] text-sm font-extrabold text-white transition hover:bg-[#1428a0]"
          >
            분석하러가기
          </RouterLink>
        </section>
      </aside>
    </div>
  </section>
</template>
