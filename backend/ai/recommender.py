import json
from openai import OpenAI
from django.conf import settings
from cards.models import Card


def _build_client():
    base_url = settings.GMS_API_BASE_URL
    # SSAFY에서 full endpoint URL을 줄 경우 /chat/completions 제거
    # OpenAI SDK가 base_url에 자동으로 /chat/completions 를 붙이기 때문
    if base_url.endswith('/chat/completions'):
        base_url = base_url[: -len('/chat/completions')]
    return OpenAI(
        api_key=settings.GMS_API_KEY,
        base_url=base_url,
    )


def _build_cards_context(max_annual_fee: int) -> list[dict]:
    cards = Card.objects.prefetch_related('benefits').filter(
        annual_fee__lte=max_annual_fee
    )
    result = []
    for card in cards:
        benefits_text = " / ".join([
            f"{b.get_benefit_category_display()} {b.discount_rate}% {b.get_benefit_type_display()}"
            + (f" (월{b.monthly_limit:,}원 한도)" if b.monthly_limit else "")
            for b in card.benefits.all()
        ])
        result.append({
            "id": card.id,
            "name": card.card_name,
            "type": card.get_card_type_display(),
            "annual_fee": card.annual_fee,
            "min_spending": card.min_prev_month_spending,
            "benefits": benefits_text or "기본 캐시백",
            "apply_url": card.apply_url,
        })
    return result


def _build_prompt(survey, cards_context: list[dict]) -> str:
    spending = {
        "식비": survey.food_monthly,
        "교통": survey.transport_monthly,
        "주유": survey.fuel_monthly,
        "쇼핑": survey.shopping_monthly,
        "여가/문화": survey.entertainment_monthly,
        "통신": survey.communication_monthly,
        "의료/건강": survey.health_monthly,
        "기타": survey.other_monthly,
    }
    total = sum(spending.values())
    cards_text = "\n".join([
        f"[카드 ID: {c['id']}] {c['name']} ({c['type']}) | 연회비 {c['annual_fee']:,}원 | "
        f"전월 실적 {c['min_spending']:,}원 이상 | 혜택: {c['benefits']}"
        for c in cards_context
    ])

    return f"""당신은 삼성카드 전문 AI 상담사입니다. 사용자의 소비 패턴을 분석하여 삼성카드 상품 중 최적의 카드 3개를 추천해주세요.

[사용자 월 소비 패턴]
{json.dumps(spending, ensure_ascii=False, indent=2)}
월 총 지출: {total:,}원
최대 허용 연회비: {survey.max_annual_fee:,}원

[추천 가능한 삼성카드 목록]
{cards_text}

[응답 형식 - 반드시 아래 JSON 형식으로만 응답하세요]
{{
  "recommendations": [
    {{
      "card_id": <카드 ID 숫자>,
      "card_name": "<카드명>",
      "rank": 1,
      "reason": "<이 카드가 사용자에게 적합한 구체적인 이유 2~3문장>",
      "expected_monthly_benefit": "<예상 월 혜택 금액 또는 설명>",
      "tip": "<이 카드를 최대한 활용하는 팁 1문장>"
    }}
  ],
  "spending_insight": "<사용자 소비 패턴에 대한 전반적인 AI 분석 2~3문장>"
}}"""


def get_gms_recommendations(survey) -> dict:
    cards_context = _build_cards_context(survey.max_annual_fee)
    if not cards_context:
        return {"error": "조건에 맞는 삼성카드가 없습니다.", "recommendations": []}

    prompt = _build_prompt(survey, cards_context)

    try:
        client = _build_client()
        response = client.chat.completions.create(
            model=settings.GMS_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "당신은 삼성카드 AI 추천 서비스입니다. 반드시 요청된 JSON 형식으로만 응답하세요.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        raw = response.choices[0].message.content.strip()

        # JSON 파싱 (마크다운 코드블록 감싸진 경우 제거)
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw)

    except Exception as e:
        return {"error": str(e), "recommendations": [], "spending_insight": ""}
