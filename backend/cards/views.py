from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from .models import Card, CardBenefit
from .serializers import CardListSerializer, CardDetailSerializer, CardBenefitSerializer


class CardListView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Card.objects.prefetch_related('benefits').all()

        card_type = request.query_params.get('card_type')
        company = request.query_params.get('company')
        max_annual_fee = request.query_params.get('max_annual_fee')

        if card_type:
            queryset = queryset.filter(card_type=card_type)
        if company:
            queryset = queryset.filter(card_company__icontains=company)
        if max_annual_fee:
            queryset = queryset.filter(annual_fee__lte=max_annual_fee)

        serializer = CardListSerializer(queryset, many=True)
        return Response({'count': queryset.count(), 'results': serializer.data})


class CardDetailView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, pk):
        card = get_object_or_404(Card, pk=pk)
        serializer = CardDetailSerializer(card)
        return Response(serializer.data)


class CardBenefitListView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, pk):
        card = get_object_or_404(Card, pk=pk)
        benefits = card.benefits.all()
        category = request.query_params.get('category')
        if category:
            benefits = benefits.filter(benefit_category=category)
        serializer = CardBenefitSerializer(benefits, many=True)
        return Response(serializer.data)
