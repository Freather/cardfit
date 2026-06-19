<template>
  <div class="min-h-screen bg-gray-100 py-10 px-4 md:px-20">
    <div class="max-w-6xl mx-auto space-y-12">
      
      <div v-if="isLoggedIn" class="bg-blue-900 text-white p-8 rounded-2xl shadow-md flex flex-col md:flex-row justify-between items-start md:items-center">
        <div>
          <h1 class="text-2xl font-bold mb-2">{{ username }}님의 소비 분석이 완료되었어요 🎉</h1>
          <p class="text-blue-200 text-sm">한 달 소비 패턴을 기반으로 가장 잘 맞는 카드 3개를 골랐어요.</p>
        </div>
        <button class="mt-4 md:mt-0 bg-white text-blue-950 font-semibold px-5 py-2.5 rounded-lg text-sm shadow hover:bg-gray-100 transition">
          리포트 자세히 보기
        </button>
      </div>

      <div v-else class="bg-gray-800 text-white p-8 rounded-2xl shadow-md flex flex-col md:flex-row justify-between items-start md:items-center">
        <div>
          <h1 class="text-2xl font-bold mb-2">나에게 딱 맞는 카드를 찾고 싶으신가요? 🤔</h1>
          <p class="text-gray-400 text-sm">정확한 소비 패턴 분석을 원하시면 로그인을 진행해 주세요.</p>
        </div>
        <button 
          @click="goToLogin" 
          class="mt-4 md:mt-0 bg-blue-600 text-white font-semibold px-5 py-2.5 rounded-lg text-sm shadow hover:bg-blue-700 transition"
        >
          로그인하러 가기
        </button>
      </div>

      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-1">
          {{ isLoggedIn ? "AI 추천 카드 TOP 3" : "삼성 카드 추천 라인업" }}
        </h2>
        <p class="text-sm text-gray-500 mb-6">
          {{ isLoggedIn ? "내 소비 패턴 기반 예상 혜택 순" : "다양한 혜택의 삼성 카드를 만나보세요" }}
        </p>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div 
            v-for="(card, index) in cards" 
            :key="card.id" 
            class="bg-white border rounded-2xl p-6 shadow-sm flex flex-col justify-between"
            :class="{ 'border-blue-500 ring-2 ring-blue-500/20': isLoggedIn && index === 0, 'border-gray-200': !(isLoggedIn && index === 0) }"
          >
            <div>
              <div class="w-full h-40 bg-gray-100 rounded-xl flex items-center justify-center text-xs text-gray-400 mb-5 relative">
                카드 이미지
                <span v-if="isLoggedIn && index === 0" class="absolute top-3 left-3 bg-blue-600 text-white text-xs font-bold px-2 py-1 rounded-md">
                  추천 1위
                </span>
              </div>

              <h3 class="text-lg font-bold text-gray-900 mb-1">{{ card.name }}</h3>
              <p class="text-xs text-gray-400 mb-6">{{ card.desc }}</p>
              
              <div v-if="isLoggedIn" class="border-t pt-4 mb-6 space-y-1">
                <span class="text-xs text-gray-500">예상 월 혜택</span>
                <div class="text-xl font-extrabold text-green-600">{{ card.benefit }}</div>
                <div class="text-xs text-gray-400">{{ card.annual }}</div>
              </div>
            </div>

            <button :class="isLoggedIn && index === 0 
              ? 'w-full py-2.5 rounded-xl font-medium text-sm bg-blue-600 text-white hover:bg-blue-700 transition' 
              : 'w-full py-2.5 rounded-xl font-medium text-sm bg-white text-blue-600 border border-blue-600 hover:bg-blue-50 transition'">
              자세히 보기
            </button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
// import samsungCardData from '../data/samsungCards.json';

const router = useRouter();

// 1. 처음에는 비어있거나 기본값으로 세팅
const isLoggedIn = ref(false); 
const username = ref('게스트');
const cards = ref([]);

const goToLogin = () => {
  router.push({ name: 'login' }); 
};

// 2. 컴포넌트가 화면에 마운트(로딩)될 때 자동으로 로그인 상태 체크
onMounted(() => {
  // 브라우저 저장소에서 'token'과 'username'이 있는지 확인합니다.
  // (로그인 API 성공 시 저장소에 'token'과 'username'을 세팅해 두었다고 가정합니다.)
  const token = localStorage.getItem('token');
  const savedUsername = localStorage.getItem('username');

  if (token) {
    // 토큰이 존재하면 자동으로 로그인 상태를 true로 전환!
    isLoggedIn.value = true;
    username.value = savedUsername || '사용자';
  } else {
    // 토큰이 없으면 로그아웃 상태
    isLoggedIn.value = false;
  }

  // 카드 데이터 로드 (추후 조건에 따라 다르게 서빙 가능)
  // cards.value = samsungCardData;
  cards.value = [
    { id: 1, name: "삼성 iD ON 카드", desc: "쇼핑·주유·통신 특화", benefit: "₩12,000", annual: "연간 약 ₩144,000" },
    { id: 2, name: "삼성 taptap O 카드", desc: "외식·배달 특화", benefit: "₩9,500", annual: "연간 약 ₩114,000" },
    { id: 3, name: "삼성 momo 카드", desc: "교통·편의점 특화", benefit: "₩7,200", annual: "연간 약 ₩86,400" }
  ];
});
</script>