# CardFit 프론트엔드 시작 가이드

시작 전에 먼저 읽어주세용

## 목차 
( 컨트롤 + 쉬프트 + V : 이걸로 미리보기 들어가면 목차에서 클릭해서 링크 가능)

1. [시작 전 중요!!](#1-시작-전-중요)
2. [처음 한 번만 하는 설치](#2-처음-한-번만-하는-설치)
3. [개발 서버 켜기](#3-개발-서버-켜기)
4. [자주 쓰는 명령어](#4-자주-쓰는-명령어)
5. [지금 설치된 주요 기술](#5-지금-설치된-주요-기술)
6. [전체 구조 한눈에 보기](#6-전체-구조-한눈에-보기)
7. [페이지는 어디에 만들까?](#7-페이지는-어디에-만들까)
8. [주소와 페이지 연결은 어디?](#8-주소와-페이지-연결은-어디)
9. [컴포넌트는 어디?](#9-컴포넌트는-어디)
10. [Tailwind CSS 쓰는 법](#10-tailwind-css-쓰는-법)
11. [상태 관리는 어디에 있나?](#11-상태-관리는-어디에-있나)
12. [API 요청 코드는 어디?](#12-api-요청-코드는-어디)
13. [백엔드 주소 설정](#13-백엔드-주소-설정)
14. [로그인 토큰 구조](#14-로그인-토큰-구조)
15. [더미 데이터?](#15-더미-데이터)
16. [유틸 함수는 어디에 있나?](#16-유틸-함수는-어디에-있나)
17. [차트 컴포넌트](#17-차트-컴포넌트)
18. [예상 작업 순서](#18-예상-작업-순서)
19. [새 컴포넌트를 만들 때 규칙](#19-새-컴포넌트를-만들-때-규칙)
20. [화면 작업할 때 기본 흐름](#20-화면-작업할-때-기본-흐름)
21. [import 경로 이해하기](#21-import-경로-이해하기)
22. [자주 나는 에러](#22-자주-나는-에러)
23. [Git 작업 전 확인](#23-git-작업-전-확인)
24. [기억할 핵심](#24-기억할-핵심)

---

## 1. 시작 전 중요!!

프론트엔드 작업을 할 때는 대부분 터미널 위치가 `frontend` 폴더여야 함!!

---

## 2. 처음 한 번만 하는 설치

프론트엔드 폴더에서 아래 명령어를 실행

```bash
npm install
```

이 명령어는 `package.json`에 적힌 라이브러리들을 설치

이미 설치되어 있어도 다시 실행해도 괜찮음!
뭔가 이상할 때도 일단 `npm install` 다시 해보기

설치가 끝나면 `node_modules` 폴더가 생깁니당
이 폴더는 직접 수정 XXXX

---

## 3. 개발 서버 켜기

화면을 보면서 작업하려면 개발 서버를 켜야 함!!

프론트엔드 폴더에서 아래 명령어를 실행

```bash
npm run dev
```

성공하면~~

```text
http://localhost:5173
```

or

```text
http://127.0.0.1:5173
```

브라우저에서 이 주소로 들어가면 프론트엔드 화면을 볼 수 있음!

중요!!

개발 서버를 켠 터미널은 끄지 말고 그대로 둬야 함
코드를 수정하면 브라우저 화면이 자동으로 갱신됨

개발 서버를 끄고 싶으면 터미널에서 Ctrl + C !!

종료할지 물어보면 `Y`를 입력하고 Enter 누르면 됨!

---

## 4. 자주 쓰는 명령어

전부 프론트엔드 폴더에서 실행하면 됨

```bash
npm install
```

필요한 라이브러리 설치.

```bash
npm run dev
```

개발 서버 켜기.
화면 보면서 작업할 때 제일 많이 씀.

```bash
npm run build
```

최종 빌드가 되는지 확인.
에러가 있으면 여기서 잡히는 경우가 많음

```bash
npm run preview
```

빌드된 결과물 미리 보기.
보통 개발 중에는 많이 안 씀.

---

## 5. 지금 설치된 주요 기술

```text
Vue 3
Vite
Tailwind CSS
Vue Router
Pinia
Axios
Chart.js
vue-chartjs
```

각각의 역할

| 기술 | 역할 |
| --- | --- |
| Vue 3 | 화면을 컴포넌트 단위로 만드는 프론트엔드 프레임워크 |
| Vite | 개발 서버와 빌드를 빠르게 해주는 도구 |
| Tailwind CSS | class 이름으로 스타일을 빠르게 작성하는 CSS 도구 |
| Vue Router | 주소에 따라 다른 페이지를 보여주는 도구 |
| Pinia | 여러 컴포넌트가 공유하는 상태를 관리하는 도구 |
| Axios | 백엔드 API에 요청을 보내는 도구 |
| Chart.js | 차트를 그리는 라이브러리 |
| vue-chartjs | Chart.js를 Vue 컴포넌트처럼 쓰게 해주는 도구 |

---

## 6. 전체 구조 한눈에 보기


```text
frontend/
├─ package.json
├─ vite.config.js
├─ index.html
├─ .env.example
└─ src/
   ├─ main.js
   ├─ App.vue
   ├─ styles/
   ├─ router/
   ├─ stores/
   ├─ services/
   ├─ data/
   ├─ utils/
   ├─ pages/
   └─ components/
```

제일 많이 작업할 곳

```text
src/pages
src/components
```

---

## 7. 페이지는 어디에 만들까?

페이지 파일

```text
src/pages
```

현재 준비된 페이지

```text
HomePage.vue
CardSearchPage.vue
CardDetailPage.vue
CardComparePage.vue
SpendingReportPage.vue
ProfilePage.vue
LoginPage.vue
SignupPage.vue
```

페이지는 보통 "주소 하나에 대응되는 큰 화면"

예를 들어:

| 주소 | 페이지 파일 |
| --- | --- |
| `/` | `HomePage.vue` |
| `/cards` | `CardSearchPage.vue` |
| `/cards/:id` | `CardDetailPage.vue` |
| `/compare` | `CardComparePage.vue` |
| `/report` | `SpendingReportPage.vue` |
| `/profile` | `ProfilePage.vue` |
| `/login` | `LoginPage.vue` |
| `/signup` | `SignupPage.vue` |

---

## 8. 주소와 페이지 연결은 어디?

라우터 파일

```text
src/router/index.js
```

예를 들어 이런 코드가 있다면

```js
{ path: '/cards', name: 'cards', component: CardSearchPage }
```

뜻은 이럼

```text
/cards 주소로 들어오면 CardSearchPage.vue를 보여준다
```

새 페이지를 만들 때는 보통 아래 순서로

1. `src/pages`에 새 페이지 파일을 만들기
2. `src/router/index.js`에 import.
3. routes 배열에 주소를 추가.

---

## 9. 컴포넌트는 어디?

컴포넌트 파일

```text
src/components
```

컴포넌트는 페이지 안에서 재사용할 작은 조각

예를 들어 카드 목록 페이지를 만든다면 이렇게 나눌 수 있음

```text
CardSearchPage.vue
└─ CardFilterPanel.vue
└─ CardList.vue
   └─ CardItem.vue
```

현재 폴더는 기능별로

```text
components/
├─ common/
├─ home/
├─ cards/
├─ compare/
├─ report/
└─ auth/
```

각 폴더 역할

| 폴더 | 역할 |
| --- | --- |
| `common` | 버튼, 입력창, 모달처럼 여러 곳에서 쓰는 공통 컴포넌트 |
| `home` | 홈/추천 화면 전용 컴포넌트 |
| `cards` | 카드 검색/상세 관련 컴포넌트 |
| `compare` | 카드 비교 화면 관련 컴포넌트 |
| `report` | 소비 리포트/차트 관련 컴포넌트 |
| `auth` | 로그인/회원가입 관련 컴포넌트 |

---

## 10. Tailwind CSS 쓰는 법

Tailwind는 CSS 파일에 직접 `.button { ... }`을 많이 쓰는 대신, HTML의 `class`에 스타일을 적기

예를 들어:

```vue
<button class="rounded-lg bg-blue-600 px-4 py-2 text-white">
  확인
</button>
```

뜻

| class | 의미 |
| --- | --- |
| `rounded-lg` | 모서리를 둥글게 |
| `bg-blue-600` | 배경색 파란색 |
| `px-4` | 좌우 padding |
| `py-2` | 위아래 padding |
| `text-white` | 글자색 흰색 |

자주 쓰는 class:

| class | 의미 |
| --- | --- |
| `p-4` | 모든 방향 padding |
| `px-4` | 좌우 padding |
| `py-2` | 위아래 padding |
| `mt-4` | 위 margin |
| `mb-4` | 아래 margin |
| `flex` | flex layout |
| `grid` | grid layout |
| `gap-4` | 요소 사이 간격 |
| `rounded-lg` | 둥근 모서리 |
| `border` | 테두리 |
| `bg-white` | 흰 배경 |
| `text-sm` | 작은 글씨 |
| `font-semibold` | 살짝 굵은 글씨 |

---

## 11. 상태 관리는 어디에 있나?

상태 관리

```text
src/stores
```

상태는 "여러 컴포넌트가 같이 알아야 하는 데이터"입니다.

예를 들어:

- 로그인한 사용자 정보
- 카드 목록
- 비교함에 담긴 카드
- 사용자가 입력한 소비 패턴

현재 store는 이렇게 나뉘어 있습니다.

| 파일 | 역할 |
| --- | --- |
| `authStore.js` | 로그인, 회원가입, 로그아웃, 토큰, 사용자 정보 |
| `cardStore.js` | 카드 목록, 카드 상세, 검색 필터 |
| `compareStore.js` | 비교함 카드 추가/삭제 |
| `spendingStore.js` | 소비 입력값, 최근 설문, 리포트 데이터 |

예를 들어 컴포넌트에서 카드 store를 쓰려면:

```vue
<script setup>
import { useCardStore } from '../stores/cardStore'

const cardStore = useCardStore()
</script>

<template>
  <p>카드 개수: {{ cardStore.cards.length }}</p>
</template>
```

---

## 12. API 요청 코드는 어디?

API 요청 코드

```text
src/services
```

컴포넌트에서 직접 `axios.get(...)`을 쓰는 것보다, service 파일에 모아두기

예를 들어 카드 목록 API는 `cardService.js`에 있음

```js
fetchCards(params = {}) {
  return api.get('/api/cards/', { params })
}
```

이렇게 해두면 나중에 백엔드 주소나 응답 형태가 조금 바뀌어도 service 쪽만 고치면 됨

---

## 13. 백엔드 주소 설정

API 기본 주소는 환경 변수로 설정.

예시 파일:

```text
.env.example
```

실제로 사용할 때는 이 파일을 복사해서 `.env` 파일을 만들면 됨

```bash
cp .env.example .env
```

`.env` 안에는 이런 값이 들어감

```text
VITE_API_BASE_URL=http://localhost:8000
```

뜻 : 
  프론트엔드는 API 요청을 보낼 때 http://localhost:8000 을 기본 주소로 사용


Django 서버가 `http://localhost:8000`에서 실행되면 이 값 그대로 쓰면 됨

환경 변수를 바꾼 뒤에는 개발 서버를 껐다가 다시 켜야 함

```bash
Ctrl + C
npm run dev
```

---

## 14. 로그인 토큰 구조

JWT 토큰은 브라우저의 `localStorage`에 저장하도록 준비되어 있음.

저장 키

```text
cardfit_access_token
cardfit_refresh_token
```

`src/services/api.js`에서 Axios 요청을 보낼 때 access token이 있으면 자동으로 헤더에 붙음

```text
Authorization: Bearer <access_token>
```

그래서 로그인 이후에는 API 요청마다 직접 토큰을 붙이지 않아도 됨

---

## 15. 더미 데이터?

더미 데이터

```text
src/data
```

현재 준비된 파일:

| 파일 | 역할 |
| --- | --- |
| `cardData.js` | 카드 더미 데이터 |
| `benefitData.js` | 혜택 카테고리/타입 데이터 |
| `spendingCategoryData.js` | 소비 카테고리 데이터 |

백엔드 API가 아직 완전히 연결되지 않아도 이 데이터로 화면을 먼저 만들 수 있음

---

## 16. 유틸 함수는 어디에 있나?

유틸 함수

```text
src/utils
```

현재 준비된 파일:

| 파일 | 역할 |
| --- | --- |
| `formatCurrency.js` | 금액을 원화 형식으로 바꿔줌 |
| `calculateBenefit.js` | 카드 혜택 예상 금액 계산 |

예를 들어:

```js
formatCurrency(30000)
```

결과:

```text
₩30,000
```

---

## 17. 차트 컴포넌트

차트 컴포넌트

```text
src/components/report
```

준비된 파일:

```text
SpendingPieChart.vue
SpendingBarChart.vue
```

이 파일들은 `vue-chartjs`와 `Chart.js`를 연결해둔 최소 예시

나중에 소비 리포트 페이지에서 `chartData`만 만들어서 넘기면 됨

예시:

```vue
<SpendingPieChart :chart-data="chartData" />
```

---

## 18. 예상 작업 순서

1. `npm run dev`로 개발 서버를 켜기
2. `src/pages/HomePage.vue`를 열기
3. 아주 작은 문구 하나를 수정 해보기
4. 브라우저에서 바로 바뀌는지 확인
5. `components/common`에서 버튼/입력창 공통 스타일을 잡기
6. 홈 화면의 소비 입력 폼을 만들기
7. 더미 카드 데이터로 추천 결과 목록을 보여주기
8. 카드 검색 페이지를 만들기
9. 카드 상세 페이지를 만들기
10. 비교 페이지와 리포트 페이지를 만들기
11. 마지막에 로그인/회원가입과 백엔드 API를 연결.

처음부터 모든 페이지를 완성하려고 하지 말고, 한 페이지씩 작게 확인하면서 가기

---

## 19. 새 컴포넌트를 만들 때 규칙

파일 이름은 PascalCase로

좋은 예:

```text
CardItem.vue
SpendingSurveyForm.vue
LoginForm.vue
```

피하는 예:

```text
card-item.vue
spending_survey_form.vue
loginform.vue
```

컴포넌트 위치도 기능에 맞춰 넣기

예를 들어 카드 필터 컴포넌트는:

```text
src/components/cards/CardFilterPanel.vue
```

로그인 폼은:

```text
src/components/auth/LoginForm.vue
```

---

## 20. 화면 작업할 때 기본 흐름

예를 들어 카드 검색 페이지를 만든다고 하면:

1. `src/pages/CardSearchPage.vue`를 연다.
2. 필요한 store를 가져온다.
3. 필요한 컴포넌트를 import 한다.
4. `<template>`에서 화면 구조를 만든다.
5. Tailwind class로 간격과 색을 잡는다.
6. 브라우저에서 확인한다.
7. 너무 길어지면 일부를 `components/cards`로 분리한다.

예시:

```vue
<script setup>
import { useCardStore } from '../stores/cardStore'

const cardStore = useCardStore()
</script>

<template>
  <section class="p-6">
    <h1 class="text-2xl font-semibold">카드 검색</h1>

    <p class="mt-2 text-sm text-slate-600">
      총 {{ cardStore.cards.length }}개의 카드가 있습니다.
    </p>
  </section>
</template>
```

---

## 21. import 경로 이해하기

파일에서 다른 파일을 가져올 때 `import`

예를 들어 `src/pages/CardSearchPage.vue`에서 `cardStore.js`를 가져오려면:

```js
import { useCardStore } from '../stores/cardStore'
```

여기서 `..`은 한 폴더 위로 올라간다는 뜻

현재 파일:

```text
src/pages/CardSearchPage.vue
```

한 폴더 위:

```text
src
```

그 다음:

```text
stores/cardStore.js
```

그래서 전체가:

```text
../stores/cardStore
```

---

## 22. 자주 나는 에러

### `npm` 명령어가 안 먹는 경우

Node.js가 설치되어 있는지 확인

```bash
node --version
npm --version
```

버전이 나오면 설치되어 있는 것

### `package.json`을 찾을 수 없다는 에러

터미널 위치가 잘못된 경우가 많음

프론트엔드 폴더로 이동

```bash
cd frontend
```

이미 `frontend` 안에 있다면 한 번 현재 위치를 확인

```bash
pwd
```

### 화면이 안 바뀌는 경우

개발 서버가 켜져 있는지 확인

```bash
npm run dev
```

또는 브라우저 새로고침을 해보기

### 환경 변수를 바꿨는데 반영이 안 되는 경우

개발 서버를 껐다가 다시 켜야 함

```bash
Ctrl + C
npm run dev
```

### import 에러가 나는 경우

파일 이름과 경로를 확인

Windows에서는 대소문자 차이를 덜 엄격하게 보는 경우가 있지만, 배포 환경에서는 문제가 될 수 있음

파일명은 정확히 맞춰 쓰는 습관이 좋음

---

## 23. Git 작업 전 확인

작업한 파일 목록을 보려면 프로젝트 루트에서 실행.

```bash
git status
```

주의할 점:

- `node_modules`는 Git에 올리지 않습니다.
- `dist`는 보통 Git에 올리지 않습니다.
- `.env`는 개인 설정이므로 Git에 올리지 않습니다.
- `.env.example`은 공유용이라 Git에 올려도 됩니다.

---

## 24. 기억할 핵심

- 터미널은 보통 `frontend` 폴더에서 실행.
- 화면 하나는 `src/pages`에 만듦.
- 재사용 조각은 `src/components`에 만듦.
- 여러 곳에서 같이 쓰는 데이터는 `src/stores`에 둠.
- API 요청은 `src/services`에 둠
- 임시 데이터는 `src/data`에 둠.
- 반복되는 계산/포맷 함수는 `src/utils`에 둠.
- 화면을 크게 한 번에 만들지 말고, 작게 만들고 브라우저에서 계속 확인.
