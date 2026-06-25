from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction as db_transaction

from .models import UserSurvey, SpendingTransaction
from .serializers import (
    UserSurveySerializer,
    UserSurveyDetailSerializer,
    SpendingTransactionSerializer,
    SpendingTransactionCreateSerializer,
    CSVUploadSerializer,
)
from .utils import build_monthly_average_by_category, parse_samsung_csv


# ─── /api/spending/ ────────────────────────────────────────────────────────────

class SpendingSurveyListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        surveys = UserSurvey.objects.filter(user=request.user)
        serializer = UserSurveySerializer(surveys, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSurveySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SpendingSurveyDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_survey(self, request, pk):
        return get_object_or_404(UserSurvey, pk=pk, user=request.user)

    def get(self, request, pk):
        survey = self._get_survey(request, pk)
        serializer = UserSurveyDetailSerializer(survey)
        return Response(serializer.data)

    def put(self, request, pk):
        survey = self._get_survey(request, pk)
        serializer = UserSurveySerializer(survey, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        survey = self._get_survey(request, pk)
        survey.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SpendingCSVUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # FormData와 FILES를 분리해서 처리
        data_dict = request.data.copy()
        data_dict.update(request.FILES)
        
        file_serializer = CSVUploadSerializer(data=data_dict)
        if not file_serializer.is_valid():
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_file = file_serializer.validated_data['file']

        try:
            parsed = parse_samsung_csv(uploaded_file)
        except Exception as e:
            return Response({'detail': f'CSV 파싱 오류: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        if not parsed:
            return Response({'detail': '유효한 거래 내역이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        category_totals = build_monthly_average_by_category(parsed)

        # 설문 정보 추출 (요청에서 제공되지 않으면 기본값 사용)
        age_group = file_serializer.validated_data.get('age_group', '30s')
        income_level = file_serializer.validated_data.get('income_level', 'mid')
        max_annual_fee = file_serializer.validated_data.get('max_annual_fee', 100000)

        with db_transaction.atomic():
            survey = UserSurvey.objects.create(
                user=request.user,
                input_type='csv',
                food_monthly=category_totals.get('food', 0),
                transport_monthly=category_totals.get('transport', 0),
                fuel_monthly=category_totals.get('fuel', 0),
                shopping_monthly=category_totals.get('shopping', 0),
                entertainment_monthly=category_totals.get('entertainment', 0),
                communication_monthly=category_totals.get('communication', 0),
                health_monthly=category_totals.get('health', 0),
                other_monthly=category_totals.get('other', 0),
                age_group=age_group,
                max_annual_fee=max_annual_fee,
                income_level=income_level,
            )
            SpendingTransaction.objects.bulk_create([
                SpendingTransaction(survey=survey, **tx) for tx in parsed
            ])

        return Response(
            {
                'message': f'{len(parsed)}건의 거래내역이 분석되었습니다.',
                'survey': UserSurveyDetailSerializer(survey).data,
            },
            status=status.HTTP_201_CREATED,
        )


class SpendingStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        surveys = UserSurvey.objects.filter(user=request.user)
        latest_manual = surveys.filter(input_type='manual').first()
        latest_csv = surveys.filter(input_type='csv').first()
        return Response({
            'has_survey': latest_manual is not None,
            'has_csv': latest_csv is not None,
            'latest_survey_id': latest_manual.id if latest_manual else None,
            'latest_csv_id': latest_csv.id if latest_csv else None,
        })


# ─── /api/transactions/ ────────────────────────────────────────────────────────

class TransactionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        survey_id = request.query_params.get('survey_id')
        category = request.query_params.get('category')

        qs = SpendingTransaction.objects.filter(survey__user=request.user)
        if survey_id:
            qs = qs.filter(survey_id=survey_id)
        if category:
            qs = qs.filter(category=category)

        serializer = SpendingTransactionSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        survey_id = request.data.get('survey_id')
        survey = get_object_or_404(UserSurvey, pk=survey_id, user=request.user)

        serializer = SpendingTransactionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tx = serializer.save(survey=survey)
        return Response(SpendingTransactionSerializer(tx).data, status=status.HTTP_201_CREATED)


class TransactionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_transaction(self, request, pk):
        return get_object_or_404(SpendingTransaction, pk=pk, survey__user=request.user)

    def get(self, request, pk):
        tx = self._get_transaction(request, pk)
        return Response(SpendingTransactionSerializer(tx).data)

    def put(self, request, pk):
        tx = self._get_transaction(request, pk)
        serializer = SpendingTransactionCreateSerializer(tx, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(SpendingTransactionSerializer(tx).data)

    def delete(self, request, pk):
        tx = self._get_transaction(request, pk)
        tx.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
