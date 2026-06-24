from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Min, Max
from django.db.models.functions import TruncMonth

from surveys.models import UserSurvey, SpendingTransaction
from cards.models import Card, CardBenefit
from surveys.utils import build_monthly_average_by_category, count_transaction_months


SPENDING_CATEGORIES = [
    'food',
    'transport',
    'fuel',
    'shopping',
    'entertainment',
    'communication',
    'health',
    'other',
]


def get_monthly_categories_for_survey(survey):
    transactions = list(survey.transactions.all())
    if survey.input_type == 'csv' and transactions:
        averages = build_monthly_average_by_category(transactions)
        return {category: averages.get(category, 0) for category in SPENDING_CATEGORIES}

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


def get_transaction_period(queryset):
    period = queryset.aggregate(
        start_date=Min('transaction_date'),
        end_date=Max('transaction_date'),
    )
    return period['start_date'], period['end_date']


def get_latest_analysis_sources(user):
    preference_survey = UserSurvey.objects.filter(user=user, input_type='manual').first()
    spending_survey = UserSurvey.objects.filter(user=user, input_type='csv').first()
    return preference_survey, spending_survey


class SpendingSummaryView(APIView):
    """최신 설문 기준 카테고리별 월 지출 요약"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        preference_survey, survey = get_latest_analysis_sources(request.user)
        if not preference_survey:
            return Response({'detail': '소비 리포트를 보려면 소비 설문과 CSV 업로드를 모두 완료해 주세요.'}, status=404)
        if not survey:
            return Response({'detail': '지출 설문 데이터가 없습니다. 먼저 설문을 완료해 주세요.'}, status=404)

        categories = get_monthly_categories_for_survey(survey)
        start_date, end_date = get_transaction_period(survey.transactions.all())
        data = {
            'survey_id': survey.id,
            'input_type': survey.input_type,
            'categories': categories,
            'food_monthly': categories['food'],
            'transport_monthly': categories['transport'],
            'fuel_monthly': categories['fuel'],
            'shopping_monthly': categories['shopping'],
            'entertainment_monthly': categories['entertainment'],
            'communication_monthly': categories['communication'],
            'health_monthly': categories['health'],
            'other_monthly': categories['other'],
            'total_monthly': sum(categories.values()),
            'preference_survey_id': preference_survey.id,
            'age_group': preference_survey.age_group,
            'income_level': preference_survey.income_level,
            'max_annual_fee': preference_survey.max_annual_fee,
            'transaction_start_date': start_date,
            'transaction_end_date': end_date,
            'created_at': survey.created_at,
        }
        return Response(data)


class CategoryBreakdownView(APIView):
    """거래내역 기반 카테고리별 상세 분석"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        survey_id = request.query_params.get('survey_id')
        qs = SpendingTransaction.objects.filter(
            survey__user=request.user,
            survey__input_type='csv',
        )
        if survey_id:
            qs = qs.filter(survey_id=survey_id)
        else:
            latest_csv = UserSurvey.objects.filter(user=request.user, input_type='csv').first()
            if latest_csv:
                qs = qs.filter(survey=latest_csv)

        start_date, end_date = get_transaction_period(qs)
        transaction_months = count_transaction_months(qs.only('transaction_date'))
        by_category = (
            qs.values('category')
            .annotate(total=Sum('amount'), count=Count('id'))
            .order_by('-total')
        )

        total_amount = sum(item['total'] for item in by_category) or 1
        monthly_total = round(total_amount / transaction_months) or 1
        results = [
            {
                'category': item['category'],
                'total': round(item['total'] / transaction_months),
                'raw_total': item['total'],
                'count': item['count'],
                'ratio': round(item['total'] / total_amount * 100, 1),
            }
            for item in by_category
        ]

        return Response({
            'total': monthly_total,
            'raw_total': total_amount,
            'period_months': transaction_months,
            'transaction_start_date': start_date,
            'transaction_end_date': end_date,
            'breakdown': results,
        })


class MonthlyTrendView(APIView):
    """월별 지출 트렌드"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = (
            SpendingTransaction.objects
            .filter(survey__user=request.user, survey__input_type='csv')
            .annotate(month=TruncMonth('transaction_date'))
            .values('month', 'category')
            .annotate(total=Sum('amount'))
            .order_by('month', 'category')
        )

        trend = {}
        for row in qs:
            month_str = row['month'].strftime('%Y-%m')
            trend.setdefault(month_str, {})[row['category']] = row['total']

        return Response({'trend': trend})


class TopMerchantsView(APIView):
    """지출 상위 가맹점"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        limit = int(request.query_params.get('limit', 10))
        qs = (
            SpendingTransaction.objects
            .filter(survey__user=request.user, survey__input_type='csv')
            .values('merchant', 'category')
            .annotate(total=Sum('amount'), count=Count('id'))
            .order_by('-total')[:limit]
        )
        return Response({'results': list(qs)})
