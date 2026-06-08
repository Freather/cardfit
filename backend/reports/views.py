from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth

from surveys.models import UserSurvey, SpendingTransaction
from cards.models import Card, CardBenefit


class SpendingSummaryView(APIView):
    """최신 설문 기준 카테고리별 월 지출 요약"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        survey = UserSurvey.objects.filter(user=request.user).first()
        if not survey:
            return Response({'detail': '지출 설문 데이터가 없습니다. 먼저 설문을 완료해 주세요.'}, status=404)

        data = {
            'survey_id': survey.id,
            'input_type': survey.input_type,
            'categories': {
                'food': survey.food_monthly,
                'transport': survey.transport_monthly,
                'shopping': survey.shopping_monthly,
                'entertainment': survey.entertainment_monthly,
                'communication': survey.communication_monthly,
                'other': survey.other_monthly,
            },
            'total_monthly': survey.total_monthly,
            'age_group': survey.age_group,
            'income_level': survey.income_level,
            'max_annual_fee': survey.max_annual_fee,
            'created_at': survey.created_at,
        }
        return Response(data)


class CategoryBreakdownView(APIView):
    """거래내역 기반 카테고리별 상세 분석"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        survey_id = request.query_params.get('survey_id')
        qs = SpendingTransaction.objects.filter(survey__user=request.user)
        if survey_id:
            qs = qs.filter(survey_id=survey_id)

        by_category = (
            qs.values('category')
            .annotate(total=Sum('amount'), count=Count('id'))
            .order_by('-total')
        )

        total_amount = sum(item['total'] for item in by_category) or 1
        results = [
            {
                'category': item['category'],
                'total': item['total'],
                'count': item['count'],
                'ratio': round(item['total'] / total_amount * 100, 1),
            }
            for item in by_category
        ]

        return Response({'total': total_amount, 'breakdown': results})


class MonthlyTrendView(APIView):
    """월별 지출 트렌드"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = (
            SpendingTransaction.objects
            .filter(survey__user=request.user)
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
            .filter(survey__user=request.user)
            .values('merchant', 'category')
            .annotate(total=Sum('amount'), count=Count('id'))
            .order_by('-total')[:limit]
        )
        return Response({'results': list(qs)})
