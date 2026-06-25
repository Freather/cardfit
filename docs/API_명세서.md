# CardFit API 紐낆꽭??
> Base URL: `http://localhost:8000`
> ?몄쬆 諛⑹떇: JWT Bearer Token
> Content-Type: `application/json`
> 理쒖쥌 ?낅뜲?댄듃: 2026-06-25

## 怨듯넻

### ?몄쬆 ?ㅻ뜑

濡쒓렇???먮뒗 ?뚯썝媛???묐떟??`tokens.access` 媛믪쓣 ?몄쬆???꾩슂??API???ы븿?⑸땲??

```http
Authorization: Bearer <access_token>
```

### 怨듯넻 ?먮윭 ?묐떟

```json
{
  "detail": "?먮윭 硫붿떆吏"
}
```

| HTTP ?곹깭 | ?섎? |
| --- | --- |
| 200 | ?깃났 |
| 201 | ?앹꽦 ?깃났 |
| 204 | ??젣/泥섎━ ?깃났, ?묐떟 蹂몃Ц ?놁쓬 |
| 400 | ?섎せ???붿껌 ?먮뒗 ?좏슚??寃利??ㅽ뙣 |
| 401 | ?몄쬆 ?꾩슂 ?먮뒗 ?좏겙 留뚮즺 |
| 403 | 沅뚰븳 ?놁쓬 |
| 404 | 由ъ냼???놁쓬 |
| 502 | ?몃? AI API 泥섎━ ?ㅽ뙣 |
| 503 | ?쒕쾭 ?ㅼ젙 ?먮뒗 ?몃? ?곕룞 以鍮?????|

### 二쇱슂 肄붾뱶媛?
| 援щ텇 | 肄붾뱶 |
| --- | --- |
| 移대뱶 ???| `credit`, `debit`, `prepaid` |
| ?쒗깮 移댄뀒怨좊━ | `food`, `transportation`, `fuel`, `shopping`, `entertainment`, `communication`, `travel`, `health`, `point`, `other` |
| 嫄곕옒/?뚮퉬 移댄뀒怨좊━ | `food`, `transport`, `fuel`, `shopping`, `entertainment`, `communication`, `health`, `other` |
| ?쒗깮 ???| `discount`, `cashback`, `point`, `mileage` |
| ?ㅻЦ ?낅젰 ???| `manual`, `csv`, `api` |
| ?곕졊? | `20s`, `30s`, `40s`, `50s`, `60s` |
| ?뚮뱷 ?섏? | `low`, `mid`, `high` |
| 寃뚯떆湲 移댄뀒怨좊━ | `general`, `review`, `question`, `info` |

## 1. Accounts

### 1-1. ?뚯썝媛??
`POST /api/accounts/register/`
?몄쬆 遺덊븘??
**Request**

```json
{
  "email": "user@example.com",
  "username": "移대뱶??,
  "password": "password123",
  "password_confirm": "password123"
}
```

**Response 201**

```json
{
  "message": "?뚯썝媛?낆씠 ?꾨즺?섏뿀?듬땲??",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "移대뱶??,
    "selected_card_id": null,
    "created_at": "2026-06-25T12:00:00+09:00",
    "updated_at": "2026-06-25T12:00:00+09:00"
  },
  "tokens": {
    "access": "<access_token>",
    "refresh": "<refresh_token>"
  }
}
```

### 1-2. 濡쒓렇??
`POST /api/accounts/login/`
?몄쬆 遺덊븘??
**Request**

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response 200**

```json
{
  "message": "濡쒓렇???깃났",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "移대뱶??,
    "selected_card_id": 3,
    "created_at": "2026-06-25T12:00:00+09:00",
    "updated_at": "2026-06-25T12:00:00+09:00"
  },
  "tokens": {
    "access": "<access_token>",
    "refresh": "<refresh_token>"
  }
}
```

### 1-3. 濡쒓렇?꾩썐

`POST /api/accounts/logout/`
?몄쬆 ?꾩슂

**Request**

```json
{
  "refresh": "<refresh_token>"
}
```

**Response 200**

```json
{
  "message": "濡쒓렇?꾩썐 ?꾨즺"
}
```

### 1-4. ?좏겙 媛깆떊

`POST /api/accounts/token/refresh/`
?몄쬆 遺덊븘??
**Request**

```json
{
  "refresh": "<refresh_token>"
}
```

**Response 200**

```json
{
  "access": "<new_access_token>",
  "refresh": "<new_refresh_token>"
}
```

### 1-5. ?꾨줈??議고쉶/?섏젙/?덊눜

`GET /api/accounts/profile/`
`PUT /api/accounts/profile/`
`DELETE /api/accounts/profile/`
?몄쬆 ?꾩슂

**PUT Request**

```json
{
  "username": "?덈땳?ㅼ엫"
}
```

**Response 200**

```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "?덈땳?ㅼ엫",
  "selected_card_id": 3,
  "created_at": "2026-06-25T12:00:00+09:00",
  "updated_at": "2026-06-25T12:30:00+09:00"
}
```

`DELETE`??怨꾩젙??鍮꾪솢?깊솕?섍퀬 `204 No Content`瑜?諛섑솚?⑸땲??

### 1-6. ???移대뱶 ?ㅼ젙

`PUT /api/accounts/select-card/`
?몄쬆 ?꾩슂

**Request**

```json
{
  "selected_card": 3
}
```

**Response 200**

```json
{
  "message": "???移대뱶媛 ?ㅼ젙?섏뿀?듬땲??",
  "selected_card_id": 3
}
```

### 1-7. ?뚯뀥 濡쒓렇??
| Method | URL | ?ㅻ챸 |
| --- | --- | --- |
| GET | `/api/accounts/oauth/kakao/` | 移댁뭅???몄쬆 ?섏씠吏濡?由щ떎?대젆??|
| GET | `/api/accounts/oauth/kakao/?debug=1` | 移댁뭅??OAuth ?ㅼ젙 ?뺤씤 |
| GET | `/api/accounts/oauth/kakao/callback/` | 移댁뭅??肄쒕갚 |
| GET | `/api/accounts/oauth/naver/` | ?ㅼ씠踰??몄쬆 ?섏씠吏濡?由щ떎?대젆??|
| GET | `/api/accounts/oauth/naver/callback/` | ?ㅼ씠踰?肄쒕갚 |
| POST | `/api/accounts/oauth/email/complete/` | ?뚯뀥 怨꾩젙 ?대찓??蹂댁셿 ??濡쒓렇???꾨즺 |

OAuth ?쒖옉 API??`next` 荑쇰━ ?뚮씪誘명꽣瑜?諛쏆쓣 ???덉뒿?덈떎.

**?대찓??蹂댁셿 Request**

```json
{
  "token": "<pending_oauth_email_token>",
  "email": "user@example.com",
  "next": "/profile"
}
```

**Response 200**

```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "移대뱶??,
    "selected_card_id": null,
    "created_at": "2026-06-25T12:00:00+09:00",
    "updated_at": "2026-06-25T12:00:00+09:00"
  },
  "tokens": {
    "access": "<access_token>",
    "refresh": "<refresh_token>"
  },
  "next": "/profile"
}
```

## 2. Cards

### 2-1. 移대뱶 紐⑸줉

`GET /api/cards/`
?몄쬆 遺덊븘??
**Query Parameters**

| ?대쫫 | ???| ?ㅻ챸 |
| --- | --- | --- |
| `card_type` | string | `credit`, `debit`, `prepaid` |
| `company` | string | 移대뱶?щ챸 遺遺?寃??|
| `max_annual_fee` | integer | ?고쉶鍮??곹븳 |

**Response 200**

```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "card_company": "?쇱꽦移대뱶",
      "card_name": "?쇱꽦 iD ON 移대뱶",
      "card_type": "credit",
      "card_type_display": "?좎슜移대뱶",
      "annual_fee": 20000,
      "min_prev_month_spending": 300000,
      "apply_url": "https://www.samsungcard.com",
      "image_url": "https://example.com/card.png",
      "benefit_count": 3,
      "benefits": [
        {
          "id": 1,
          "benefit_category": "food",
          "benefit_category_display": "?앸퉬",
          "benefit_type": "discount",
          "benefit_type_display": "?좎씤",
          "discount_rate": "10.00",
          "monthly_limit": 3000,
          "condition_description": "?꾩썡 ?ㅼ쟻 30留뚯썝 ?댁긽"
        }
      ],
      "is_wished": false,
      "synced_at": "2026-06-25T12:00:00+09:00"
    }
  ]
}
```

### 2-2. 移대뱶 ?곸꽭

`GET /api/cards/{id}/`
?몄쬆 遺덊븘??
?묐떟 ?꾨뱶??移대뱶 紐⑸줉??移대뱶 媛앹껜? 嫄곗쓽 媛숈쑝硫? `benefits` ?꾩껜 紐⑸줉???ы븿?⑸땲??

### 2-3. 移대뱶 ?쒗깮 紐⑸줉

`GET /api/cards/{id}/benefits/`
?몄쬆 遺덊븘??
**Query Parameters**

| ?대쫫 | ???| ?ㅻ챸 |
| --- | --- | --- |
| `category` | string | ?쒗깮 移댄뀒怨좊━ ?꾪꽣 |

**Response 200**

```json
[
  {
    "id": 1,
    "benefit_category": "food",
    "benefit_category_display": "?앸퉬",
    "benefit_type": "discount",
    "benefit_type_display": "?좎씤",
    "discount_rate": "10.00",
    "monthly_limit": 3000,
    "condition_description": "?꾩썡 ?ㅼ쟻 30留뚯썝 ?댁긽"
  }
]
```

### 2-4. 李?紐⑸줉

`GET /api/cards/wishlist/`
?몄쬆 ?꾩슂

**Response 200**

```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "user": 1,
      "card": {
        "id": 3,
        "card_company": "?쇱꽦移대뱶",
        "card_name": "?쇱꽦 iD ON 移대뱶",
        "card_type": "credit",
        "is_wished": true
      },
      "source": "detail",
      "created_at": "2026-06-25T12:00:00+09:00"
    }
  ]
}
```

### 2-5. 李?異붽?/??젣

`POST /api/cards/wishlist/`
`DELETE /api/cards/wishlist/{card_id}/`
?몄쬆 ?꾩슂

**POST Request**

```json
{
  "card_id": 3,
  "source": "detail"
}
```

`source` 媛믪? `search`, `detail`, `recommendation`, `compare` 以??섎굹?낅땲??

## 3. Spending Surveys

### 3-1. ?ㅻЦ 紐⑸줉/?앹꽦

`GET /api/spending/`
`POST /api/spending/`
?몄쬆 ?꾩슂

**POST Request**

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

**Response 200/201**

```json
{
  "id": 1,
  "input_type": "manual",
  "input_type_display": "吏곸젒?낅젰",
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
  "age_group_display": "30?",
  "max_annual_fee": 30000,
  "income_level": "mid",
  "income_level_display": "以묎컙",
  "transaction_count": 0,
  "transaction_start_date": null,
  "transaction_end_date": null,
  "created_at": "2026-06-25T12:00:00+09:00",
  "updated_at": "2026-06-25T12:00:00+09:00"
}
```

### 3-2. ?ㅻЦ ?곹깭

`GET /api/spending/status/`
?몄쬆 ?꾩슂

**Response 200**

```json
{
  "has_survey": true,
  "has_csv": true,
  "latest_survey_id": 1,
  "latest_csv_id": 2
}
```

### 3-3. ?ㅻЦ ?곸꽭/?섏젙/??젣

`GET /api/spending/{id}/`
`PUT /api/spending/{id}/`
`DELETE /api/spending/{id}/`
?몄쬆 ?꾩슂

?곸꽭 議고쉶???ㅻЦ ?묐떟 ?꾨뱶??`transactions` 諛곗뿴??異붽??⑸땲??
`PUT`? 遺遺??섏젙??媛?ν빀?덈떎. `DELETE`??`204 No Content`瑜?諛섑솚?⑸땲??

### 3-4. CSV ?낅줈??
`POST /api/spending/upload-csv/`
?몄쬆 ?꾩슂, `multipart/form-data`

?쇱꽦移대뱶 CSV瑜??뚯떛??`input_type: "csv"` ?ㅻЦ怨?嫄곕옒?댁뿭???앹꽦?⑸땲??

**Form Data**

| ?대쫫 | ???| ?꾩닔 | 湲곕낯媛?| ?ㅻ챸 |
| --- | --- | --- | --- | --- |
| `file` | file | O | - | `.csv`, 理쒕? 5MB |
| `age_group` | string | X | `30s` | ?곕졊? |
| `income_level` | string | X | `mid` | ?뚮뱷 ?섏? |
| `max_annual_fee` | integer | X | `100000` | 理쒕? ?고쉶鍮?|

**Response 201**

```json
{
  "message": "87嫄댁쓽 嫄곕옒?댁뿭??遺꾩꽍?덉뒿?덈떎.",
  "survey": {
    "id": 2,
    "input_type": "csv",
    "total_monthly": 838000,
    "transaction_count": 87,
    "transaction_start_date": "2026-04-01",
    "transaction_end_date": "2026-05-31",
    "transactions": [
      {
        "id": 1,
        "survey": 2,
        "category": "food",
        "category_display": "?앸퉬",
        "merchant": "?ㅽ?踰낆뒪 媛뺣궓??,
        "amount": 6500,
        "transaction_date": "2026-05-31"
      }
    ]
  }
}
```

## 4. Transactions

### 4-1. 嫄곕옒?댁뿭 紐⑸줉/?앹꽦

`GET /api/transactions/`
`POST /api/transactions/`
?몄쬆 ?꾩슂

**GET Query Parameters**

| ?대쫫 | ???| ?ㅻ챸 |
| --- | --- | --- |
| `survey_id` | integer | ?뱀젙 ?ㅻЦ??嫄곕옒?댁뿭留?議고쉶 |
| `category` | string | 嫄곕옒 移댄뀒怨좊━ ?꾪꽣 |

**POST Request**

```json
{
  "survey_id": 1,
  "category": "food",
  "merchant": "?ㅽ?踰낆뒪 媛뺣궓??,
  "amount": 6500,
  "transaction_date": "2026-05-31"
}
```

**Response 200/201**

```json
{
  "id": 1,
  "survey": 1,
  "category": "food",
  "category_display": "?앸퉬",
  "merchant": "?ㅽ?踰낆뒪 媛뺣궓??,
  "amount": 6500,
  "transaction_date": "2026-05-31"
}
```

### 4-2. 嫄곕옒?댁뿭 ?곸꽭/?섏젙/??젣

`GET /api/transactions/{id}/`
`PUT /api/transactions/{id}/`
`DELETE /api/transactions/{id}/`
?몄쬆 ?꾩슂

`PUT`? `category`, `merchant`, `amount`, `transaction_date` 遺遺??섏젙??媛?ν빀?덈떎.
`DELETE`??`204 No Content`瑜?諛섑솚?⑸땲??

## 5. Reports

紐⑤뱺 由ы룷??API???몄쬆???꾩슂?⑸땲??

### 5-1. ?뚮퉬 ?붿빟

`GET /api/reports/spending-summary/`

理쒓렐 `manual` ?ㅻЦ???좏샇 議곌굔?쇰줈, 理쒓렐 `csv` ?ㅻЦ???ㅼ젣 ?뚮퉬 ?곗씠?곕줈 ?ъ슜?⑸땲??

**Response 200**

```json
{
  "survey_id": 2,
  "input_type": "csv",
  "categories": {
    "food": 312400,
    "transport": 95600,
    "fuel": 0,
    "shopping": 288000,
    "entertainment": 42000,
    "communication": 55000,
    "health": 20000,
    "other": 45000
  },
  "food_monthly": 312400,
  "transport_monthly": 95600,
  "fuel_monthly": 0,
  "shopping_monthly": 288000,
  "entertainment_monthly": 42000,
  "communication_monthly": 55000,
  "health_monthly": 20000,
  "other_monthly": 45000,
  "total_monthly": 858000,
  "preference_survey_id": 1,
  "age_group": "30s",
  "income_level": "mid",
  "max_annual_fee": 30000,
  "transaction_start_date": "2026-04-01",
  "transaction_end_date": "2026-05-31",
  "created_at": "2026-06-25T12:00:00+09:00"
}
```

### 5-2. 移댄뀒怨좊━ 遺꾩꽍

`GET /api/reports/category-breakdown/`

**Query Parameters**

| ?대쫫 | ???| ?ㅻ챸 |
| --- | --- | --- |
| `survey_id` | integer | ?뱀젙 CSV ?ㅻЦ 湲곗? 遺꾩꽍. ?놁쑝硫?理쒓렐 CSV ?ㅻЦ ?ъ슜 |

**Response 200**

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
    }
  ]
}
```

### 5-3. ?붾퀎 異붿씠

`GET /api/reports/monthly-trend/`

濡쒓렇???ъ슜?먯쓽 紐⑤뱺 CSV 嫄곕옒?댁뿭????移댄뀒怨좊━蹂꾨줈 吏묎퀎?⑸땲??

**Response 200**

```json
{
  "trend": {
    "2026-04": {
      "food": 280000,
      "transport": 75000
    },
    "2026-05": {
      "food": 312400,
      "shopping": 288000
    }
  }
}
```

### 5-4. ?곸쐞 媛留뱀젏

`GET /api/reports/top-merchants/`

**Query Parameters**

| ?대쫫 | ???| 湲곕낯媛?| ?ㅻ챸 |
| --- | --- | --- | --- |
| `limit` | integer | `10` | 諛섑솚??媛留뱀젏 ??|

**Response 200**

```json
{
  "results": [
    {
      "merchant": "?좏뵆?ㅽ넗??媛뺣궓",
      "category": "shopping",
      "total": 174600,
      "count": 2
    }
  ]
}
```

## 6. AI

AI API??紐⑤몢 ?몄쬆???꾩슂?섎ŉ, ?쒕쾭??`GMS_API_KEY`媛 ?ㅼ젙?섏뼱 ?덉뼱???⑸땲??

### 6-1. AI 移대뱶 異붿쿇

`GET /api/ai/recommend/`
`POST /api/ai/recommend/`

`GET`? 理쒖떊 `manual` ?ㅻЦ怨?理쒖떊 ?먮뒗 吏?뺥븳 `csv` ?ㅻЦ??紐⑤몢 ?덉뼱???⑸땲??

**GET Query Parameters**

| ?대쫫 | ???| ?ㅻ챸 |
| --- | --- | --- |
| `survey_id` | integer | ?뱀젙 CSV ?ㅻЦ 湲곗? 異붿쿇 |
| `top` | integer | ?묐떟 異붿쿇 媛쒖닔 ?쒗븳 |

**GET Response 200**

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
    "health_monthly": 20000,
    "other_monthly": 45000,
    "total_monthly": 858000,
    "max_annual_fee": 30000
  },
  "recommendations": [
    {
      "card_id": 4,
      "card_name": "?쇱꽦 iD ON 移대뱶",
      "card_company": "?쇱꽦移대뱶",
      "annual_fee": 20000,
      "apply_url": "https://www.samsungcard.com",
      "rank": 1,
      "reason": "異붿쿇 ?ъ쑀",
      "expected_monthly_benefit": "??15,000??,
      "net_benefit": "??160,000??,
      "benefit_details": "二쇱슂 ?쒗깮 ?ㅻ챸"
    }
  ],
  "spending_insight": "?뚮퉬 ?⑦꽩 遺꾩꽍 臾몄옣"
}
```

**POST Request**

```json
{
  "food_monthly": 400000,
  "transport_monthly": 60000,
  "fuel_monthly": 0,
  "shopping_monthly": 150000,
  "entertainment_monthly": 50000,
  "communication_monthly": 55000,
  "health_monthly": 20000,
  "other_monthly": 30000,
  "max_annual_fee": 15000
}
```

`POST` ?묐떟? AI媛 ?앹꽦??`recommendations`, `spending_insight` 援ъ“瑜?諛섑솚?⑸땲??

### 6-2. ?뱀젙 移대뱶 AI 異붿쿇 ?ъ쑀

`GET /api/ai/cards/{card_id}/reason/`

**Query Parameters**

| ?대쫫 | ???| ?ㅻ챸 |
| --- | --- | --- |
| `survey_id` | integer | ?뱀젙 CSV ?ㅻЦ 湲곗? ?ъ쑀 ?앹꽦 |

**Response 200**

```json
{
  "card_id": 4,
  "card_name": "?쇱꽦 iD ON 移대뱶",
  "card_company": "?쇱꽦移대뱶",
  "reason": "??移대뱶媛 ?곹빀???댁쑀",
  "expected_monthly_benefit": "??15,000??,
  "tip": "?쒖슜 ??
}
```

### 6-3. 湲덉쑖/移대뱶 梨쀫큸

`POST /api/ai/chat/`

**Request**

```json
{
  "messages": [
    {
      "role": "user",
      "content": "???뚮퉬 ?⑦꽩??留욌뒗 移대뱶瑜??뚮젮以?
    }
  ],
  "page_context": {
    "route_name": "report",
    "path": "/report",
    "visible_heading": "?뚮퉬 由ы룷??,
    "page_kind": "?뚮퉬 由ы룷???섏씠吏",
    "params": {},
    "query": {}
  }
}
```

`messages`??`role`? `user`, `assistant`留??ъ슜?⑸땲?? ?쒕쾭??理쒓렐 8媛?硫붿떆吏留?AI???꾨떖?⑸땲??

**Response 200**

```json
{
  "reply": "梨쀫큸 ?듬?"
}
```

## 7. Community

?쎄린 API ?쇰???鍮꾨줈洹몄씤??媛?ν븯怨? ?묒꽦/?섏젙/??젣/醫뗭븘?붾뒗 ?몄쬆???꾩슂?⑸땲??

### 7-1. 寃뚯떆湲 紐⑸줉/?묒꽦

`GET /api/community/posts/`
`POST /api/community/posts/`

**GET Query Parameters**

| ?대쫫 | ???| ?ㅻ챸 |
| --- | --- | --- |
| `category` | string | 寃뚯떆湲 移댄뀒怨좊━ ?꾪꽣 |
| `search` | string | ?쒕ぉ/?댁슜 寃??|
| `page` | integer | ?섏씠吏 踰덊샇 |
| `page_size` | integer | ?섏씠吏 ?ш린, 理쒕? 50 |

**GET Response 200**

```json
{
  "count": 42,
  "next": "http://localhost:8000/api/community/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user_email": "user@example.com",
      "username": "移대뱶??,
      "title": "移대뱶 ?ъ슜 ?꾧린",
      "category": "review",
      "views_count": 120,
      "likes_count": 15,
      "comments_count": 5,
      "is_liked": false,
      "is_author": true,
      "created_at": "2026-06-25T12:00:00+09:00"
    }
  ]
}
```

**POST Request**

```json
{
  "title": "?쇱꽦移대뱶 iD ON ?ъ슜 ?꾧린",
  "content": "?앸퉬 ?좎씤 ?쒗깮??醫뗭븯?듬땲??",
  "category": "review"
}
```

### 7-2. ?멸린 寃뚯떆湲

`GET /api/community/posts/popular/`
?몄쬆 遺덊븘??
醫뗭븘???? 議고쉶??湲곗??쇰줈 ?곸쐞 10媛?寃뚯떆湲??諛섑솚?⑸땲??

### 7-3. 寃뚯떆湲 ?곸꽭/?섏젙/??젣

`GET /api/community/posts/{id}/`
`PUT /api/community/posts/{id}/`
`DELETE /api/community/posts/{id}/`

`GET`? ?몄쬆 遺덊븘?? `PUT`/`DELETE`???묒꽦???몄쬆???꾩슂?⑸땲??

**Detail Response 200**

```json
{
  "id": 1,
  "user_email": "user@example.com",
  "username": "移대뱶??,
  "title": "?쇱꽦移대뱶 iD ON ?ъ슜 ?꾧린",
  "content": "?앸퉬 ?좎씤 ?쒗깮??醫뗭븯?듬땲??",
  "category": "review",
  "views_count": 42,
  "likes_count": 5,
  "comments_count": 2,
  "comments": [
    {
      "id": 1,
      "user_email": "other@example.com",
      "username": "?ㅻⅨ?ъ슜??,
      "content": "醫뗭? ?뺣낫 媛먯궗?⑸땲??",
      "likes_count": 1,
      "is_liked": false,
      "is_author": false,
      "created_at": "2026-06-25T12:10:00+09:00",
      "updated_at": "2026-06-25T12:10:00+09:00"
    }
  ],
  "is_liked": false,
  "is_author": true,
  "created_at": "2026-06-25T12:00:00+09:00",
  "updated_at": "2026-06-25T12:00:00+09:00"
}
```

### 7-4. ?볤? 紐⑸줉/?묒꽦

`GET /api/community/posts/{id}/comments/`
`POST /api/community/posts/{id}/comments/`

`GET`? ?몄쬆 遺덊븘?? `POST`???몄쬆 ?꾩슂?낅땲??

**POST Request**

```json
{
  "content": "醫뗭? ?뺣낫 媛먯궗?⑸땲??"
}
```

### 7-5. ?볤? ?섏젙/??젣

`PUT /api/community/posts/{id}/comments/{comment_id}/`
`DELETE /api/community/posts/{id}/comments/{comment_id}/`
?묒꽦???몄쬆 ?꾩슂

**PUT Request**

```json
{
  "content": "?섏젙???볤? ?댁슜?낅땲??"
}
```

### 7-6. 寃뚯떆湲 醫뗭븘???좉?

`POST /api/community/posts/{id}/like/`
?몄쬆 ?꾩슂

**Response 200**

```json
{
  "liked": true,
  "likes_count": 6
}
```

### 7-7. ?볤? 醫뗭븘???좉?

`POST /api/community/posts/{id}/comments/{comment_id}/like/`
?몄쬆 ?꾩슂

蹂몄씤 ?볤??먮뒗 醫뗭븘?붾? ?꾨? ???놁뒿?덈떎.

**Response 200**

```json
{
  "liked": true,
  "likes_count": 2
}
```

### 7-8. 寃뚯떆湲 議고쉶??利앷?

`POST /api/community/posts/{id}/view/`
?몄쬆 遺덊븘??
**Response 200**

```json
{
  "views_count": 43
}
```
