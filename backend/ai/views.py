from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings

from surveys.models import UserSurvey
from .recommender import get_gms_recommendations


class CardRecommendView(APIView):
    """소비 패턴 기반 삼성카드 AI 추천 (SSAFY GMS API)
    - 결과는 DB에 저장하지 않고 실시간으로 응답합니다.
    """
    permission_classes = [IsAuthenticated]

    def _get_survey(self, request, survey_id=None):
        if survey_id:
            return UserSurvey.objects.filter(pk=survey_id, user=request.user).first()
        return UserSurvey.objects.filter(user=request.user).first()

    def get(self, request):
        """저장된 설문 기반 추천"""
        survey_id = request.query_params.get('survey_id')
        survey = self._get_survey(request, survey_id)

        if not survey:
            return Response(
                {'detail': '지출 데이터가 없습니다. 먼저 설문을 완료하거나 CSV를 업로드해 주세요.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not settings.GMS_API_KEY:
            return Response(
                {'detail': 'GMS_API_KEY가 설정되지 않았습니다. .env 파일을 확인해 주세요.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        result = get_gms_recommendations(survey)

        if 'error' in result and result['error']:
            return Response(
                {'detail': f'AI 추천 오류: {result["error"]}'},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response({
            'survey_id': survey.id,
            'based_on': {
                'food_monthly': survey.food_monthly,
                'transport_monthly': survey.transport_monthly,
                'shopping_monthly': survey.shopping_monthly,
                'entertainment_monthly': survey.entertainment_monthly,
                'communication_monthly': survey.communication_monthly,
                'other_monthly': survey.other_monthly,
                'total_monthly': survey.total_monthly,
                'max_annual_fee': survey.max_annual_fee,
            },
            **result,
        })

    def post(self, request):
        """즉석 지출 입력 기반 추천 (설문 저장 없이)"""
        if not settings.GMS_API_KEY:
            return Response(
                {'detail': 'GMS_API_KEY가 설정되지 않았습니다.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        class TempSurvey:
            food_monthly = int(request.data.get('food_monthly', 0))
            transport_monthly = int(request.data.get('transport_monthly', 0))
            shopping_monthly = int(request.data.get('shopping_monthly', 0))
            entertainment_monthly = int(request.data.get('entertainment_monthly', 0))
            communication_monthly = int(request.data.get('communication_monthly', 0))
            other_monthly = int(request.data.get('other_monthly', 0))
            max_annual_fee = int(request.data.get('max_annual_fee', 200000))
            total_monthly = (
                food_monthly + transport_monthly + shopping_monthly +
                entertainment_monthly + communication_monthly + other_monthly
            )

        result = get_gms_recommendations(TempSurvey())

        if 'error' in result and result['error']:
            return Response(
                {'detail': f'AI 추천 오류: {result["error"]}'},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(result)
