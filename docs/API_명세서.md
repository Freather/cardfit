# CardFit API 명세서

> Base URL: `http://localhost:8000`  
> 인증 방식: JWT Bearer Token  
> Content-Type: `application/json`

---

## 목차

- [인증 헤더](#인증-헤더)
- [공통 응답 형식](#공통-응답-형식)
- [1. Accounts — 계정](#1-accounts--계정)
- [2. Cards — 카드](#2-cards--카드)
- [3. Surveys — 지출 설문](#3-surveys--지출-설문)
- [4. Transactions — 거래내역](#4-transactions--거래내역)
- [5. Reports — 리포트](#5-reports--리포트)
- [6. AI — 카드 추천](#6-ai--카드-추천)
- [7. Community — 커뮤니티](#7-community--커뮤니티)

---

## 인증 헤더

로그인 후 발급된 `access` 토큰을 모든 인증 필요 요청에 포함합니다.

```
Authorization: Bearer <access_token>
```

---

## 공통 응답 형식

### 에러 응답

```json
{
  "detail": "에러 메시지"
}
```

| HTTP 상태 | 의미 |
|-----------|------|
| 200 | 성공 |
| 201 | 생성 성공 |
| 204 | 삭제 성공 (본문 없음) |
| 400 | 잘못된 요청 (유효성 검사 실패) |
| 401 | 인증 필요 (토큰 없음 또는 만료) |
| 403 | 권한 없음 |
| 404 | 리소스 없음 |
| 503 | 서버 설정 오류 (OAuth 키 미설정 등) |

---

## 1. Accounts — 계정

### 1-1. 회원가입

**POST** `/api/accounts/register/`  
인증 불필요

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| email | string | ✅ | 이메일 (고유) |
| username | string | ✅ | 닉네임 (고유) |
| password | string | ✅ | 비밀번호 (8자 이상) |
| password_confirm | string | ✅ | 비밀번호 확인 |

```json
{
  "email": "user@example.com",
  "username": "홍길동",
  "password": "password123",
  "password_confirm": "password123"
}
```

**Response** `201 Created`

```json
{
  "message": "회원가입이 완료되었습니다.",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "홍길동",
    "selected_card_id": null,
    "created_at": "2026-06-08T12:00:00+09:00",
    "updated_at": "2026-06-08T12:00:00+09:00"
  },
  "tokens": {
    "access": "<access_token>",
    "refresh": "<refresh_token>"
  }
}
```

---

### 1-2. 로그인

**POST** `/api/accounts/login/`  
인증 불필요

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| email | string | ✅ | 이메일 |
| password | string | ✅ | 비밀번호 |

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response** `200 OK`

```json
{
  "message": "로그인 성공",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "홍길동",
    "selected_card_id": 3,
    "created_at": "2026-06-08T12:00:00+09:00",
    "updated_at": "2026-06-08T12:00:00+09:00"
  },
  "tokens": {
    "access": "<access_token>",
    "refresh": "<refresh_token>"
  }
}
```

---

### 1-3. 로그아웃

**POST** `/api/accounts/logout/`  
인증 필요

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| refresh | string | ✅ | Refresh 토큰 (블랙리스트 등록) |

```json
{
  "refresh": "<refresh_token>"
}
```

**Response** `200 OK`

```json
{
  "message": "로그아웃 완료"
}
```

---

### 1-4. 토큰 갱신

**POST** `/api/accounts/token/refresh/`  
인증 불필요

**Request Body**

```json
{
  "refresh": "<refresh_token>"
}
```

**Response** `200 OK`

```json
{
  "access": "<new_access_token>",
  "refresh": "<new_refresh_token>"
}
```

---

### 1-5. 프로필 조회

**GET** `/api/accounts/profile/`  
인증 필요

**Response** `200 OK`

```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "홍길동",
  "selected_card_id": 3,
  "created_at": "2026-06-08T12:00:00+09:00",
  "updated_at": "2026-06-08T12:00:00+09:00"
}
```

---

### 1-6. 프로필 수정

**PUT** `/api/accounts/profile/`  
인증 필요 · 부분 수정 가능

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| username | string | | 닉네임 변경 |

```json
{
  "username": "새닉네임"
}
```

**Response** `200 OK` — 수정된 프로필 반환

---

### 1-7. 회원 탈퇴

**DELETE** `/api/accounts/profile/`  
인증 필요

계정을 비활성화합니다 (실제 삭제 아님).

**Response** `204 No Content`

```json
{
  "message": "계정이 비활성화되었습니다."
}
```

---

### 1-8. 대표 카드 설정

**PUT** `/api/accounts/select-card/`  
인증 필요

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| selected_card | integer | ✅ | 카드 ID (null 가능) |

```json
{
  "selected_card": 3
}
```

**Response** `200 OK`

```json
{
  "message": "대표 카드가 설정되었습니다.",
  "selected_card_id": 3
}
```

---

### 1-9. 카카오 소셜 로그인 시작

**GET** `/api/accounts/oauth/kakao/`  
인증 불필요

카카오 OAuth 인증 페이지로 리디렉트합니다.

**Query Parameters**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| next | string | 로그인 완료 후 이동할 프론트엔드 경로 (기본값: `/`) |
| debug | string | `1` 전달 시 리디렉트 없이 설정 진단 정보 반환 |

**Response** — 카카오 인증 페이지로 302 리디렉트  
설정 오류 시 `503 Service Unavailable`

```json
{
  "detail": "카카오 로그인 설정이 필요합니다.",
  "missing": ["KAKAO_REST_API_KEY"]
}
```

---

### 1-10. 카카오 소셜 로그인 콜백

**GET** `/api/accounts/oauth/kakao/callback/`  
인증 불필요

카카오가 호출하는 콜백 엔드포인트입니다. 처리 결과에 따라 프론트엔드로 리디렉트합니다.

- 성공 시: `{FRONTEND_URL}/login/oauth/callback?access=...&refresh=...`
- 이메일 미제공 시: `{FRONTEND_URL}/login/oauth/email?provider=kakao&token=...&nickname=...`
- 오류 시: `{FRONTEND_URL}/login/oauth/callback?error=...`

> 직접 호출하는 엔드포인트가 아닙니다. 카카오 개발자 콘솔의 Redirect URI로 등록해야 합니다.

---

### 1-11. 네이버 소셜 로그인 시작

**GET** `/api/accounts/oauth/naver/`  
인증 불필요

네이버 OAuth 인증 페이지로 리디렉트합니다.

**Query Parameters**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| next | string | 로그인 완료 후 이동할 프론트엔드 경로 (기본값: `/`) |

**Response** — 네이버 인증 페이지로 302 리디렉트  
설정 오류 시 `503 Service Unavailable`

```json
{
  "detail": "네이버 로그인 설정이 필요합니다.",
  "missing": ["NAVER_CLIENT_ID", "NAVER_CLIENT_SECRET"]
}
```

---

### 1-12. 네이버 소셜 로그인 콜백

**GET** `/api/accounts/oauth/naver/callback/`  
인증 불필요

네이버가 호출하는 콜백 엔드포인트입니다. 처리 결과에 따라 프론트엔드로 리디렉트합니다.

- 성공 시: `{FRONTEND_URL}/login/oauth/callback?access=...&refresh=...`
- 이메일 미동의 시: `{FRONTEND_URL}/login/oauth/callback?error=네이버 계정 이메일 제공 동의가 필요해요.`

> 직접 호출하는 엔드포인트가 아닙니다. 네이버 개발자 콘솔의 Callback URL로 등록해야 합니다.

---

### 1-13. OAuth 이메일 보완 완료

**POST** `/api/accounts/oauth/email/complete/`  
인증 불필요

카카오 소셜 로그인 시 이메일이 제공되지 않은 경우, 사용자가 직접 입력한 이메일로 회원가입/로그인을 완료합니다.

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| token | string | ✅ | 카카오 콜백에서 받은 pending token (10분 유효) |
| email | string | ✅ | 사용자가 입력한 이메일 주소 |
| next | string | | 완료 후 이동할 경로 (기본값: `/`) |

```json
{
  "token": "<pending_token>",
  "email": "user@example.com",
  "next": "/dashboard"
}
```

**Response** `200 OK`

```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "홍길동",
    "selected_card_id": null,
    "created_at": "2026-06-08T12:00:00+09:00",
    "updated_at": "2026-06-08T12:00:00+09:00"
  },
  "tokens": {
    "access": "<access_token>",
    "refresh": "<refresh_token>"
  },
  "next": "/dashboard"
}
```

| HTTP 상태 | 의미 |
|-----------|------|
| 200 | 성공 |
| 400 | 토큰 만료 또는 이메일 형식 오류 |

---

## 2. Cards — 카드

### 2-1. 카드 목록 조회

**GET** `/api/cards/`  
인증 불필요 (로그인 시 `is_wished` 정확하게 반환)

**Query Parameters**

| 파라미터 | 타입 | 설명 | 예시 |
|----------|------|------|------|
| card_type | string | 카드 종류 필터 | `credit` / `debit` / `prepaid` |
| company | string | 카드사 이름 검색 (부분 일치) | `삼성` |
| max_annual_fee | integer | 연회비 상한 필터 | `30000` |

**Response** `200 OK`

```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "card_company": "삼성카드",
      "card_name": "삼성 iD ON 카드",
      "card_type": "credit",
      "card_type_display": "신용카드",
      "annual_fee": 0,
      "min_prev_month_spending": 300000,
      "apply_url": "https://www.samsungcard.com",
      "image_url": "https://cdn.example.com/cards/1.png",
      "benefit_count": 3,
      "benefits": [...],
      "is_wished": false,
      "synced_at": "2026-06-01T00:00:00Z"
    }
  ]
}
```

---

### 2-2. 카드 상세 조회

**GET** `/api/cards/{id}/`  
인증 불필요 (로그인 시 `is_wished` 정확하게 반환)

**Response** `200 OK`

```json
{
  "id": 1,
  "card_company": "삼성카드",
  "card_name": "삼성 iD ON 카드",
  "card_type": "credit",
  "card_type_display": "신용카드",
  "annual_fee": 0,
  "min_prev_month_spending": 300000,
  "apply_url": "https://www.samsungcard.com",
  "image_url": "https://cdn.example.com/cards/1.png",
  "is_wished": false,
  "synced_at": "2026-06-01T00:00:00Z",
  "benefits": [
    {
      "id": 1,
      "benefit_category": "food",
      "benefit_category_display": "식비",
      "benefit_type": "discount",
      "benefit_type_display": "할인",
      "discount_rate": "10.00",
      "monthly_limit": 3000,
      "condition_description": "전월 실적 30만원 이상 시 식비 10% 할인, 월 3,000원 한도"
    }
  ]
}
```

---

### 2-3. 카드 혜택 목록

**GET** `/api/cards/{id}/benefits/`  
인증 불필요

**Query Parameters**

| 파라미터 | 타입 | 설명 | 예시 |
|----------|------|------|------|
| category | string | 혜택 카테고리 필터 | `food` / `transportation` / `shopping` |

**Response** `200 OK` — 혜택 배열 반환

```json
[
  {
    "id": 1,
    "benefit_category": "food",
    "benefit_category_display": "식비",
    "benefit_type": "discount",
    "benefit_type_display": "할인",
    "discount_rate": "10.00",
    "monthly_limit": 3000,
    "condition_description": "전월 실적 30만원 이상 시 식비 10% 할인"
  }
]
```

---

### 2-4. 카드 찜 목록 조회

**GET** `/api/cards/wishlist/`  
인증 필요

**Response** `200 OK`

```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "card": {
        "id": 3,
        "card_company": "삼성카드",
        "card_name": "삼성 iD ON 카드",
        "card_type": "credit",
        "card_type_display": "신용카드",
        "annual_fee": 0,
        "min_prev_month_spending": 300000,
        "apply_url": "https://www.samsungcard.com",
        "image_url": "https://cdn.example.com/cards/3.png",
        "benefit_count": 3,
        "benefits": [...],
        "is_wished": true,
        "synced_at": "2026-06-01T00:00:00Z"
      },
      "source": "detail",
      "created_at": "2026-06-22T07:16:00Z"
    }
  ]
}
```

---

### 2-5. 카드 찜 추가

**POST** `/api/cards/wishlist/`  
인증 필요

이미 찜한 카드를 다시 추가해도 기존 항목을 반환합니다 (중복 허용).

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| card_id | integer | ✅ | 찜할 카드 ID |
| source | string | | `search` / `detail` / `recommendation` / `compare` |

```json
{
  "card_id": 3,
  "source": "detail"
}
```

**Response** `201 Created` — 찜 항목 반환

---

### 2-6. 카드 찜 삭제

**DELETE** `/api/cards/wishlist/{card_id}/`  
인증 필요

**Response** `204 No Content`

---

#### 카드 혜택 카테고리 코드표

| 코드 | 의미 |
|------|------|
| `food` | 식비 |
| `transportation` | 교통 |
| `fuel` | 주유 |
| `shopping` | 쇼핑 |
| `entertainment` | 여가/문화 |
| `communication` | 통신 |
| `travel` | 여행 |
| `health` | 의료/건강 |
| `point` | 포인트 |
| `other` | 기타 |

---

## 3. Surveys — 지출 설문

### 3-1. 설문 목록 조회

**GET** `/api/spending/`  
인증 필요

로그인한 사용자의 설문 목록을 최신순으로 반환합니다.

**Response** `200 OK`

```json
[
  {
    "id": 1,
    "input_type": "manual",
    "input_type_display": "직접입력",
    "food_monthly": 300000,
    "transport_monthly": 80000,
    "fuel_monthly": 100000,
    "shopping_monthly": 200000,
    "entertainment_monthly": 50000,
    "communication_monthly": 55000,
    "health_monthly": 20000,
    "other_monthly": 30000,
    "total_monthly": 835000,
    "age_group": "30s",
    "age_group_display": "30대",
    "max_annual_fee": 30000,
    "income_level": "mid",
    "income_level_display": "중소득",
    "transaction_count": 0,
    "transaction_start_date": null,
    "transaction_end_date": null,
    "created_at": "2026-06-08T12:00:00+09:00",
    "updated_at": "2026-06-08T12:00:00+09:00"
  }
]
```

---

### 3-2. 설문 생성 (직접 입력)

**POST** `/api/spending/`  
인증 필요

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| input_type | string | | `manual` / `csv` / `api` (기본값: `manual`) |
| food_monthly | integer | | 월 식비 (원) |
| transport_monthly | integer | | 월 교통비 (원) |
| fuel_monthly | integer | | 월 주유비 (원) |
| shopping_monthly | integer | | 월 쇼핑비 (원) |
| entertainment_monthly | integer | | 월 여가비 (원) |
| communication_monthly | integer | | 월 통신비 (원) |
| health_monthly | integer | | 월 의료/건강비 (원) |
| other_monthly | integer | | 월 기타 지출 (원) |
| age_group | string | ✅ | `20s` / `30s` / `40s` / `50s` / `60s` |
| max_annual_fee | integer | ✅ | 최대 연회비 (원) |
| income_level | string | ✅ | `low` / `mid` / `high` |

```json
{
  "input_type": "manual",
  "food_monthly": 300000,
  "transport_monthly": 80000,
  "fuel_monthly": 100000,
  "shopping_monthly": 200000,
  "entertainment_monthly": 50000,
  "communication_monthly": 55000,
  "health_monthly": 20000,
  "other_monthly": 30000,
  "age_group": "30s",
  "max_annual_fee": 30000,
  "income_level": "mid"
}
```

**Response** `201 Created` — 생성된 설문 반환

---

### 3-3. 설문 상태 조회

**GET** `/api/spending/status/`  
인증 필요

로그인한 사용자의 직접입력 설문 및 CSV 설문 존재 여부를 반환합니다.

**Response** `200 OK`

```json
{
  "has_survey": true,
  "has_csv": true,
  "latest_survey_id": 1,
  "latest_csv_id": 2
}
```

| 필드 | 설명 |
|------|------|
| has_survey | `input_type=manual` 설문 존재 여부 |
| has_csv | `input_type=csv` 설문 존재 여부 |
| latest_survey_id | 가장 최근 manual 설문 ID (없으면 null) |
| latest_csv_id | 가장 최근 csv 설문 ID (없으면 null) |

---

### 3-4. 설문 상세 조회

**GET** `/api/spending/{id}/`  
인증 필요

거래내역(`transactions`)을 포함하여 반환합니다.

**Response** `200 OK`

```json
{
  "id": 1,
  "input_type": "csv",
  "input_type_display": "CSV 업로드",
  "food_monthly": 250000,
  "transport_monthly": 95000,
  "fuel_monthly": 0,
  "shopping_monthly": 200000,
  "entertainment_monthly": 40000,
  "communication_monthly": 55000,
  "health_monthly": 20000,
  "other_monthly": 35000,
  "total_monthly": 695000,
  "age_group": "30s",
  "age_group_display": "30대",
  "max_annual_fee": 30000,
  "income_level": "mid",
  "income_level_display": "중소득",
  "transaction_count": 87,
  "transaction_start_date": "2026-04-01",
  "transaction_end_date": "2026-05-31",
  "created_at": "2026-06-08T12:00:00+09:00",
  "updated_at": "2026-06-08T12:00:00+09:00",
  "transactions": [
    {
      "id": 1,
      "survey": 1,
      "category": "food",
      "category_display": "식비",
      "merchant": "스타벅스 강남점",
      "amount": 6500,
      "transaction_date": "2026-05-31"
    }
  ]
}
```

---

### 3-5. 설문 수정

**PUT** `/api/spending/{id}/`  
인증 필요 · 부분 수정 가능

**Request Body** — 수정할 필드만 전송

```json
{
  "max_annual_fee": 50000,
  "age_group": "30s"
}
```

**Response** `200 OK` — 수정된 설문 반환

---

### 3-6. 설문 삭제

**DELETE** `/api/spending/{id}/`  
인증 필요

연결된 거래내역도 함께 삭제됩니다.

**Response** `204 No Content`

---

### 3-7. CSV 파일 업로드

**POST** `/api/spending/upload-csv/`  
인증 필요 · `Content-Type: multipart/form-data`

삼성카드 CSV 포맷을 파싱하여 설문 + 거래내역을 자동 생성합니다.

**Request Form Data**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| file | file | ✅ | `.csv` 파일 (최대 5MB) |
| age_group | string | | `20s` / `30s` / `40s` / `50s` / `60s` (기본값: `30s`) |
| income_level | string | | `low` / `mid` / `high` (기본값: `mid`) |
| max_annual_fee | integer | | 최대 연회비 (기본값: `100000`) |

**Response** `201 Created`

```json
{
  "message": "87건의 거래내역이 분석되었습니다.",
  "survey": {
    "id": 2,
    "input_type": "csv",
    "input_type_display": "CSV 업로드",
    "food_monthly": 312400,
    "transport_monthly": 95600,
    "shopping_monthly": 288000,
    "entertainment_monthly": 42000,
    "communication_monthly": 55000,
    "other_monthly": 45000,
    "total_monthly": 838000,
    "transaction_count": 87,
    "transaction_start_date": "2026-04-01",
    "transaction_end_date": "2026-05-31",
    "transactions": [...]
  }
}
```

---

## 4. Transactions — 거래내역

### 4-1. 거래내역 목록 조회

**GET** `/api/transactions/`  
인증 필요

**Query Parameters**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| survey_id | integer | 특정 설문의 거래내역만 조회 |
| category | string | 카테고리 필터 |

**Response** `200 OK`

```json
[
  {
    "id": 1,
    "survey": 1,
    "category": "food",
    "category_display": "식비",
    "merchant": "스타벅스 강남점",
    "amount": 6500,
    "transaction_date": "2026-05-31"
  }
]
```

---

### 4-2. 거래내역 단건 추가

**POST** `/api/transactions/`  
인증 필요

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| survey_id | integer | ✅ | 연결할 설문 ID |
| category | string | ✅ | `food` / `transport` / `fuel` / `shopping` / `entertainment` / `communication` / `health` / `other` |
| merchant | string | ✅ | 가맹점명 |
| amount | integer | ✅ | 금액 (원) |
| transaction_date | string | ✅ | 거래일 (`YYYY-MM-DD`) |

```json
{
  "survey_id": 1,
  "category": "food",
  "merchant": "이디야커피 역삼점",
  "amount": 4500,
  "transaction_date": "2026-05-30"
}
```

**Response** `201 Created`

---

### 4-3. 거래내역 상세 조회

**GET** `/api/transactions/{id}/`  
인증 필요

**Response** `200 OK` — 거래내역 단건 반환

---

### 4-4. 거래내역 수정

**PUT** `/api/transactions/{id}/`  
인증 필요 · 부분 수정 가능

**Response** `200 OK`

---

### 4-5. 거래내역 삭제

**DELETE** `/api/transactions/{id}/`  
인증 필요

**Response** `204 No Content`

---

#### 거래 카테고리 코드표

| 코드 | 의미 |
|------|------|
| `food` | 식비 |
| `transport` | 교통 |
| `fuel` | 주유 |
| `shopping` | 쇼핑 |
| `entertainment` | 여가 |
| `communication` | 통신 |
| `health` | 의료/건강 |
| `other` | 기타 |

---

## 5. Reports — 리포트

> 모든 리포트 API는 인증이 필요하며, 로그인한 사용자의 데이터만 조회합니다.  
> CSV 업로드(`input_type=csv`) 데이터를 기반으로 분석합니다.

---

### 5-1. 월 지출 요약

**GET** `/api/reports/spending-summary/`  
인증 필요

최신 CSV 설문과 직접입력 설문을 결합하여 카테고리별 월 지출 요약을 반환합니다.  
두 설문이 모두 없으면 `404`를 반환합니다.

**Response** `200 OK`

```json
{
  "survey_id": 2,
  "preference_survey_id": 1,
  "input_type": "csv",
  "categories": {
    "food": 312400,
    "transport": 95600,
    "fuel": 0,
    "shopping": 288000,
    "entertainment": 42000,
    "communication": 55000,
    "health": 0,
    "other": 45000
  },
  "food_monthly": 312400,
  "transport_monthly": 95600,
  "fuel_monthly": 0,
  "shopping_monthly": 288000,
  "entertainment_monthly": 42000,
  "communication_monthly": 55000,
  "health_monthly": 0,
  "other_monthly": 45000,
  "total_monthly": 838000,
  "age_group": "30s",
  "income_level": "mid",
  "max_annual_fee": 30000,
  "transaction_start_date": "2026-04-01",
  "transaction_end_date": "2026-05-31",
  "created_at": "2026-06-08T12:00:00+09:00"
}
```

| 필드 | 설명 |
|------|------|
| survey_id | CSV 설문 ID |
| preference_survey_id | 직접입력(manual) 설문 ID |
| categories | 카테고리별 월 평균 지출 (중복 필드) |
| transaction_start_date | 거래내역 시작일 |
| transaction_end_date | 거래내역 종료일 |

---

### 5-2. 카테고리별 비율 분석

**GET** `/api/reports/category-breakdown/`  
인증 필요

CSV 거래내역 기반 카테고리별 상세 분석을 반환합니다. `survey_id` 미입력 시 최신 CSV 설문을 사용합니다.

**Query Parameters**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| survey_id | integer | 특정 CSV 설문 ID (미입력 시 최신 CSV 설문) |

**Response** `200 OK`

```json
{
  "total": 838000,
  "raw_total": 1676000,
  "period_months": 2,
  "transaction_start_date": "2026-04-01",
  "transaction_end_date": "2026-05-31",
  "breakdown": [
    {
      "category": "food",
      "total": 312400,
      "raw_total": 624800,
      "count": 42,
      "ratio": 37.3
    },
    {
      "category": "shopping",
      "total": 288000,
      "raw_total": 576000,
      "count": 18,
      "ratio": 34.4
    }
  ]
}
```

| 필드 | 설명 |
|------|------|
| total | 월 평균 총 지출 |
| raw_total | 기간 전체 합계 |
| period_months | 분석 기간 (개월) |
| breakdown[].total | 카테고리 월 평균 지출 |
| breakdown[].raw_total | 카테고리 기간 전체 합계 |
| breakdown[].ratio | 전체 대비 비율 (%) |

---

### 5-3. 월별 지출 트렌드

**GET** `/api/reports/monthly-trend/`  
인증 필요

CSV 거래내역 기반 월별 카테고리 지출 합계를 반환합니다.

**Response** `200 OK`

```json
{
  "trend": {
    "2026-04": {
      "food": 280000,
      "transport": 75000,
      "shopping": 320000
    },
    "2026-05": {
      "food": 312400,
      "transport": 95600,
      "shopping": 288000
    }
  }
}
```

---

### 5-4. 지출 상위 가맹점

**GET** `/api/reports/top-merchants/`  
인증 필요

CSV 거래내역 기반 지출 금액 상위 가맹점을 반환합니다.

**Query Parameters**

| 파라미터 | 타입 | 기본값 | 설명 |
|----------|------|--------|------|
| limit | integer | 10 | 반환할 가맹점 수 |

**Response** `200 OK`

```json
{
  "results": [
    { "merchant": "홈플러스 강남점",     "category": "shopping",      "total": 174600, "count": 2 },
    { "merchant": "무신사 주식회사",     "category": "shopping",      "total": 158000, "count": 2 },
    { "merchant": "에스케이텔레콤 (주)", "category": "communication", "total": 110000, "count": 2 }
  ]
}
```

---

## 6. AI — 카드 추천

### 6-1. 설문 기반 카드 추천 (GET)

**GET** `/api/ai/recommend/`  
인증 필요

저장된 CSV 설문과 직접입력 설문을 기반으로 GMS AI가 최적 카드를 추천합니다.  
두 설문이 모두 없거나 `GMS_API_KEY`가 미설정이면 오류를 반환합니다.

**Query Parameters**

| 파라미터 | 타입 | 기본값 | 설명 |
|----------|------|--------|------|
| survey_id | integer | | 특정 CSV 설문 ID (미입력 시 최신 CSV 설문 사용) |
| top | integer | | 추천 결과 상위 N개로 자름 |

**Response** `200 OK`

```json
{
  "survey_id": 2,
  "preference_survey_id": 1,
  "based_on": {
    "food_monthly": 312400,
    "transport_monthly": 95600,
    "fuel_monthly": 0,
    "shopping_monthly": 288000,
    "entertainment_monthly": 42000,
    "communication_monthly": 55000,
    "health_monthly": 0,
    "other_monthly": 45000,
    "total_monthly": 838000,
    "max_annual_fee": 30000
  },
  "recommendations": [
    {
      "card_id": 4,
      "card_name": "신한 Mr. Life 카드",
      "card_company": "신한카드",
      "annual_fee": 30000,
      "apply_url": "https://www.shinhancard.com",
      "rank": 1,
      "reason": "식비와 쇼핑 지출이 많은 소비 패턴에 최적화된 카드입니다.",
      "expected_monthly_benefit": "월 약 8,550원 절감",
      "net_benefit": "연 72,600원",
      "benefit_details": "식비 5% 할인 (월 최대 15,000원), 쇼핑 3% 할인 (월 최대 8,640원)"
    }
  ],
  "spending_insight": "식비(37.3%)와 쇼핑(34.4%) 비중이 높습니다."
}
```

| HTTP 상태 | 의미 |
|-----------|------|
| 200 | 성공 |
| 404 | 설문 데이터 없음 |
| 503 | GMS_API_KEY 미설정 |
| 502 | AI 추천 오류 |

---

### 6-2. 즉석 지출 입력 추천 (POST)

**POST** `/api/ai/recommend/`  
인증 필요

설문을 저장하지 않고 즉석에서 지출을 입력해 GMS AI 카드 추천을 받습니다.

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| food_monthly | integer | | 월 식비 (원) |
| transport_monthly | integer | | 월 교통비 (원) |
| fuel_monthly | integer | | 월 주유비 (원) |
| shopping_monthly | integer | | 월 쇼핑비 (원) |
| entertainment_monthly | integer | | 월 여가비 (원) |
| communication_monthly | integer | | 월 통신비 (원) |
| health_monthly | integer | | 월 의료/건강비 (원) |
| other_monthly | integer | | 월 기타 지출 (원) |
| max_annual_fee | integer | | 최대 연회비 (기본값: 200,000원) |

```json
{
  "food_monthly": 400000,
  "transport_monthly": 60000,
  "shopping_monthly": 150000,
  "communication_monthly": 55000,
  "max_annual_fee": 15000
}
```

**Response** `200 OK` — GMS AI 추천 결과 반환 (형식은 6-1과 동일)

| HTTP 상태 | 의미 |
|-----------|------|
| 200 | 성공 |
| 503 | GMS_API_KEY 미설정 |
| 502 | AI 추천 오류 |

---

### 6-3. 카드 추천 사유 조회

**GET** `/api/ai/cards/{card_id}/reason/`  
인증 필요

특정 카드에 대해 GMS AI가 사용자 지출 패턴 기반으로 추천 사유를 생성합니다.  
직접입력 설문과 CSV 설문이 모두 있어야 합니다.

**Path Parameters**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| card_id | integer | 추천 사유를 조회할 카드 ID |

**Query Parameters**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| survey_id | integer | 특정 CSV 설문 ID (미입력 시 최신 사용) |

**Response** `200 OK`

```json
{
  "card_id": 4,
  "card_name": "신한 Mr. Life 카드",
  "card_company": "신한카드",
  "reason": "...",
  "expected_monthly_benefit": "...",
  "benefit_details": "..."
}
```

| HTTP 상태 | 의미 |
|-----------|------|
| 200 | 성공 |
| 404 | 카드 없음 또는 설문 데이터 없음 |
| 503 | GMS_API_KEY 미설정 |
| 502 | AI 오류 |

---

### 6-4. 금융 챗봇

**POST** `/api/ai/chat/`  
인증 필요

카드 및 금융 관련 질문에 GMS AI가 대화형으로 답변합니다.

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| messages | array | ✅ | 대화 메시지 배열 (`[{"role": "user", "content": "..."}]`) |
| page_context | object | | 현재 페이지 컨텍스트 정보 (선택) |

```json
{
  "messages": [
    { "role": "user", "content": "식비 할인 혜택이 좋은 카드 추천해줘" }
  ],
  "page_context": {
    "page": "recommend",
    "card_id": 4
  }
}
```

**Response** `200 OK` — GMS AI 답변 반환

```json
{
  "reply": "식비 할인 혜택이 좋은 카드로는 ..."
}
```

| HTTP 상태 | 의미 |
|-----------|------|
| 200 | 성공 |
| 400 | 메시지 형식 오류 |
| 503 | GMS_API_KEY 미설정 |
| 502 | AI 답변 생성 실패 |

---

## 7. Community — 커뮤니티

---

### 7-1. 게시글 목록 조회

**GET** `/api/community/posts/`  
인증 선택 (비로그인 시 `is_liked`, `is_author`는 `false`)

**Query Parameters**

| 파라미터 | 타입 | 설명 | 예시 |
|----------|------|------|------|
| category | string | 카테고리 필터 | `general` / `review` / `question` / `info` |
| search | string | 제목 또는 내용 검색 (부분 일치) | `삼성카드` |
| page | integer | 페이지 번호 (기본값: 1) | `2` |
| page_size | integer | 페이지당 항목 수 (기본값: 10, 최대 50) | `20` |

**Response** `200 OK`

```json
{
  "count": 42,
  "next": "http://localhost:8000/api/community/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user_email": "user@example.com",
      "username": "홍길동",
      "title": "삼성카드 사용 후기",
      "category": "review",
      "views_count": 120,
      "likes_count": 15,
      "comments_count": 5,
      "is_liked": false,
      "is_author": true,
      "created_at": "2026-06-20T10:30:00+09:00"
    }
  ]
}
```

---

### 7-2. 게시글 작성

**POST** `/api/community/posts/`  
인증 필요

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| title | string | ✅ | 제목 (최대 200자) |
| content | string | ✅ | 내용 |
| category | string | | `general` / `review` / `question` / `info` (기본값: `general`) |

```json
{
  "title": "삼성카드 iD ON 사용 후기",
  "content": "식비 할인 혜택이 좋습니다.",
  "category": "review"
}
```

**Response** `201 Created`

```json
{
  "id": 1,
  "user_email": "user@example.com",
  "username": "홍길동",
  "title": "삼성카드 iD ON 사용 후기",
  "content": "식비 할인 혜택이 좋습니다.",
  "category": "review",
  "views_count": 0,
  "likes_count": 0,
  "comments_count": 0,
  "comments": [],
  "is_liked": false,
  "is_author": true,
  "created_at": "2026-06-20T10:30:00+09:00",
  "updated_at": "2026-06-20T10:30:00+09:00"
}
```

---

### 7-3. 인기 게시글 조회

**GET** `/api/community/posts/popular/`  
인증 불필요

좋아요 수 기준 내림차순으로 상위 10개 게시글을 반환합니다 (동점 시 조회수 순).

**Response** `200 OK`

```json
[
  {
    "id": 5,
    "user_email": "user@example.com",
    "username": "홍길동",
    "title": "카드 혜택 총정리",
    "category": "info",
    "views_count": 980,
    "likes_count": 72,
    "comments_count": 18,
    "is_liked": false,
    "is_author": false,
    "created_at": "2026-06-15T09:00:00+09:00"
  }
]
```

---

### 7-4. 게시글 상세 조회

**GET** `/api/community/posts/{id}/`  
인증 선택 (비로그인 시 `is_liked`, `is_author`는 `false`)

**Response** `200 OK`

```json
{
  "id": 1,
  "user_email": "user@example.com",
  "username": "홍길동",
  "title": "삼성카드 iD ON 사용 후기",
  "content": "식비 할인 혜택이 좋습니다.",
  "category": "review",
  "views_count": 42,
  "likes_count": 5,
  "comments_count": 2,
  "comments": [
    {
      "id": 1,
      "user_email": "other@example.com",
      "username": "김철수",
      "content": "저도 사용 중인데 좋더라고요!",
      "likes_count": 3,
      "is_liked": false,
      "is_author": false,
      "created_at": "2026-06-20T11:00:00+09:00",
      "updated_at": "2026-06-20T11:00:00+09:00"
    }
  ],
  "is_liked": false,
  "is_author": true,
  "created_at": "2026-06-20T10:30:00+09:00",
  "updated_at": "2026-06-20T10:30:00+09:00"
}
```

---

### 7-5. 게시글 수정

**PUT** `/api/community/posts/{id}/`  
인증 필요 · 작성자 본인만 가능 · 부분 수정 가능

**Request Body** — 수정할 필드만 전송

| 필드 | 타입 | 설명 |
|------|------|------|
| title | string | 제목 |
| content | string | 내용 |
| category | string | 카테고리 |

```json
{
  "title": "삼성카드 iD ON 후기 (수정)",
  "content": "6개월 사용 후 업데이트합니다."
}
```

**Response** `200 OK` — 수정된 게시글 상세 반환

| HTTP 상태 | 의미 |
|-----------|------|
| 200 | 수정 성공 |
| 403 | 작성자 본인이 아님 |
| 404 | 게시글 없음 |

---

### 7-6. 게시글 삭제

**DELETE** `/api/community/posts/{id}/`  
인증 필요 · 작성자 본인만 가능

**Response** `204 No Content`

| HTTP 상태 | 의미 |
|-----------|------|
| 204 | 삭제 성공 |
| 403 | 작성자 본인이 아님 |
| 404 | 게시글 없음 |

---

### 7-7. 댓글 목록 조회

**GET** `/api/community/posts/{id}/comments/`  
인증 선택 (비로그인 시 `is_liked`, `is_author`는 `false`)

**Response** `200 OK`

```json
[
  {
    "id": 1,
    "user_email": "other@example.com",
    "username": "김철수",
    "content": "저도 사용 중인데 좋더라고요!",
    "likes_count": 3,
    "is_liked": false,
    "is_author": false,
    "created_at": "2026-06-20T11:00:00+09:00",
    "updated_at": "2026-06-20T11:00:00+09:00"
  }
]
```

---

### 7-8. 댓글 작성

**POST** `/api/community/posts/{id}/comments/`  
인증 필요

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| content | string | ✅ | 댓글 내용 |

```json
{
  "content": "좋은 정보 감사합니다!"
}
```

**Response** `201 Created`

```json
{
  "id": 3,
  "user_email": "user@example.com",
  "username": "홍길동",
  "content": "좋은 정보 감사합니다!",
  "likes_count": 0,
  "is_liked": false,
  "is_author": true,
  "created_at": "2026-06-20T12:00:00+09:00",
  "updated_at": "2026-06-20T12:00:00+09:00"
}
```

---

### 7-9. 댓글 수정

**PUT** `/api/community/posts/{id}/comments/{comment_pk}/`  
인증 필요 · 작성자 본인만 가능 · 부분 수정 가능

**Request Body**

```json
{
  "content": "수정된 댓글 내용입니다."
}
```

**Response** `200 OK` — 수정된 댓글 반환

| HTTP 상태 | 의미 |
|-----------|------|
| 200 | 수정 성공 |
| 403 | 작성자 본인이 아님 |
| 404 | 댓글 없음 |

---

### 7-10. 댓글 삭제

**DELETE** `/api/community/posts/{id}/comments/{comment_pk}/`  
인증 필요 · 작성자 본인만 가능

**Response** `204 No Content`

| HTTP 상태 | 의미 |
|-----------|------|
| 204 | 삭제 성공 |
| 403 | 작성자 본인이 아님 |
| 404 | 댓글 없음 |

---

### 7-11. 게시글 좋아요 토글

**POST** `/api/community/posts/{id}/like/`  
인증 필요

이미 좋아요한 게시글이면 취소, 아니면 추가합니다.

**Response** `200 OK`

좋아요 추가 시:
```json
{
  "liked": true,
  "likes_count": 6
}
```

좋아요 취소 시:
```json
{
  "liked": false,
  "likes_count": 5
}
```

---

### 7-12. 댓글 좋아요 토글

**POST** `/api/community/posts/{id}/comments/{comment_pk}/like/`  
인증 필요

이미 좋아요한 댓글이면 취소, 아니면 추가합니다. 본인 댓글은 좋아요 불가합니다.

**Response** `200 OK`

좋아요 추가 시:
```json
{
  "liked": true,
  "likes_count": 4
}
```

좋아요 취소 시:
```json
{
  "liked": false,
  "likes_count": 3
}
```

| HTTP 상태 | 의미 |
|-----------|------|
| 200 | 성공 |
| 400 | 본인 댓글 좋아요 시도 |
| 404 | 댓글 없음 |

---

### 7-13. 조회수 증가

**POST** `/api/community/posts/{id}/view/`  
인증 불필요

게시글 조회수를 1 증가시킵니다. 게시글 상세 페이지 진입 시 별도로 호출해야 합니다.

**Response** `200 OK`

```json
{
  "views_count": 43
}
```

---

#### 게시글 카테고리 코드표

| 코드 | 의미 |
|------|------|
| `general` | 일반 |
| `review` | 카드 후기 |
| `question` | 질문 |
| `info` | 정보 |

---

*최종 업데이트: 2026-06-26*
