<script setup>
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router'

const activeTab = ref('all')
const keyword = ref('')
const currentPage = ref(1)
const postsPerPage = 5

const tabs = [
  { id: 'all', label: '전체' },
  { id: 'recommend', label: '카드 추천/후기' },
  { id: 'benefit', label: '혜택 꿀팁' },
  { id: 'free', label: '자유게시판' },
  { id: 'question', label: '질문답변' },
]

const posts = [
  {
    id: 1,
    category: 'recommend',
    categoryLabel: '카드 추천/후기',
    time: '어제 21:45',
    title: '삼성카드 taptap O 실제 사용기 - 스타벅스 50%의 위엄',
    author: '카드고수김씨',
    views: 1242,
    likes: 48,
    hot: true,
  },
  {
    id: 2,
    category: 'benefit',
    categoryLabel: '혜택 꿀팁',
    time: '어제 18:20',
    title: '공항 라운지 이용 가능한 체크카드 총정리 (2024년 최신)',
    author: '여행전문가',
    views: 3501,
    likes: 156,
    hot: true,
  },
  {
    id: 3,
    category: 'free',
    categoryLabel: '자유게시판',
    time: '어제 15:10',
    title: '이번 달 카드값 실화인가요... 다들 절약 어떻게 하시나요?',
    author: '절약왕김두리',
    views: 856,
    likes: 12,
  },
  {
    id: 4,
    category: 'question',
    categoryLabel: '질문답변',
    time: '어제 12:05',
    title: '사회초년생 첫 신용카드 추천 부탁드려요! (연봉 3,500 기준)',
    author: '신입사원A',
    views: 2110,
    likes: 22,
    hot: true,
  },
  {
    id: 5,
    category: 'recommend',
    categoryLabel: '카드 추천/후기',
    time: '어제 09:30',
    title: '삼성 iD On 카드의 숨겨진 혜택 찾아냈습니다.',
    author: '데이터마니아',
    views: 5820,
    likes: 102,
    hot: true,
  },
]

const popularPosts = [
  { id: 1, title: '2024년 상반기 알짜 신용카드 TOP 10' },
  { id: 2, title: '혜택이랑 전월 실적 구조 간단 정리하는 카드들' },
  { id: 5, title: '삼성카드 포인트 현금화 하는 방법' },
  { id: 4, title: '혜택별로 사용 가능한 카드 리스트' },
  { id: 3, title: '무실적 카드 괜찮은 무엇이 있을까요?' },
]

const filteredPosts = computed(() => {
  const normalizedKeyword = keyword.value.trim().toLowerCase()

  return posts.filter((post) => {
    const matchesTab = activeTab.value === 'all' || post.category === activeTab.value
    const matchesKeyword =
      !normalizedKeyword ||
      post.title.toLowerCase().includes(normalizedKeyword) ||
      post.author.toLowerCase().includes(normalizedKeyword)

    return matchesTab && matchesKeyword
  })
})

const totalPages = computed(() => Math.ceil(filteredPosts.value.length / postsPerPage))
const visiblePages = computed(() => Array.from({ length: totalPages.value }, (_, index) => index + 1))
const paginatedPosts = computed(() => {
  const start = (currentPage.value - 1) * postsPerPage
  return filteredPosts.value.slice(start, start + postsPerPage)
})

function formatNumber(value) {
  return Number(value).toLocaleString('ko-KR')
}

function resetPage() {
  currentPage.value = 1
}

function goToPage(page) {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
}
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
            스마트한 카드 생활을 공유하고<br />
            나에게 꼭 맞는 혜택을 찾아보세요.
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
              @input="resetPage"
            />
          </label>

          <RouterLink
            :to="{ name: 'community-write' }"
            class="inline-flex h-12 items-center justify-center gap-2 rounded-md bg-[#001278] px-8 text-sm font-extrabold text-white transition hover:bg-[#1428a0]"
          >
            <svg class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path d="M14.7 2.3a1 1 0 0 1 1.4 0l1.6 1.6a1 1 0 0 1 0 1.4L7.3 15.7 3 17l1.3-4.3L14.7 2.3Z" />
            </svg>
            글쓰기
          </RouterLink>
        </div>
      </div>

      <div class="mt-10 grid gap-7 lg:grid-cols-[1fr_270px]">
        <main>
          <div class="flex gap-8 border-b border-[#d7dbea]">
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
              @click="activeTab = tab.id; resetPage()"
            >
              {{ tab.label }}
            </button>
          </div>

          <div class="overflow-hidden rounded-b-lg border border-t-0 border-[#d7dbea] bg-white">
            <article
              v-for="post in paginatedPosts"
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

              <div class="flex w-24 shrink-0 flex-col items-end justify-center gap-3 text-xs text-[#4d5870]">
                <span class="inline-flex items-center gap-1">
                  <svg class="h-4 w-4" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true">
                    <path d="M2.5 10s2.6-5 7.5-5 7.5 5 7.5 5-2.6 5-7.5 5-7.5-5-7.5-5Z" />
                    <circle cx="10" cy="10" r="2" />
                  </svg>
                  {{ formatNumber(post.views) }}
                </span>
                <span class="inline-flex items-center gap-1 font-extrabold text-[#001278]">
                  <svg class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path d="M10 17s-6.5-3.9-6.5-8.3A3.7 3.7 0 0 1 10 6.2a3.7 3.7 0 0 1 6.5 2.5C16.5 13.1 10 17 10 17Z" />
                  </svg>
                  {{ post.likes }}
                </span>
              </div>
            </article>

            <div v-if="!filteredPosts.length" class="px-5 py-16 text-center text-sm font-semibold text-[#6b7280]">
              검색 결과가 없습니다.
            </div>
          </div>

          <div v-if="totalPages > 0" class="mt-10 flex justify-center gap-3">
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
              <svg class="h-4 w-4 text-[#001278]" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                <path d="M4 14 8 10l3 3 5-7" />
                <path d="M13 6h3v3" />
              </svg>
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
                  <p class="mt-1 text-xs text-[#8b93a7]">댓글 {{ 20 - index * 2 }}개</p>
                </div>
              </li>
            </ol>
          </section>

          <RouterLink
            :to="{ name: 'card-detail', params: { id: 2 } }"
            class="group overflow-hidden rounded-lg bg-[#001278] text-white shadow-lg transition hover:-translate-y-0.5 hover:shadow-xl"
            aria-label="삼성 iD On 카드 상세 페이지로 이동"
          >
            <div class="flex min-h-[260px] flex-col justify-end bg-[radial-gradient(circle_at_25%_15%,rgba(255,255,255,0.35),transparent_16%),linear-gradient(145deg,#06145c_0%,#001278_55%,#0f2ccc_100%)] p-6">
              <p class="text-xs font-extrabold uppercase tracking-widest text-white/70">Featured Card</p>
              <h2 class="mt-3 text-3xl font-extrabold leading-tight">
                이번엔 삼성카드<br />
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
