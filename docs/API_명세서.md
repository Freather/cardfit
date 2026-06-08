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

## 2. Cards — 카드

### 2-1. 카드 목록 조회

**GET** `/api/cards/`  
인증 불필요

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
      "benefit_count": 3,
      "synced_at": "2026-06-01T00:00:00Z"
    }
  ]
}
```

---

### 2-2. 카드 상세 조회

**GET** `/api/cards/{id}/`  
인증 불필요

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
| category | string | 혜택 카테고리 필터 | `food` / `transport` / `shopping` |

**Response** `200 OK` — 혜택 배열 반환

---

#### 카드 카테고리 코드표

| 코드 | 의미 |
|------|------|
| `food` | 식비 |
| `transport` | 교통 |
| `shopping` | 쇼핑 |
| `entertainment` | 여가/문화 |
| `communication` | 통신 |
| `travel` | 여행 |
| `health` | 의료/건강 |
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
    "shopping_monthly": 200000,
    "entertainment_monthly": 50000,
    "communication_monthly": 55000,
    "other_monthly": 30000,
    "total_monthly": 715000,
    "age_group": "30s",
    "age_group_display": "30대",
    "max_annual_fee": 30000,
    "income_level": "mid",
    "income_level_display": "중소득",
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
| shopping_monthly | integer | | 월 쇼핑비 (원) |
| entertainment_monthly | integer | | 월 여가비 (원) |
| communication_monthly | integer | | 월 통신비 (원) |
| other_monthly | integer | | 월 기타 지출 (원) |
| age_group | string | ✅ | `20s` / `30s` / `40s` / `50s` / `60s` |
| max_annual_fee | integer | ✅ | 최대 연회비 (원) |
| income_level | string | ✅ | `low` / `mid` / `high` |

```json
{
  "input_type": "manual",
  "food_monthly": 300000,
  "transport_monthly": 80000,
  "shopping_monthly": 200000,
  "entertainment_monthly": 50000,
  "communication_monthly": 55000,
  "other_monthly": 30000,
  "age_group": "30s",
  "max_annual_fee": 30000,
  "income_level": "mid"
}
```

**Response** `201 Created` — 생성된 설문 반환

---

### 3-3. 설문 상세 조회

**GET** `/api/spending/{id}/`  
인증 필요

거래내역(`transactions`)을 포함하여 반환합니다.

**Response** `200 OK`

```json
{
  "id": 1,
  "input_type": "csv",
  "food_monthly": 250000,
  "transport_monthly": 95000,
  ...
  "total_monthly": 695000,
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

### 3-4. 설문 수정

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

### 3-5. 설문 삭제

**DELETE** `/api/spending/{id}/`  
인증 필요

연결된 거래내역도 함께 삭제됩니다.

**Response** `204 No Content`

---

### 3-6. CSV 파일 업로드

**POST** `/api/spending/upload-csv/`  
인증 필요 · `Content-Type: multipart/form-data`

삼성카드 CSV 포맷을 파싱하여 설문 + 거래내역을 자동 생성합니다.

**Request Form Data**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| file | file | ✅ | `.csv` 파일 (최대 5MB) |

**Response** `201 Created`

```json
{
  "message": "87건의 거래내역이 분석되었습니다.",
  "survey": {
    "id": 2,
    "input_type": "csv",
    "food_monthly": 312400,
    "transport_monthly": 95600,
    "shopping_monthly": 288000,
    "entertainment_monthly": 42000,
    "communication_monthly": 55000,
    "other_monthly": 45000,
    "total_monthly": 838000,
    "transactions": [ ... ]
  }
}
```

> CSV 업로드 후 `age_group`, `max_annual_fee`, `income_level`은 기본값으로 저장됩니다.  
> `/api/spending/{id}/` PUT으로 이후 수정하세요.

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
| category | string | ✅ | `food` / `transport` / `shopping` / `entertainment` / `communication` / `health` / `other` |
| merchant | string | ✅ | 가맹점명 |
| amount | integer | ✅ | 금액 (원, 음수 불가) |
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

## 5. Reports — 리포트

> 모든 리포트 API는 인증이 필요하며, 로그인한 사용자의 데이터만 조회합니다.

---

### 5-1. 월 지출 요약

**GET** `/api/reports/spending-summary/`  
인증 필요

가장 최근 설문 기준으로 카테고리별 월 지출 요약을 반환합니다.

**Response** `200 OK`

```json
{
  "survey_id": 1,
  "input_type": "csv",
  "categories": {
    "food": 312400,
    "transport": 95600,
    "shopping": 288000,
    "entertainment": 42000,
    "communication": 55000,
    "other": 45000
  },
  "total_monthly": 838000,
  "age_group": "30s",
  "income_level": "mid",
  "max_annual_fee": 30000,
  "created_at": "2026-06-08T12:00:00+09:00"
}
```

---

### 5-2. 카테고리별 비율 분석

**GET** `/api/reports/category-breakdown/`  
인증 필요

**Query Parameters**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| survey_id | integer | 특정 설문 ID 지정 (미입력 시 전체) |

**Response** `200 OK`

```json
{
  "total": 838000,
  "breakdown": [
    { "category": "food",          "total": 312400, "count": 42, "ratio": 37.3 },
    { "category": "shopping",      "total": 288000, "count": 18, "ratio": 34.4 },
    { "category": "transport",     "total": 95600,  "count": 15, "ratio": 11.4 },
    { "category": "communication", "total": 55000,  "count": 1,  "ratio": 6.6  },
    { "category": "other",         "total": 45000,  "count": 7,  "ratio": 5.4  },
    { "category": "entertainment", "total": 42000,  "count": 4,  "ratio": 5.0  }
  ]
}
```

---

### 5-3. 월별 지출 트렌드

**GET** `/api/reports/monthly-trend/`  
인증 필요

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

**Query Parameters**

| 파라미터 | 타입 | 기본값 | 설명 |
|----------|------|--------|------|
| limit | integer | 10 | 반환할 가맹점 수 |

**Response** `200 OK`

```json
{
  "results": [
    { "merchant": "홈플러스 강남점",    "category": "shopping", "total": 174600, "count": 2 },
    { "merchant": "무신사 주식회사",    "category": "shopping", "total": 158000, "count": 2 },
    { "merchant": "에스케이텔레콤 (주)", "category": "communication", "total": 110000, "count": 2 }
  ]
}
```

---

## 6. AI — 카드 추천

### 6-1. 설문 기반 카드 추천 (GET)

**GET** `/api/ai/recommend/`  
인증 필요

저장된 설문 데이터를 기반으로 최적 카드를 추천합니다.

**Query Parameters**

| 파라미터 | 타입 | 기본값 | 설명 |
|----------|------|--------|------|
| survey_id | integer | | 특정 설문 ID (미입력 시 최신 설문 사용) |
| top | integer | 5 | 추천 카드 수 (최대 10) |

**Response** `200 OK`

```json
{
  "survey_id": 1,
  "based_on": {
    "food_monthly": 300000,
    "transport_monthly": 80000,
    "shopping_monthly": 200000,
    "entertainment_monthly": 50000,
    "communication_monthly": 55000,
    "other_monthly": 30000,
    "max_annual_fee": 30000
  },
  "recommendations": [
    {
      "card_id": 4,
      "card_company": "신한카드",
      "card_name": "신한 Mr. Life 카드",
      "card_type": "credit",
      "annual_fee": 30000,
      "apply_url": "https://www.shinhancard.com",
      "total_annual_savings": 102600,
      "annual_fee": 30000,
      "net_benefit": 72600,
      "benefit_details": [
        {
          "category": "food",
          "discount_rate": 5.0,
          "monthly_spending": 300000,
          "monthly_savings": 15000,
          "annual_savings": 180000
        }
      ]
    }
  ]
}
```

---

### 6-2. 즉석 지출 입력 추천 (POST)

**POST** `/api/ai/recommend/`  
인증 필요

설문을 저장하지 않고 즉석에서 지출을 입력해 카드를 추천받습니다.

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| food_monthly | integer | | 월 식비 (원) |
| transport_monthly | integer | | 월 교통비 (원) |
| shopping_monthly | integer | | 월 쇼핑비 (원) |
| entertainment_monthly | integer | | 월 여가비 (원) |
| communication_monthly | integer | | 월 통신비 (원) |
| other_monthly | integer | | 월 기타 지출 (원) |
| max_annual_fee | integer | | 최대 연회비 (기본값: 200,000원) |
| top | integer | | 추천 카드 수 (기본값: 5, 최대 10) |

```json
{
  "food_monthly": 400000,
  "transport_monthly": 60000,
  "shopping_monthly": 150000,
  "communication_monthly": 55000,
  "max_annual_fee": 15000,
  "top": 3
}
```

**Response** `200 OK`

```json
{
  "recommendations": [
    {
      "card_id": 1,
      "card_company": "삼성카드",
      "card_name": "삼성 iD ON 카드",
      "annual_fee": 0,
      "total_annual_savings": 48000,
      "net_benefit": 48000,
      "benefit_details": [ ... ]
    }
  ]
}
```

---

## 추천 알고리즘 설명

**net_benefit 점수** = 연간 예상 절감액 합계 − 연회비

```
연간 절감액 = Σ (월 지출 × 할인율, min(월한도)) × 12
```

- `max_annual_fee` 이하인 카드만 후보에 포함
- `net_benefit` 내림차순 정렬 후 상위 N개 반환

---

*최종 업데이트: 2026-06-08*
