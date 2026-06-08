# CardFit 백엔드 개발 가이드

> Samsung Card 기반 AI 카드 추천 서비스 — Django REST Framework 백엔드

---

## 목차

1. [기술 스택](#1-기술-스택)
2. [프로젝트 구조](#2-프로젝트-구조)
3. [로컬 환경 세팅](#3-로컬-환경-세팅)
4. [환경 변수](#4-환경-변수)
5. [앱 아키텍처 및 모델](#5-앱-아키텍처-및-모델)
6. [인증 흐름 (JWT)](#6-인증-흐름-jwt)
7. [API 엔드포인트 요약](#7-api-엔드포인트-요약)
8. [삼성카드 CSV 업로드](#8-삼성카드-csv-업로드)
9. [AI 카드 추천 (SSAFY GMS API)](#9-ai-카드-추천-ssafy-gms-api)
10. [Fixtures — 초기 카드 데이터](#10-fixtures--초기-카드-데이터)
11. [개발 규칙 및 주의사항](#11-개발-규칙-및-주의사항)

---

## 1. 기술 스택

| 항목 | 버전 / 설명 |
|---|---|
| Python | 3.11+ |
| Django | 4.2.16 |
| Django REST Framework | 3.15.2 |
| JWT 인증 | djangorestframework-simplejwt 5.3.1 |
| CORS | django-cors-headers 4.4.0 |
| 환경변수 | python-dotenv 1.0.1 |
| AI 연동 | openai SDK ≥ 1.52.0 (SSAFY GMS API) |
| DB | SQLite3 (개발) |
| 이미지 처리 | Pillow 10.4.0 |

---

## 2. 프로젝트 구조

```
pjt_card/
├── backend/
│   ├── config/             # Django 프로젝트 설정
│   │   ├── settings.py
│   │   ├── urls.py         # 루트 URL 라우팅
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── accounts/           # 사용자 인증 앱
│   ├── cards/              # 삼성카드 상품/혜택 앱
│   ├── surveys/            # 지출 설문 & 거래내역 앱
│   ├── reports/            # 리포트 앱
│   ├── ai/                 # AI 카드 추천 앱 (GMS API)
│   ├── fixtures/           # 초기 카드 데이터 (삼성카드)
│   │   ├── cards.json
│   │   └── card_benefits.json
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env                # ⚠️ Git 제외 — 직접 생성 필요
│   └── .env.example        # 환경변수 템플릿
└── docs/
    ├── API_명세서.md
    └── BACKEND_GUIDE.md    # 이 문서
```

### URL 라우팅 구조

```
/api/accounts/      → accounts 앱
/api/cards/         → cards 앱
/api/spending/      → surveys 앱 (지출 설문)
/api/transactions/  → surveys 앱 (거래내역 / CSV 업로드)
/api/reports/       → reports 앱
/api/ai/            → ai 앱
```

---

## 3. 로컬 환경 세팅

### 3-1. 저장소 클론 후 backend 폴더로 이동

```bash
cd backend
```

### 3-2. 가상환경 생성 및 활성화

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3-3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3-4. 환경변수 파일 생성

`.env.example`을 복사해서 `.env`를 만든 뒤 값을 채웁니다.

```bash
copy .env.example .env   # Windows
cp .env.example .env     # macOS/Linux
```

팀 채널에서 공유된 `GMS_API_KEY` 값을 `.env`에 입력합니다. (아래 [4. 환경 변수](#4-환경-변수) 참고)

### 3-5. DB 마이그레이션

```bash
python manage.py migrate
```

### 3-6. 초기 카드 데이터 로드 (삼성카드 7종)

```bash
python manage.py loaddata fixtures/cards.json fixtures/card_benefits.json
```

### 3-7. 개발 서버 실행

```bash
python manage.py runserver
```

서버 주소: `http://127.0.0.1:8000`

### 3-8. VS Code 인터프리터 설정 (선택)

`Ctrl + Shift + P` → `Python: Select Interpreter` → `.\backend\venv\Scripts\python.exe` 선택

---

## 4. 환경 변수

`.env` 파일은 **절대 Git에 커밋하지 않습니다.** `.gitignore`에 등록되어 있습니다.

```env
# Django
SECRET_KEY=django-insecure-cardfit-local-dev-key-change-before-deploy
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# SSAFY GMS API (팀 채널에서 공유된 키 사용)
GMS_API_KEY=<팀에서 받은 API 키>
GMS_API_BASE_URL=https://gms.ssafy.io/gmsapi/api.openai.com/v1/chat/completions
GMS_MODEL=gpt-4o
```

> **중요**: `GMS_API_BASE_URL`은 `/chat/completions`가 붙은 전체 URL로 입력합니다.  
> `ai/recommender.py`의 `_build_client()` 함수가 OpenAI SDK에 맞게 자동으로 suffix를 제거합니다.

---

## 5. 앱 아키텍처 및 모델

### accounts — 사용자 인증

커스텀 User 모델 (`AbstractBaseUser` 기반), **이메일로 로그인**합니다.

```
User
├── email (unique, USERNAME_FIELD)
├── username
├── selected_card → FK → cards.Card (nullable)
├── is_active, is_staff
└── created_at, updated_at
```

### cards — 삼성카드 상품

**삼성카드 단일 카드사** 데이터만 사용합니다. fixtures로 초기화하며, 관리자가 Admin에서 추가/수정합니다.

```
Card
├── card_company   (예: "삼성카드")
├── card_name
├── card_type      (credit / debit / prepaid)
├── annual_fee     (원)
├── min_prev_month_spending  (전월 실적 기준, 원)
└── apply_url      (삼성카드 공식 사이트 링크)

CardBenefit  (Card : CardBenefit = 1 : N)
├── card → FK → Card
├── benefit_category  (food / transport / shopping / entertainment / communication / travel / health / other)
├── benefit_type      (discount / cashback / point / mileage)
├── discount_rate     (%, DecimalField)
└── monthly_limit     (월 한도, 원, nullable)
```

### surveys — 지출 설문 및 거래내역

```
UserSurvey
├── user → FK → accounts.User
├── input_type     (manual / csv / api)
├── food_monthly, transport_monthly, shopping_monthly,
│   entertainment_monthly, communication_monthly, other_monthly  (원/월)
├── age_group      (20s / 30s / 40s / 50s / 60s)
├── max_annual_fee (원)
├── income_level   (low / mid / high)
└── total_monthly  @property — 카테고리 합산

SpendingTransaction  (UserSurvey : SpendingTransaction = 1 : N)
├── survey → FK → UserSurvey
├── category     (food / transport / shopping / entertainment / communication / health / other)
├── merchant     (가맹점명)
├── amount       (원)
└── transaction_date
```

### reports — 리포트

현재 기본 뷰 구조만 존재합니다. surveys 데이터를 집계하여 월별 리포트를 제공하는 방향으로 확장 예정입니다.

### ai — AI 카드 추천

SSAFY GMS API를 호출하여 실시간 추천 결과를 반환합니다. **결과를 DB에 저장하지 않습니다.**

---

## 6. 인증 흐름 (JWT)

```
1. POST /api/accounts/register/   → 회원가입
2. POST /api/accounts/login/      → access + refresh 토큰 발급
3. 이후 모든 요청:
   Authorization: Bearer <access_token>
4. POST /api/accounts/token/refresh/  → access 토큰 갱신 (refresh 토큰 사용)
5. POST /api/accounts/logout/         → refresh 토큰 블랙리스트 처리
```

| 설정 | 값 |
|---|---|
| Access Token 유효기간 | 2시간 |
| Refresh Token 유효기간 | 7일 |
| Rotate Refresh Tokens | True (갱신 시 새 refresh 토큰 발급) |
| Blacklist After Rotation | True (이전 refresh 토큰 무효화) |

프론트에서 access 토큰 만료 시 refresh 토큰으로 자동 갱신하는 인터셉터 처리가 필요합니다.

---

## 7. API 엔드포인트 요약

> 전체 요청/응답 예시는 [API_명세서.md](./API_명세서.md)를 참고하세요.

### accounts

| 메서드 | URL | 설명 | 인증 |
|---|---|---|---|
| POST | `/api/accounts/register/` | 회원가입 | 불필요 |
| POST | `/api/accounts/login/` | 로그인 (JWT 발급) | 불필요 |
| POST | `/api/accounts/logout/` | 로그아웃 (토큰 블랙리스트) | 필요 |
| POST | `/api/accounts/token/refresh/` | Access 토큰 갱신 | 불필요 |
| GET/PUT | `/api/accounts/profile/` | 내 프로필 조회/수정 | 필요 |
| POST | `/api/accounts/select-card/` | 사용 카드 선택 | 필요 |

### cards

| 메서드 | URL | 설명 | 인증 |
|---|---|---|---|
| GET | `/api/cards/` | 삼성카드 전체 목록 | 불필요 |
| GET | `/api/cards/<id>/` | 카드 상세 (혜택 포함) | 불필요 |

### spending (surveys)

| 메서드 | URL | 설명 | 인증 |
|---|---|---|---|
| GET | `/api/spending/surveys/` | 내 설문 목록 | 필요 |
| POST | `/api/spending/surveys/` | 지출 설문 등록 | 필요 |
| GET/PUT/DELETE | `/api/spending/surveys/<id>/` | 설문 상세/수정/삭제 | 필요 |

### transactions (surveys)

| 메서드 | URL | 설명 | 인증 |
|---|---|---|---|
| GET | `/api/transactions/` | 내 거래내역 목록 | 필요 |
| POST | `/api/transactions/upload-csv/` | 삼성카드 CSV 업로드 | 필요 |

### ai

| 메서드 | URL | 설명 | 인증 |
|---|---|---|---|
| GET | `/api/ai/recommend/` | 저장된 설문 기반 AI 추천 | 필요 |
| POST | `/api/ai/recommend/` | 즉석 지출 입력 기반 AI 추천 | 필요 |

---

## 8. 삼성카드 CSV 업로드

### 지원 파일

삼성카드 앱 / 홈페이지에서 내려받은 이용내역 CSV 파일 (인코딩: utf-8-sig 또는 euc-kr 자동 감지)

### 요청

```http
POST /api/transactions/upload-csv/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

file: <CSV 파일>
```

### 처리 과정

1. `surveys/utils.py`의 `parse_samsung_csv()` 함수로 파싱
2. 취소 거래(`취소여부` 컬럼) 및 금액 ≤ 0 건 자동 제외
3. 가맹점명 → 카테고리 자동 분류 (`MERCHANT_CATEGORY_MAP`)
4. 카테고리별 합산 → `UserSurvey` 자동 생성 (input_type=`csv`)
5. 개별 거래는 `SpendingTransaction`으로 저장

### 가맹점-카테고리 매핑 주요 키워드

| 카테고리 | 키워드 예시 |
|---|---|
| food | 스타벅스, 배달의민족, GS25, 파리바게뜨 |
| transport | 카카오T, 티머니, 한국철도, 지하철 |
| shopping | 이마트, 홈플러스, 무신사, 올리브영 |
| communication | KT, SKT, LG유플러스 |
| entertainment | CGV, 롯데시네마, 메가박스 |
| health | 정형외과, 내과, 약국 |

매핑에 없는 가맹점은 `other`로 분류됩니다. 키워드 추가가 필요하면 `surveys/utils.py`의 `MERCHANT_CATEGORY_MAP`을 수정합니다.

---

## 9. AI 카드 추천 (SSAFY GMS API)

### 개요

- SSAFY에서 제공하는 GMS(OpenAI 호환) API를 사용합니다.
- OpenAI Python SDK로 연동합니다 (`openai >= 1.52.0`).
- **추천 결과는 DB에 저장하지 않습니다** — 매 요청마다 실시간으로 GMS에 호출합니다.

### 동작 흐름

```
클라이언트
  │
  ├─ GET /api/ai/recommend/          저장된 UserSurvey 기반 추천
  └─ POST /api/ai/recommend/         즉석 지출 데이터로 추천
          │
          ↓
  ai/recommender.py
  ├── _build_client()          GMS API 클라이언트 생성
  ├── _build_cards_context()   연회비 조건에 맞는 삼성카드 목록 조회
  ├── _build_prompt()          소비패턴 + 카드 목록으로 프롬프트 작성
  └── get_gms_recommendations() → GMS API 호출 → JSON 파싱 → 반환
          │
          ↓
  응답: recommendations (3개) + spending_insight
```

### 응답 구조 예시

```json
{
  "survey_id": 1,
  "based_on": {
    "food_monthly": 400000,
    "transport_monthly": 100000,
    "total_monthly": 700000,
    "max_annual_fee": 30000
  },
  "recommendations": [
    {
      "card_id": 1,
      "card_name": "taptap O",
      "rank": 1,
      "reason": "식비 비중이 높은 사용자에게 적합합니다. 편의점·카페 5% 할인으로 월 2만원 이상 절약 가능합니다.",
      "expected_monthly_benefit": "약 25,000원",
      "tip": "전월 실적 30만원 이상 유지 시 모든 혜택이 활성화됩니다."
    }
  ],
  "spending_insight": "식비와 쇼핑 비중이 전체의 70%로 생활밀착형 혜택 카드가 유리합니다."
}
```

### GMS API URL 주의사항

`.env`의 `GMS_API_BASE_URL`에 `/chat/completions`가 포함된 전체 URL을 입력하더라도,  
`ai/recommender.py`의 `_build_client()` 함수가 OpenAI SDK와의 충돌을 방지하기 위해 자동으로 suffix를 제거합니다.

```python
# ai/recommender.py
if base_url.endswith('/chat/completions'):
    base_url = base_url[: -len('/chat/completions')]
```

---

## 10. Fixtures — 초기 카드 데이터

삼성카드 공식 홈페이지(samsungcard.com) 기준으로 수동 작성된 JSON 파일입니다.

### 포함된 카드 (7종)

| ID | 카드명 | 종류 | 연회비 |
|---|---|---|---|
| 1 | taptap O | 신용 | 15,000원 |
| 2 | iD VITA ALL STATION | 신용 | 20,000원 |
| 3 | MILEAGE PLATINUM | 신용 | 100,000원 |
| 4 | THE iD. 1st | 신용 | 10,000원 |
| 5 | 모니모A | 신용 | 20,000원 |
| 6 | K-패스 체크 | 체크 | 0원 |
| 7 | 삼성카드 체크카드 | 체크 | 0원 |

### 데이터 적용 방법

```bash
# 기존 DB 초기화 후 재로드 (개발 중 데이터 리셋 필요 시)
python manage.py flush --no-input
python manage.py loaddata fixtures/cards.json fixtures/card_benefits.json

# 또는 마이그레이션부터 다시 (완전 초기화)
python manage.py migrate
python manage.py loaddata fixtures/cards.json fixtures/card_benefits.json
```

### 카드 데이터 수정 방법

1. `fixtures/cards.json` 또는 `fixtures/card_benefits.json` 직접 수정
2. `python manage.py flush --no-input && python manage.py loaddata ...` 재실행
3. 또는 Django Admin(`/admin/`)에서 직접 수정

---

## 11. 개발 규칙 및 주의사항

### Git 관련

- `.env` 파일은 **절대 커밋 금지** (`.gitignore`에 등록됨)
- `.env.example`은 커밋 가능 (실제 키 값 없이 키 이름만 포함)
- `db.sqlite3`, `media/`, `staticfiles/`, `venv/` 모두 `.gitignore` 처리됨

### 데이터 정책

- 카드사는 **삼성카드 단일** — 다른 카드사 데이터 추가 금지
- AI 추천 결과는 DB에 저장하지 않음 (기획서 결정 사항)
- 카드 데이터 변경 시 fixtures 파일도 함께 업데이트

### API 인증

- 모든 `/api/` 엔드포인트는 JWT Bearer 토큰 필요 (카드 목록 조회 제외)
- 프론트에서 `Authorization: Bearer <token>` 헤더를 모든 요청에 포함해야 함

### CORS 허용 출처

```
http://localhost:5173   (Vite 기본 포트)
http://localhost:3000   (React/Next 기본 포트)
http://127.0.0.1:5173
http://127.0.0.1:3000
```

다른 포트 사용 시 `config/settings.py`의 `CORS_ALLOWED_ORIGINS`에 추가합니다.

### 마이그레이션

- 모델 변경 후 반드시 `python manage.py makemigrations && python manage.py migrate` 실행
- 마이그레이션 파일은 Git에 포함합니다

### 관리자 계정 생성

```bash
python manage.py createsuperuser
```

Admin 페이지: `http://127.0.0.1:8000/admin/`

---

## 빠른 시작 요약

```bash
cd backend
python -m venv venv && venv\Scripts\activate  # Windows
pip install -r requirements.txt
copy .env.example .env                         # .env 편집 후 GMS_API_KEY 입력
python manage.py migrate
python manage.py loaddata fixtures/cards.json fixtures/card_benefits.json
python manage.py runserver
```
