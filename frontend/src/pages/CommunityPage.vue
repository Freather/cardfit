<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'

import { getApiErrorMessage } from '../services/api'
import { communityService } from '../services/communityService'

const activeTab = ref('all')
const keyword = ref('')
const currentPage = ref(1)
const postsPerPage = 5
const posts = ref([])
const popularPosts = ref([])
const totalItems = ref(0)
const isLoading = ref(false)
const errorMessage = ref('')

const tabs = [
  { id: 'all', label: '전체', apiCategory: '' },
  { id: 'recommend', label: '카드 추천/후기', apiCategory: 'review' },
  { id: 'benefit', label: '혜택 꿀팁', apiCategory: 'info' },
  { id: 'free', label: '자유게시판', apiCategory: 'general' },
  { id: 'question', label: '질문답변', apiCategory: 'question' },
]

const totalPages = computed(() => Math.max(1, Math.ceil(totalItems.value / postsPerPage)))
const visiblePages = computed(() => Array.from({ length: totalPages.value }, (_, index) => index + 1))

async function loadPosts() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const active = tabs.find((tab) => tab.id === activeTab.value)
    const params = {
      page: currentPage.value,
      page_size: postsPerPage,
    }

    if (active?.apiCategory) params.category = active.apiCategory
    if (keyword.value.trim()) params.search = keyword.value.trim()

    const { data } = await communityService.fetchPosts(params)
    const results = Array.isArray(data) ? data : data.results || []
    posts.value = results.map(normalizePost)
    totalItems.value = Number(data.count ?? results.length)
  } catch (error) {
    posts.value = []
    totalItems.value = 0
    errorMessage.value = getApiErrorMessage(error, '글 목록을 불러오지 못했어요.')
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

async function resetPage() {
  currentPage.value = 1
  await loadPosts()
}

async function goToPage(page) {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  await loadPosts()
}

function normalizePost(post = {}) {
  const category = toUiCategory(post.category)

  return {
    id: post.id,
    category,
    categoryLabel: getCategoryLabel(category),
    time: formatDate(post.created_at),
    title: post.title || '제목 없음',
    author: formatAuthor(post),
    views: post.views_count || 0,
    likes: post.likes_count || 0,
    comments: post.comments_count || 0,
    hot: Number(post.likes_count || 0) >= 10 || Number(post.views_count || 0) >= 100,
  }
}

function toUiCategory(category) {
  return {
    review: 'recommend',
    info: 'benefit',
    general: 'free',
    question: 'question',
  }[category] || 'free'
}

function getCategoryLabel(category) {
  return tabs.find((tab) => tab.id === category)?.label || '자유게시판'
}

function formatAuthor(post = {}) {
  if (post.username) return post.username
  return post.user_email ? post.user_email.split('@')[0] : '익명'
}

function formatDate(value) {
  if (!value) return ''
  return new Intl.DateTimeFormat('ko-KR', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value))
}

function formatNumber(value) {
  return Number(value || 0).toLocaleString('ko-KR')
}

watch(activeTab, resetPage)

onMounted(async () => {
  await Promise.all([loadPosts(), loadPopularPosts()])
})
</script>

<template>
  <section class="min-h-screen bg-[#faf8f7] text-[#111827]">
    <div class="mx-auto max-w-[1180px] px-5 py-10 lg:px-8">
      <div class="text-xs font-semibold text-[#4d5870]">
        <span class="text-[#001278]">Community</span>
      </div>

      <div class="mt-5 flex flex-col gap-6 border-b border-[#d7dbea] pb-10 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <h1 class="text-4xl font-extrabold tracking-tight text-[#001278]">커뮤니티</h1>
          <p class="mt-4 max-w-md text-base leading-7 text-[#4d5870]">
            카드 사용 경험과 혜택 정보를 공유하고<br />
            나에게 맞는 카드 생활 팁을 찾아보세요.
          </p>
        </div>

        <div class="flex flex-col gap-3 sm:flex-row sm:items-center">
          <label class="flex h-12 w-full items-center rounded-md border border-[#cfd4e5] bg-white px-4 sm:w-[330px]">
            <svg class="h-4 w-4 text-[#6b7280]" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
              <circle cx="9" cy="9" r="5" />
              <path d="m13 13 4 4" />
            </svg>
            <input
              v-model="keyword"
              type="search"
              class="ml-3 h-full w-full bg-transparent text-sm outline-none placeholder:text-[#8b93a7]"
              placeholder="게시글 제목, 내용 검색"
              @keyup.enter="resetPage"
            />
          </label>
          <button
            type="button"
            class="h-12 rounded-md border border-[#cfd4e5] bg-white px-4 text-sm font-bold text-[#001278] transition hover:bg-[#eef1ff]"
            @click="resetPage"
          >
            검색
          </button>

          <RouterLink
            :to="{ name: 'community-write' }"
            class="inline-flex h-12 items-center justify-center gap-2 rounded-md bg-[#001278] px-8 text-sm font-extrabold text-white transition hover:bg-[#1428a0]"
          >
            글쓰기
          </RouterLink>
        </div>
      </div>

      <div class="mt-10 grid gap-7 lg:grid-cols-[1fr_270px]">
        <main>
          <div class="flex flex-wrap gap-8 border-b border-[#d7dbea]">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              type="button"
              class="border-b-2 px-1 pb-4 text-sm font-bold transition"
              :class="
                activeTab === tab.id
                  ? 'border-[#001278] text-[#001278]'
                  : 'border-transparent text-[#6b7280] hover:text-[#001278]'
              "
              @click="activeTab = tab.id"
            >
              {{ tab.label }}
            </button>
          </div>

          <div class="overflow-hidden rounded-b-lg border border-t-0 border-[#d7dbea] bg-white">
            <div v-if="isLoading" class="px-5 py-16 text-center text-sm font-semibold text-[#6b7280]">
              게시글을 불러오는 중입니다...
            </div>
            <div v-else-if="errorMessage" class="px-5 py-16 text-center text-sm font-semibold text-red-600">
              {{ errorMessage }}
            </div>
            <article
              v-for="post in posts"
              v-else
              :key="post.id"
              class="flex gap-5 border-b border-[#e4e7f0] px-5 py-5 last:border-b-0"
            >
              <div class="min-w-0 flex-1">
                <div class="flex flex-wrap items-center gap-2">
                  <span
                    class="rounded-sm px-2 py-1 text-[11px] font-extrabold"
                    :class="post.hot ? 'bg-[#eef1ff] text-[#001278]' : 'bg-[#f2f3f7] text-[#4d5870]'"
                  >
                    {{ post.categoryLabel }}
                  </span>
                  <span class="text-xs font-medium text-[#6b7280]">{{ post.time }}</span>
                </div>
                <RouterLink
                  :to="{ name: 'community-detail', params: { id: post.id } }"
                  class="mt-2 block truncate text-lg font-extrabold text-[#111827] transition hover:text-[#001278]"
                >
                  {{ post.title }}
                </RouterLink>
                <div class="mt-3 flex items-center gap-2 text-sm text-[#4d5870]">
                  <span class="inline-flex h-5 w-5 items-center justify-center rounded-full bg-[#e8ded1] text-[10px] font-bold text-[#6d4b2f]">
                    {{ post.author.slice(0, 1) }}
                  </span>
                  {{ post.author }}
                </div>
              </div>

              <div class="flex w-28 shrink-0 flex-col items-end justify-center gap-3 text-xs text-[#4d5870]">
                <span>조회 {{ formatNumber(post.views) }}</span>
                <span class="font-extrabold text-[#001278]">추천 {{ formatNumber(post.likes) }}</span>
                <span>댓글 {{ formatNumber(post.comments) }}</span>
              </div>
            </article>

            <div v-if="!isLoading && !errorMessage && !posts.length" class="px-5 py-16 text-center text-sm font-semibold text-[#6b7280]">
              검색 결과가 없어요.
            </div>
          </div>

          <div v-if="totalItems > postsPerPage" class="mt-10 flex justify-center gap-3">
            <button
              type="button"
              class="h-11 w-11 rounded-md border border-[#d7dbea] bg-white text-sm font-extrabold text-[#4d5870] transition hover:border-[#001278] hover:text-[#001278] disabled:cursor-not-allowed disabled:opacity-40"
              :disabled="currentPage === 1"
              @click="goToPage(currentPage - 1)"
            >
              &lt;
            </button>
            <button
              v-for="page in visiblePages"
              :key="page"
              type="button"
              class="h-11 min-w-11 rounded-md border px-4 text-sm font-extrabold transition"
              :class="
                page === currentPage
                  ? 'border-[#001278] bg-[#001278] text-white'
                  : 'border-[#d7dbea] bg-white text-[#111827] hover:border-[#001278] hover:text-[#001278]'
              "
              @click="goToPage(page)"
            >
              {{ page }}
            </button>
            <button
              type="button"
              class="h-11 w-11 rounded-md border border-[#d7dbea] bg-white text-sm font-extrabold text-[#4d5870] transition hover:border-[#001278] hover:text-[#001278] disabled:cursor-not-allowed disabled:opacity-40"
              :disabled="currentPage === totalPages"
              @click="goToPage(currentPage + 1)"
            >
              &gt;
            </button>
          </div>
        </main>

        <aside class="grid content-start gap-7">
          <section class="rounded-lg border border-[#d7dbea] bg-white p-5">
            <div class="flex items-center justify-between">
              <h2 class="text-lg font-extrabold">인기 게시글</h2>
            </div>
            <ol class="mt-5 grid gap-4">
              <li v-for="(post, index) in popularPosts" :key="post.id" class="flex gap-3">
                <span class="text-base font-extrabold text-[#001278]">{{ index + 1 }}</span>
                <div>
                  <RouterLink
                    :to="{ name: 'community-detail', params: { id: post.id } }"
                    class="text-sm font-bold leading-5 transition hover:text-[#001278]"
                  >
                    {{ post.title }}
                  </RouterLink>
                  <p class="mt-1 text-xs text-[#8b93a7]">추천 {{ formatNumber(post.likes) }}개</p>
                </div>
              </li>
              <li v-if="!popularPosts.length" class="text-sm text-[#8b93a7]">아직 인기 글이 없어요.</li>
            </ol>
          </section>

          <RouterLink
            :to="{ name: 'card-detail', params: { id: 2 } }"
            class="group overflow-hidden rounded-lg bg-[#001278] text-white shadow-lg transition hover:-translate-y-0.5 hover:shadow-xl"
          >
            <div class="flex min-h-[260px] flex-col justify-end bg-[radial-gradient(circle_at_25%_15%,rgba(255,255,255,0.35),transparent_16%),linear-gradient(145deg,#06145c_0%,#001278_55%,#0f2ccc_100%)] p-6">
              <p class="text-xs font-extrabold uppercase tracking-widest text-white/70">Featured Card</p>
              <h2 class="mt-3 text-3xl font-extrabold leading-tight">
                삼성카드<br />
                iD 혜택 총정리
              </h2>
              <span class="mt-6 inline-flex h-10 w-28 items-center justify-center rounded-md bg-white text-sm font-extrabold text-[#001278] transition group-hover:bg-[#eef1ff]">
                자세히 보기
              </span>
            </div>
          </RouterLink>
        </aside>
      </div>
    </div>
  </section>
</template>
