<template>
  <section class="overflow-hidden rounded-2xl bg-gradient-to-br from-[#050b1a] to-[#0a1433] text-white shadow-[0_20px_60px_rgba(0,10,30,0.4)] border border-white/5 relative">

    <div class="grid gap-8 px-6 py-8 md:grid-cols-[1fr_420px] md:px-10 md:py-12">
      <!-- Left: text + chips -->
      <div class="flex flex-col justify-start gap-6 z-10">
        <div>
          <p class="text-sm font-black uppercase tracking-[0.25em] text-[#00e5ff]">Today's Pick</p>
          <h1 class="mt-4 text-4xl font-black leading-tight md:text-5xl tracking-tight">
            마음 가는 카드로<br />
            <span class="bg-gradient-to-r from-white to-white/60 bg-clip-text text-transparent">오늘의 운세를</span>
          </h1>
          <p class="mt-5 text-sm leading-relaxed text-white/60 md:text-base">
            눈앞에 펼쳐진 세 장의 카드 중 하나를 선택해보세요.
          </p>
        </div>

        <div class="grid gap-4 sm:grid-cols-3">
          <div
            v-for="item in fortuneChips"
            :key="item.label"
            class="rounded-xl border border-white/10 bg-white/5 px-5 py-4"
          >
            <p class="text-[11px] font-black uppercase tracking-widest text-[#00e5ff]/70">{{ item.label }}</p>
            <p class="mt-1.5 text-sm font-extrabold text-white/90">{{ item.value }}</p>
          </div>
        </div>

        <!-- Detailed Fortune Box under the chips -->
        <div
          v-if="hasDrawn && isFlipped"
          class="rounded-[18px] border border-white/10 bg-white/5 px-5 py-4 text-white fortune-reveal flex flex-col justify-between"
        >
          <div>
            <p class="text-sm font-black text-[#00e5ff]">{{ fortune.title }}</p>
            <p class="mt-2 text-xs leading-relaxed text-white/70">{{ fortune.detail }}</p>
          </div>
          <div class="mt-4">
            <RouterLink
              v-if="drawnCard"
              :to="{ name: 'card-detail', params: { id: drawnCard.id } }"
              class="inline-flex h-9 items-center justify-center rounded-xl border border-white/20 bg-white/5 px-4 text-xs font-extrabold text-white hover:bg-white hover:text-[#0a1128] transition-colors"
            >
              해당 카드 상세보기
            </RouterLink>
          </div>
        </div>
      </div>

      <!-- Right: card fan + fortune -->
      <div class="flex flex-col items-center pt-6" style="perspective: 1200px;">

        <p
          class="text-xs font-bold text-white/50 tracking-widest uppercase transition-all duration-500 ease-in-out"
          :style="{
            opacity: isCardsSpread && selectedIndex === null ? 1 : 0,
            height: selectedIndex === null ? '1rem' : '0px',
            marginBottom: selectedIndex === null ? '2.5rem' : '0px',
            overflow: 'hidden'
          }"
        >
          원하는 카드를 선택하세요
        </p>

        <!-- 320px shared column -->
        <div
          class="w-[320px] flex flex-col items-center gap-4"
        >

          <!-- Cards fan area -->
          <div class="relative w-full h-[188px]">
            <div
              v-for="(card, index) in walletCards"
              :key="card?.id ?? index"
              class="card-outer absolute top-0 left-0 w-full h-full"
              :style="outerStyle(index)"
            >
              <button
                class="card-btn relative w-full h-full focus:outline-none"
                :class="{ 'card-btn--hovered': hoveredIndex === index && selectedIndex === null }"
                :style="innerStyle(index)"
                :disabled="!isCardsSpread || selectedIndex !== null || !card"
                @mouseenter="onHoverEnter(index)"
                @mouseleave="onHoverLeave"
                @click="drawCard(index)"
              >
                <!-- Back face -->
                <div class="card-face card-back absolute inset-0 rounded-[18px] bg-gradient-to-br from-[#1e2a5e] to-[#0c1433] border border-white/10 flex items-center justify-center overflow-hidden">
                  <div class="absolute inset-0 opacity-20" style="background-image: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px); background-size: 18px 18px;"></div>
                  <div class="absolute top-4 left-4 w-8 h-5 rounded-md bg-gradient-to-r from-[#d4af37] to-[#aa7c11]"></div>
                  <!-- shimmer stripe -->
                  <div class="card-shimmer absolute inset-0 pointer-events-none overflow-hidden rounded-[18px]">
                    <div class="shimmer-line absolute top-0 bottom-0 w-1/3 bg-gradient-to-r from-transparent via-white/12 to-transparent -translate-x-full"></div>
                  </div>
                  <span class="relative z-10 text-lg font-black tracking-[0.3em] text-white/80 uppercase">CardFit</span>
                </div>

                <!-- Front face -->
                <div
                  class="card-face card-front absolute inset-0 rounded-[18px] bg-[#f8fafc] overflow-hidden"
                  style="transform: rotateY(180deg);"
                >
                  <img
                    v-if="drawnCard?.image_url"
                    :src="drawnCard.image_url"
                    :alt="drawnCard?.name"
                    class="w-full h-full object-contain p-3"
                  />
                  <div v-else class="w-full h-full bg-gradient-to-br from-[#001278] to-[#3152ff] p-5 flex flex-col justify-between text-white">
                    <span class="text-xs font-black uppercase tracking-widest text-white/60">CardFit</span>
                    <strong class="text-lg leading-tight">{{ drawnCard?.name ?? '오늘의 카드' }}</strong>
                  </div>
                  <div v-if="isFlipped" class="absolute inset-0 pointer-events-none bg-gradient-to-r from-transparent via-white/40 to-transparent animate-sweep"></div>
                </div>
              </button>
            </div>
          </div>

          <!-- Fortune result box (same 320px width) -->
          <div
            v-if="hasDrawn && isFlipped"
            class="w-full rounded-[18px] border border-white/20 bg-white/10 backdrop-blur-xl px-4 py-3 text-white fortune-reveal"
          >
            <span class="inline-flex h-6 items-center rounded-full bg-[#00e5ff]/20 px-3 text-[11px] font-black text-[#00e5ff] ring-1 ring-[#00e5ff]/30">
              {{ primaryBenefitLabel }} 운세
            </span>
            <h2 class="mt-2 text-sm font-black leading-snug">{{ drawnCard?.name }}</h2>
            <p class="mt-1 text-xs leading-relaxed text-white/70">{{ fortune.summary }}</p>
            <button
              @click="resetDraw"
              class="mt-3 w-full h-9 rounded-xl bg-gradient-to-r from-[#00e5ff] to-[#00bfff] text-[#0a1128] font-black text-xs hover:opacity-90 transition-opacity"
            >
              다른 카드 뽑기
            </button>
          </div>

        </div>
      </div>
    </div>

  </section>
</template>

<script setup>
import { computed, ref, watch, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { getRepresentativeBenefit } from '../../utils/representativeBenefit'

const props = defineProps({
  cards: { type: Array, default: () => [] },
})

// ── state ──────────────────────────────────────────────
const isCardsSpread  = ref(false)
const isFlipped      = ref(false)
const hasDrawn       = ref(false)
const isDrawing      = ref(false)
const selectedIndex  = ref(null)
const selectedCardId = ref(null)
const hoveredIndex   = ref(null)
const walletCards    = ref([])

// ── derived ────────────────────────────────────────────
const drawnCard = computed(() => {
  if (selectedCardId.value === null) return null
  return walletCards.value.find(c => String(c?.id) === String(selectedCardId.value)) ?? null
})

const primaryBenefit = computed(() => getRepresentativeBenefit(drawnCard.value))

const categoryLabels = {
  food: '식비', transport: '교통', transportation: '교통', fuel: '주유',
  shopping: '쇼핑', entertainment: '문화/여가', communication: '통신',
  health: '의료/건강', travel: '여행', point: '포인트', other: '생활',
}
const primaryBenefitLabel = computed(() => categoryLabels[primaryBenefit.value?.benefit_category] ?? '생활')

const fortune = computed(() => {
  const card = drawnCard.value
  const label = primaryBenefitLabel.value
  const benefitType = { discount: '할인', cashback: '캐시백', point: '포인트 적립', mileage: '마일리지' }[primaryBenefit.value?.benefit_type] ?? '혜택'
  const tone = getFortuneTone(primaryBenefit.value?.benefit_category)
  if (!card) return { title: '카드를 뽑으면 운세가 열립니다.', summary: '아직 카드가 숨어 있어요.', detail: '' }
  return {
    title: `${tone.title} ${label}운이 들어왔어요.`,
    summary: tone.summary,
    detail: `${card.name}이(가) 오늘의 카드예요. ${label} 관련 ${benefitType} 기운이 강하게 들어와 있으니 ${tone.detail}`,
  }
})

const fortuneChips = computed(() => {
  if (!hasDrawn.value) return [
    { label: '상태', value: '카드 뽑을 준비 완료' },
    { label: '할 일', value: '카드 한 장 고르기' },
    { label: '결과', value: '운세는 숨겨져 있어요' },
  ]
  return [
    { label: '키워드', value: primaryBenefitLabel.value },
    { label: '카드 등급', value: getCardMood(drawnCard.value) },
    { label: '오늘의 운', value: getDailyTip(primaryBenefit.value?.benefit_category) },
  ]
})

// ── transform helpers ───────────────────────────────────
function outerStyle(index) {
  const base = { transition: 'transform 0.8s cubic-bezier(0.25,1,0.25,1), opacity 0.8s ease' }

  if (!isCardsSpread.value) {
    return { ...base, transform: 'translate(0,24px) scale(0.95)', opacity: 0, zIndex: 10 }
  }

  if (selectedIndex.value === null) {
    const tx = index === 0 ? '-105px' : index === 2 ? '105px' : '0px'
    const ty = index === 1 ? '0px' : '14px'
    return { ...base, transform: `translate(${tx}, ${ty})`, opacity: 1, zIndex: 20 }
  }

  if (selectedIndex.value === index) {
    return { ...base, transform: 'translate(0, -14px) scale(1.04)', opacity: 1, zIndex: 50 }
  }

  return { ...base, transform: 'translate(0, 50px) scale(0.9)', opacity: 0, zIndex: 10 }
}

function innerStyle(index) {
  const base = {
    transformStyle: 'preserve-3d',
    transition: 'transform 0.35s cubic-bezier(0.25,1,0.25,1)',
  }

  if (selectedIndex.value === index) {
    return { ...base, transform: isFlipped.value ? 'rotateY(180deg)' : 'rotateY(0deg)' }
  }

  if (isCardsSpread.value && selectedIndex.value === null) {
    const rot = index === 0 ? '-14deg' : index === 2 ? '14deg' : '0deg'
    const lift = hoveredIndex.value === index ? ' translateY(-12px) scale(1.05)' : ''
    return { ...base, transform: `rotateZ(${rot})${lift}` }
  }

  return { ...base, transform: 'rotateZ(0deg)' }
}

// ── interaction ─────────────────────────────────────────
function onHoverEnter(index) {
  if (selectedIndex.value !== null || !isCardsSpread.value) return
  hoveredIndex.value = index
}
function onHoverLeave() {
  hoveredIndex.value = null
}

function drawCard(index) {
  const card = walletCards.value[index]
  if (!card || isDrawing.value || !isCardsSpread.value) return

  selectedIndex.value  = index
  selectedCardId.value = card.id
  hasDrawn.value       = false
  isDrawing.value      = true
  isFlipped.value      = false
  hoveredIndex.value   = null

  setTimeout(() => {
    isFlipped.value = true
    setTimeout(() => {
      hasDrawn.value  = true
      isDrawing.value = false
    }, 700)
  }, 600)
}

function resetDraw() {
  hasDrawn.value       = false
  isFlipped.value      = false
  isDrawing.value      = false
  isCardsSpread.value  = false
  selectedIndex.value  = null
  selectedCardId.value = null
  hoveredIndex.value   = null

  setTimeout(() => {
    walletCards.value = shuffle(props.cards).slice(0, 3)
    setTimeout(() => { isCardsSpread.value = true }, 300)
  }, 400)
}

function shuffle(arr) {
  return [...arr].sort(() => Math.random() - 0.5)
}

function init() {
  if (props.cards.length === 0) return
  walletCards.value = shuffle(props.cards).slice(0, 3)
  setTimeout(() => { isCardsSpread.value = true }, 400)
}

onMounted(init)

watch(() => props.cards.length, (len) => {
  if (len > 0 && walletCards.value.length === 0) init()
})

// ── fortune helpers ──────────────────────────────────────
function getFortuneTone(cat) {
  return ({
    food:           { title: '입맛 좋은 날.',        summary: '맛있는 약속이 생기기 쉬운 하루예요.',               detail: '밥값이나 카페 결제에서 괜히 기분 좋은 절약감을 챙기기 좋습니다.' },
    shopping:       { title: '장바구니가 부르는 날.', summary: '미뤄둔 쇼핑을 비교해보기 좋은 타이밍입니다.',       detail: '충동구매만 피하면 필요한 물건을 꽤 똑똑하게 살 수 있습니다.' },
    transport:      { title: '이동운이 가벼운 날.',   summary: '여기저기 움직여도 리듬이 크게 무너지지 않는 하루예요.', detail: '교통비처럼 매일 새는 돈을 작게 붙잡는 감각이 좋습니다.' },
    transportation: { title: '이동운이 가벼운 날.',   summary: '여기저기 움직여도 리듬이 크게 무너지지 않는 하루예요.', detail: '교통비처럼 매일 새는 돈을 작게 붙잡는 감각이 좋습니다.' },
    fuel:           { title: '주유 타이밍이 보이는 날.', summary: '차를 쓰는 일정이 있다면 비용 감각이 좋아지는 하루예요.', detail: '주유나 차량 관련 지출을 한 번 더 확인하면 만족도가 올라갑니다.' },
    communication:  { title: '고정비 정리운이 온 날.', summary: '통신비나 자동납부를 살펴보기 좋은 하루입니다.',     detail: '매달 나가는 돈을 정리하는 쪽으로 운이 붙습니다.' },
    entertainment:  { title: '놀거리 운이 열린 날.',  summary: '영화, OTT, 문화생활 쪽에서 작은 즐거움이 생기기 쉽습니다.', detail: '예약 전 혜택 조건만 보면 즐길 때 마음이 더 가벼워집니다.' },
    health:         { title: '컨디션 점검운이 있는 날.', summary: '건강 관련 지출을 미루지 말라는 신호에 가깝습니다.', detail: '병원, 약국, 건강관리 비용을 챙기면 괜히 든든합니다.' },
    travel:         { title: '멀리 보는 운이 있는 날.', summary: '여행이나 예약 계획을 세우기 좋은 흐름입니다.',    detail: '일정과 혜택 조건을 같이 보면 더 기분 좋은 선택이 됩니다.' },
    point:          { title: '쌓이는 운이 있는 날.',  summary: '작은 포인트도 놓치지 않으면 나중에 꽤 든든해집니다.', detail: '오늘은 할인보다 적립 흐름을 챙기는 쪽이 잘 맞습니다.' },
  })[cat] ?? { title: '생활운이 무난한 날.', summary: '크게 튀진 않지만 새는 돈을 막기 좋은 하루예요.', detail: '조건을 한 번 확인하고 쓰면 일상 지출에서 작은 이득을 챙길 수 있습니다.' }
}

function getCardMood(card) {
  const fee = Number(card?.annual_fee ?? 0)
  if (!fee) return '가볍게 시작'
  if (fee <= 15000) return '실속 챙김'
  if (fee <= 50000) return '균형 잡힌 선택'
  return '프리미엄 기운'
}

function getDailyTip(cat) {
  return { food: '맛집 결제운', shopping: '장바구니운', transport: '이동운', transportation: '이동운',
    fuel: '주유운', communication: '고정비운', entertainment: '놀거리운',
    health: '컨디션운', travel: '여행운', point: '적립운' }[cat] ?? '생활운'
}
</script>

<style scoped>
/* 3D face setup */
.card-btn { transform-style: preserve-3d; }
.card-face { backface-visibility: hidden; -webkit-backface-visibility: hidden; }

/* Hover glow on back face via CSS — no JS transform conflicts */
.card-btn--hovered .card-back {
  box-shadow: 0 0 0 1.5px rgba(0,229,255,0.55), 0 12px 36px rgba(0,0,0,0.5), inset 0 0 28px rgba(0,229,255,0.06);
  border-color: rgba(0,229,255,0.35);
  transition: box-shadow 0.25s ease, border-color 0.25s ease;
}
.card-back {
  transition: box-shadow 0.25s ease, border-color 0.25s ease;
  box-shadow: 0 8px 24px rgba(0,0,0,0.45);
}

/* Shimmer on hover */
.card-btn--hovered .shimmer-line {
  animation: shimmer 0.65s ease-in-out forwards;
}
@keyframes shimmer {
  from { transform: translateX(-100%) skewX(-10deg); }
  to   { transform: translateX(350%)  skewX(-10deg); }
}

/* Flip sweep */
.animate-sweep {
  animation: sweep 1s ease-in-out forwards;
}
@keyframes sweep {
  from { transform: translateX(-150%) skewX(-20deg); }
  to   { transform: translateX(250%)  skewX(-20deg); }
}

/* Fortune box entrance */
.fortune-reveal {
  animation: fadeUp 0.45s ease forwards;
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0);    }
}
</style>
