# CardFit Frontend

Vue 3, Vite, Tailwind CSS 기반 CardFit 프론트엔드입니다. 현재는 화면 구현 전 밑작업 단계이며, 라우팅, 상태관리, API 계층, 더미 데이터, 유틸, 기본 컴포넌트 구조만 준비되어 있습니다.

## 실행 방법

```bash
npm install
npm run dev
```

개발 서버 기본 주소는 Vite 출력값을 확인하세요. 일반적으로 `http://localhost:5173`입니다.

## 빌드

```bash
npm run build
```

## 환경 변수

`.env.example`을 참고해 `.env`를 만들 수 있습니다.

```bash
VITE_API_BASE_URL=http://localhost:8000
```

## 폴더 구조

```text
src/
├─ main.js
├─ App.vue
├─ assets/
│  └─ images/
├─ styles/
│  └─ main.css
├─ router/
│  └─ index.js
├─ stores/
│  ├─ authStore.js
│  ├─ cardStore.js
│  ├─ compareStore.js
│  └─ spendingStore.js
├─ services/
│  ├─ api.js
│  ├─ authService.js
│  ├─ cardService.js
│  ├─ spendingService.js
│  └─ aiService.js
├─ data/
│  ├─ cardData.js
│  ├─ benefitData.js
│  └─ spendingCategoryData.js
├─ utils/
│  ├─ formatCurrency.js
│  └─ calculateBenefit.js
├─ pages/
└─ components/
```

## 준비된 기능

- Vue Router 라우트: `/`, `/cards`, `/cards/:id`, `/compare`, `/report`, `/profile`, `/login`, `/signup`
- Pinia store: 인증, 카드, 비교함, 소비 패턴
- Axios 인스턴스: `Authorization: Bearer <access_token>` 자동 주입
- JWT 저장 키: `cardfit_access_token`, `cardfit_refresh_token`
- Tailwind CSS: `src/styles/main.css`에서 바로 사용 가능
- Chart.js 예시 컴포넌트: `SpendingPieChart.vue`, `SpendingBarChart.vue`

## 개발 메모

- 화면은 의도적으로 최소 placeholder만 들어 있습니다.
- API 서버가 없을 때도 카드 목록과 일부 리포트 상태는 더미 데이터로 개발할 수 있습니다.
- DRF API 연동은 `src/services` 계층에서 교체하거나 확장하세요.
