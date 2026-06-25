from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cards.models import Card
from surveys.models import UserSurvey
from surveys.utils import build_monthly_average_by_category
from .recommender import get_card_reason, get_financial_chat_reply, get_gms_recommendations


SPENDING_FIELDS = [
    'food_monthly',
    'transport_monthly',
    'fuel_monthly',
    'shopping_monthly',
    'entertainment_monthly',
    'communication_monthly',
    'health_monthly',
    'other_monthly',
]

FIELD_BY_CATEGORY = {
    'food': 'food_monthly',
    'transport': 'transport_monthly',
    'fuel': 'fuel_monthly',
    'shopping': 'shopping_monthly',
    'entertainment': 'entertainment_monthly',
    'communication': 'communication_monthly',
    'health': 'health_monthly',
    'other': 'other_monthly',
}


def get_analysis_sources(request, survey_id=None):
    preference_survey = UserSurvey.objects.filter(
        user=request.user,
        input_type='manual',
    ).first()
    spending_qs = UserSurvey.objects.filter(
        user=request.user,
        input_type='csv',
    )
    if survey_id:
        spending_qs = spending_qs.filter(pk=survey_id)
    return preference_survey, spending_qs.first()


def build_monthly_survey_proxy(spending_survey, preference_survey=None):
    preference_survey = preference_survey or spending_survey
    transactions = list(spending_survey.transactions.all())
    monthly_values = {field: getattr(spending_survey, field) for field in SPENDING_FIELDS}

    if spending_survey.input_type == 'csv' and transactions:
        averages = build_monthly_average_by_category(transactions)
        for category, field in FIELD_BY_CATEGORY.items():
            monthly_values[field] = averages.get(category, 0)

    class MonthlySurvey:
        pass

    proxy = MonthlySurvey()
    for field, value in monthly_values.items():
        setattr(proxy, field, value)
    proxy.max_annual_fee = preference_survey.max_annual_fee
    proxy.total_monthly = sum(monthly_values.values())
    return proxy


class CardRecommendView(APIView):
    """Recommend cards from objective CSV spending and manual preferences."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        survey_id = request.query_params.get('survey_id')
        preference_survey, spending_survey = get_analysis_sources(request, survey_id)

        if not preference_survey or not spending_survey:
            return Response(
                {'detail': 'AI 추천을 보려면 소비 설문과 CSV 업로드를 모두 완료해 주세요.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not settings.GMS_API_KEY:
            return Response(
                {'detail': 'GMS_API_KEY가 설정되지 않았습니다. .env 파일을 확인해 주세요.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        monthly_survey = build_monthly_survey_proxy(spending_survey, preference_survey)
        result = get_gms_recommendations(monthly_survey)

        if 'error' in result and result['error']:
            return Response(
                {'detail': f'AI 추천 오류: {result["error"]}'},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        recommendations = result.get('recommendations', [])
        top = request.query_params.get('top')
        if top:
            try:
                recommendations = recommendations[:int(top)]
            except ValueError:
                pass

        card_ids = [rec.get('card_id') for rec in recommendations if rec.get('card_id')]
        card_map = {card.id: card for card in Card.objects.filter(id__in=card_ids)}
        enriched = []
        for rec in recommendations:
            card = card_map.get(rec.get('card_id'))
            enriched.append({
                'card_id': rec.get('card_id'),
                'card_name': rec.get('card_name'),
                'card_company': card.card_company if card else '',
                'annual_fee': card.annual_fee if card else 0,
                'apply_url': card.apply_url if card else '',
                'rank': rec.get('rank'),
                'reason': rec.get('reason', ''),
                'expected_monthly_benefit': rec.get('expected_monthly_benefit', ''),
                'net_benefit': rec.get('net_benefit', ''),
                'benefit_details': rec.get('benefit_details', ''),
            })

        return Response({
            'survey_id': spending_survey.id,
            'preference_survey_id': preference_survey.id,
            'based_on': {
                'food_monthly': monthly_survey.food_monthly,
                'transport_monthly': monthly_survey.transport_monthly,
                'fuel_monthly': monthly_survey.fuel_monthly,
                'shopping_monthly': monthly_survey.shopping_monthly,
                'entertainment_monthly': monthly_survey.entertainment_monthly,
                'communication_monthly': monthly_survey.communication_monthly,
                'health_monthly': monthly_survey.health_monthly,
                'other_monthly': monthly_survey.other_monthly,
                'total_monthly': monthly_survey.total_monthly,
                'max_annual_fee': monthly_survey.max_annual_fee,
            },
            'recommendations': enriched,
            'spending_insight': result.get('spending_insight', ''),
        })

    def post(self, request):
        if not settings.GMS_API_KEY:
            return Response(
                {'detail': 'GMS_API_KEY가 설정되지 않았습니다.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        class TempSurvey:
            food_monthly = int(request.data.get('food_monthly', 0))
            transport_monthly = int(request.data.get('transport_monthly', 0))
            fuel_monthly = int(request.data.get('fuel_monthly', 0))
            shopping_monthly = int(request.data.get('shopping_monthly', 0))
            entertainment_monthly = int(request.data.get('entertainment_monthly', 0))
            communication_monthly = int(request.data.get('communication_monthly', 0))
            health_monthly = int(request.data.get('health_monthly', 0))
            other_monthly = int(request.data.get('other_monthly', 0))
            max_annual_fee = int(request.data.get('max_annual_fee', 200000))
            total_monthly = (
                food_monthly + transport_monthly + fuel_monthly + shopping_monthly +
                entertainment_monthly + communication_monthly + health_monthly + other_monthly
            )

        result = get_gms_recommendations(TempSurvey())

        if 'error' in result and result['error']:
            return Response(
                {'detail': f'AI 추천 오류: {result["error"]}'},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(result)


class CardReasonView(APIView):
    """Return an AI reason for a specific card."""

    permission_classes = [IsAuthenticated]

    def get(self, request, card_id):
        try:
            card = Card.objects.prefetch_related('benefits').get(pk=card_id)
        except Card.DoesNotExist:
            return Response({'detail': '카드를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        if not settings.GMS_API_KEY:
            return Response(
                {'detail': 'GMS_API_KEY가 설정되지 않았습니다.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        survey_id = request.query_params.get('survey_id')
        preference_survey, spending_survey = get_analysis_sources(request, survey_id)

        if not preference_survey or not spending_survey:
            return Response(
                {'detail': 'AI 추천 사유를 보려면 소비 설문과 CSV 업로드를 모두 완료해 주세요.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        result = get_card_reason(card, build_monthly_survey_proxy(spending_survey, preference_survey))

        if 'error' in result and result['error']:
            return Response(
                {'detail': f'AI 오류: {result["error"]}'},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response({
            'card_id': card.id,
            'card_name': card.card_name,
            'card_company': card.card_company,
            **result,
        })


class FinancialChatView(APIView):
    """General finance/card chat powered by GMS API."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not settings.GMS_API_KEY:
            return Response(
                {'detail': 'AI 채팅 설정이 아직 준비되지 않았어요.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        messages = request.data.get('messages', [])
        if not isinstance(messages, list):
            return Response(
                {'detail': '메시지 형식을 확인해주세요.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        page_context = request.data.get('page_context', {})
        if not isinstance(page_context, dict):
            page_context = {}

        result = get_financial_chat_reply(messages, user=request.user, page_context=page_context)
        if result.get('error'):
            return Response(
                {'detail': 'AI 답변을 만들지 못했어요. 다시 시도해주세요.'},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(result)
