import json
from openai import OpenAI
from django.conf import settings
from django.db.models import Count, Max, Min, Sum
from django.db.models.functions import TruncMonth
from cards.models import Card
from surveys.models import SpendingTransaction, UserSurvey
from surveys.utils import build_monthly_average_by_category, count_transaction_months


CATEGORY_LABELS = {
    'food': '식비',
    'transport': '교통',
    'transportation': '교통',
    'fuel': '주유',
    'shopping': '쇼핑',
    'entertainment': '여가/문화',
    'communication': '통신',
    'health': '의료/건강',
    'other': '기타',
}

AGE_GROUP_LABELS = {
    '20s': '20대',
    '30s': '30대',
    '40s': '40대',
    '50s': '50대',
    '60s': '60대 이상',
}

INCOME_LEVEL_LABELS = {
    'low': '저소득',
    'mid': '중간',
    'high': '고소득',
}

BENEFIT_CATEGORY_BY_SPENDING = {
    'food': 'food',
    'transport': 'transportation',
    'fuel': 'fuel',
    'shopping': 'shopping',
    'entertainment': 'entertainment',
    'communication': 'communication',
    'health': 'health',
    'other': 'other',
}


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


def _format_won(value) -> str:
    return f"{int(value or 0):,}원"


def _format_date(value) -> str:
    return value.isoformat() if value else '정보 없음'


def _safe_context_text(value, limit: int = 120) -> str:
    text = str(value or '').replace('\n', ' ').strip()
    return text[:limit]


def _build_page_chat_context(page_context: dict | None) -> str:
    if not isinstance(page_context, dict) or not page_context:
        return '[현재 페이지 맥락]\n- 현재 페이지 정보가 전달되지 않았습니다.'

    route_name = _safe_context_text(page_context.get('route_name'), 60)
    page_kind = _safe_context_text(page_context.get('page_kind'), 80)
    path = _safe_context_text(page_context.get('path'), 120)
    visible_heading = _safe_context_text(page_context.get('visible_heading'), 120)
    visible_subheading = _safe_context_text(page_context.get('visible_subheading'), 120)
    params = page_context.get('params') if isinstance(page_context.get('params'), dict) else {}
    query = page_context.get('query') if isinstance(page_context.get('query'), dict) else {}

    lines = [
        '[현재 페이지 맥락]',
        f"- 페이지 종류: {page_kind or '정보 없음'}",
        f"- 라우트: {route_name or '정보 없음'}",
        f"- 경로: {path or '정보 없음'}",
    ]

    if visible_heading:
        lines.append(f"- 화면 제목: {visible_heading}")
    if visible_subheading and visible_subheading != visible_heading:
        lines.append(f"- 화면 보조 제목: {visible_subheading}")

    if params:
        safe_params = {
            _safe_context_text(key, 40): _safe_context_text(value, 80)
            for key, value in params.items()
        }
        lines.append(f"- 라우트 파라미터: {json.dumps(safe_params, ensure_ascii=False)}")

    if query:
        safe_query = {
            _safe_context_text(key, 40): _safe_context_text(value, 80)
            for key, value in query.items()
        }
        lines.append(f"- 쿼리: {json.dumps(safe_query, ensure_ascii=False)}")

    card_id = params.get('id') if route_name == 'card-detail' else None
    if card_id:
        try:
            card = Card.objects.prefetch_related('benefits').get(pk=card_id)
            benefits = [
                (
                    f"{CATEGORY_LABELS.get(benefit.benefit_category, benefit.get_benefit_category_display())} "
                    f"{benefit.discount_rate}% {benefit.get_benefit_type_display()}"
                    + (f", 월 한도 {_format_won(benefit.monthly_limit)}" if benefit.monthly_limit else '')
                )
                for benefit in card.benefits.all()
            ]
            lines.extend([
                '[현재 보고 있는 카드]',
                f"- 카드명: {card.card_company} {card.card_name}",
                f"- 카드 유형: {card.get_card_type_display()}",
                f"- 연회비: {_format_won(card.annual_fee)}",
                f"- 전월 실적: {_format_won(card.min_prev_month_spending)}",
                f"- 주요 혜택: {' / '.join(benefits[:6]) if benefits else '등록된 혜택 정보 없음'}",
            ])
        except (Card.DoesNotExist, ValueError, TypeError):
            lines.append('- 현재 카드 상세 정보를 DB에서 찾지 못했습니다.')

    lines.extend([
        '[페이지 답변 지침]',
        '- 사용자가 "이거", "여기", "현재 페이지", "이 카드"라고 말하면 위 현재 페이지 맥락을 우선 참조하세요.',
        '- 현재 페이지에서 할 수 있는 다음 행동이 있으면 CardFit 메뉴명 기준으로 짧게 안내하세요.',
    ])
    return '\n'.join(lines)


def _get_monthly_categories(survey) -> dict:
    if not survey:
        return {}

    transactions = list(survey.transactions.all())
    if survey.input_type == 'csv' and transactions:
        averages = build_monthly_average_by_category(transactions)
        return {
            category: int(averages.get(category, 0) or 0)
            for category in CATEGORY_LABELS
            if category != 'transportation'
        }

    return {
        'food': survey.food_monthly,
        'transport': survey.transport_monthly,
        'fuel': survey.fuel_monthly,
        'shopping': survey.shopping_monthly,
        'entertainment': survey.entertainment_monthly,
        'communication': survey.communication_monthly,
        'health': survey.health_monthly,
        'other': survey.other_monthly,
    }


def _build_relevant_cards_context(monthly_categories: dict, max_annual_fee: int, limit: int = 8) -> str:
    if not monthly_categories:
        return '사용자 소비 카테고리 정보가 부족해 관련 카드 후보를 좁히지 못했습니다.'

    top_categories = [
        category
        for category, amount in sorted(monthly_categories.items(), key=lambda item: item[1], reverse=True)
        if amount > 0
    ][:3]
    benefit_categories = [
        BENEFIT_CATEGORY_BY_SPENDING.get(category, category)
        for category in top_categories
    ]

    cards = (
        Card.objects
        .prefetch_related('benefits')
        .filter(annual_fee__lte=max_annual_fee or 999999999)
        .filter(benefits__benefit_category__in=benefit_categories)
        .distinct()[:limit]
    )

    lines = []
    for card in cards:
        benefits = [
            (
                f"{CATEGORY_LABELS.get(benefit.benefit_category, benefit.get_benefit_category_display())} "
                f"{benefit.discount_rate}% {benefit.get_benefit_type_display()}"
                + (f", 월 한도 {_format_won(benefit.monthly_limit)}" if benefit.monthly_limit else '')
            )
            for benefit in card.benefits.all()
            if benefit.benefit_category in benefit_categories
        ]
        if not benefits:
            continue
        lines.append(
            f"- {card.card_company} {card.card_name}: 연회비 {_format_won(card.annual_fee)}, "
            f"전월 실적 {_format_won(card.min_prev_month_spending)}, 주요 혜택 {' / '.join(benefits[:3])}"
        )

    return '\n'.join(lines) if lines else '현재 소비 상위 카테고리에 바로 매칭되는 카드 후보가 없습니다.'


def _build_user_chat_context(user) -> str:
    if not user or not getattr(user, 'is_authenticated', False):
        return '로그인 사용자 정보가 없어 개인 소비 리포트 컨텍스트를 사용할 수 없습니다.'

    preference_survey = UserSurvey.objects.filter(user=user, input_type='manual').first()
    spending_survey = (
        UserSurvey.objects
        .filter(user=user, input_type='csv')
        .prefetch_related('transactions')
        .first()
    )

    if not preference_survey and not spending_survey:
        return (
            '이 사용자는 아직 수동 설문과 CSV 소비 데이터를 등록하지 않았습니다. '
            '개인화 답변 대신 일반적인 카드/소비 리포트 안내를 제공하세요.'
        )

    source_survey = spending_survey or preference_survey
    preference = preference_survey or spending_survey
    monthly_categories = _get_monthly_categories(source_survey)
    total_monthly = sum(monthly_categories.values())
    sorted_categories = sorted(monthly_categories.items(), key=lambda item: item[1], reverse=True)
    non_zero_categories = [(category, amount) for category, amount in sorted_categories if amount > 0]

    lines = [
        '[사용자 개인화 컨텍스트]',
        f"- 분석 데이터: {'CSV 거래내역 기반 소비 리포트' if spending_survey else '수동 설문 기반'}",
        f"- 월평균 총지출: {_format_won(total_monthly)}",
    ]

    if preference:
        lines.extend([
            f"- 연령대: {AGE_GROUP_LABELS.get(preference.age_group, preference.age_group or '정보 없음')}",
            f"- 소득 수준: {INCOME_LEVEL_LABELS.get(preference.income_level, preference.income_level or '정보 없음')}",
            f"- 희망 최대 연회비: {_format_won(preference.max_annual_fee)}",
        ])

    if spending_survey:
        transactions = spending_survey.transactions.all()
        period = transactions.aggregate(start_date=Min('transaction_date'), end_date=Max('transaction_date'))
        month_count = count_transaction_months(transactions.only('transaction_date'))
        lines.extend([
            f"- CSV 거래 기간: {_format_date(period['start_date'])} ~ {_format_date(period['end_date'])}",
            f"- 리포트 계산 방식: CSV 전체 거래를 {month_count}개월로 나누어 월평균 카테고리 지출을 산출",
        ])

    if non_zero_categories:
        lines.append('- 월평균 카테고리별 지출:')
        for category, amount in non_zero_categories:
            ratio = round(amount / total_monthly * 100, 1) if total_monthly else 0
            lines.append(f"  - {CATEGORY_LABELS.get(category, category)}: {_format_won(amount)} ({ratio}%)")
        top_category, top_amount = non_zero_categories[0]
        lines.append(
            f"- 소비 리포트 핵심: {CATEGORY_LABELS.get(top_category, top_category)} 비중이 가장 큼 "
            f"({_format_won(top_amount)})."
        )

    if spending_survey:
        top_merchants = (
            SpendingTransaction.objects
            .filter(survey=spending_survey)
            .values('merchant', 'category')
            .annotate(total=Sum('amount'), count=Count('id'))
            .order_by('-total')[:5]
        )
        if top_merchants:
            lines.append('- 상위 가맹점:')
            for merchant in top_merchants:
                lines.append(
                    f"  - {merchant['merchant']} ({CATEGORY_LABELS.get(merchant['category'], merchant['category'])}): "
                    f"총 {_format_won(merchant['total'])}, {merchant['count']}건"
                )

        monthly_trends = (
            SpendingTransaction.objects
            .filter(survey=spending_survey)
            .annotate(month=TruncMonth('transaction_date'))
            .values('month')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )
        if monthly_trends:
            trend_text = ', '.join(
                f"{row['month'].strftime('%Y-%m')} {_format_won(row['total'])}"
                for row in monthly_trends
            )
            lines.append(f"- 월별 총지출 추이: {trend_text}")

    max_annual_fee = preference.max_annual_fee if preference else 999999999
    lines.extend([
        '[관련 카드 후보]',
        _build_relevant_cards_context(monthly_categories, max_annual_fee),
        '[답변 지침]',
        '- 사용자가 소비 리포트, CSV, 설문, 카드 추천을 물으면 위 개인화 컨텍스트를 우선 근거로 답하세요.',
        '- 근거가 부족한 항목은 단정하지 말고 어떤 데이터가 더 필요한지 짧게 안내하세요.',
        '- 카드 추천은 사용자의 상위 소비 카테고리, 월평균 지출, 연회비 한도를 함께 언급하세요.',
    ])
    return '\n'.join(lines)


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
      "expected_monthly_benefit": "<예상 월 혜택 금액(숫자, 원 단위)>",
      "net_benefit": "<연회비 차감 후 연간 순혜택 금액(숫자, 원 단위)>",
      "benefit_details": "<주요 혜택 항목 요약 1~2문장>"
    }}
  ],
  "spending_insight": "<사용자 소비 패턴에 대한 전반적인 AI 분석 2~3문장>"
}}"""


def get_card_reason(card, survey) -> dict:
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
    benefits_text = " / ".join([
        f"{b.get_benefit_category_display()} {b.discount_rate}% {b.get_benefit_type_display()}"
        + (f" (월{b.monthly_limit:,}원 한도)" if b.monthly_limit else "")
        for b in card.benefits.all()
    ])
    prompt = f"""당신은 삼성카드 전문 AI 상담사입니다.
사용자의 소비 패턴과 아래 카드의 혜택을 분석하여 이 카드가 사용자에게 적합한 이유를 설명해주세요.

[사용자 월 소비 패턴]
{json.dumps(spending, ensure_ascii=False, indent=2)}
월 총 지출: {total:,}원

[카드 정보]
카드명: {card.card_name}
카드사: {card.card_company}
연회비: {card.annual_fee:,}원
혜택: {benefits_text or '기본 캐시백'}

[응답 형식 - 반드시 아래 JSON 형식으로만 응답하세요]
{{
  "reason": "<이 카드가 사용자에게 적합한 구체적인 이유 2~3문장>",
  "expected_monthly_benefit": "<예상 월 혜택 금액 또는 설명>",
  "tip": "<이 카드를 최대한 활용하는 팁 1문장>"
}}"""

    try:
        client = _build_client()
        response = client.chat.completions.create(
            model=settings.GMS_MODEL,
            messages=[
                {"role": "system", "content": "당신은 삼성카드 AI 추천 서비스입니다. 반드시 요청된 JSON 형식으로만 응답하세요."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw)
    except Exception as e:
        return {"error": str(e), "reason": "", "expected_monthly_benefit": "", "tip": ""}


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


def get_financial_chat_reply(messages: list[dict], user=None, page_context=None) -> dict:
    system_prompt = """당신은 CardFit의 금융 전문 AI 상담사입니다.
사용자가 카드 혜택, 소비 리포트, 전월 실적, 연회비, 카드 비교를 쉽게 이해하도록 돕습니다.

답변 원칙:
- 한국어 존댓말을 사용합니다.
- 첫 문장에 결론을 말합니다.
- 어려운 금융 용어는 쉽게 풀어 설명합니다.
- 한 문장은 짧게 씁니다.
- 카드 발급, 투자, 대출처럼 중요한 결정은 사용자가 약관과 본인 상황을 확인하도록 안내합니다.
- 특정 카드가 필요하면 CardFit의 카드 검색, AI 추천, 소비 리포트를 확인하도록 자연스럽게 안내합니다.
- 확정적인 수익, 승인 보장, 법률·세무 자문처럼 단정적인 표현은 피합니다.
- 답변은 짧은 카톡 대화처럼 친근하게 작성하되, 핵심 금액/비율/카드명은 **굵게** 표시하고 필요한 경우 `-` 목록을 사용합니다.
"""
    user_context = _build_user_chat_context(user)
    current_page_context = _build_page_chat_context(page_context)

    safe_messages = []
    for message in messages[-8:]:
        role = message.get('role')
        content = str(message.get('content', '')).strip()
        if role not in ('user', 'assistant') or not content:
            continue
        safe_messages.append({'role': role, 'content': content[:1000]})

    if not safe_messages:
        return {'reply': '궁금한 내용을 입력해주세요. 카드 혜택과 소비 분석을 쉽게 알려드릴게요.'}

    try:
        client = _build_client()
        response = client.chat.completions.create(
            model=settings.GMS_MODEL,
            messages=[
                {'role': 'system', 'content': f'{system_prompt}\n\n{user_context}\n\n{current_page_context}'},
                *safe_messages,
            ],
            temperature=0.45,
            max_tokens=500,
        )
        reply = response.choices[0].message.content.strip()
        return {'reply': reply}
    except Exception as e:
        return {'error': str(e), 'reply': ''}
