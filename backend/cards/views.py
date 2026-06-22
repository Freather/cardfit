from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from .models import Card, CardBenefit, CardWishList
from .serializers import (
    CardListSerializer,
    CardDetailSerializer,
    CardBenefitSerializer,
    CardWishListSerializer,
)


class CardListView(APIView):
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

        wish_card_ids = set()
        if request.user.is_authenticated:
            wish_card_ids = set(
                CardWishList.objects
                .filter(user=request.user, card__in=queryset)
                .values_list('card_id', flat=True)
            )
        serializer = CardListSerializer(
            queryset,
            many=True,
            context={'request': request, 'wish_card_ids': wish_card_ids},
        )
        return Response({'count': queryset.count(), 'results': serializer.data})


class CardDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        card = get_object_or_404(Card, pk=pk)
        serializer = CardDetailSerializer(card, context={'request': request})
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


class CardWishListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishes = (
            CardWishList.objects
            .filter(user=request.user)
            .select_related('card')
            .prefetch_related('card__benefits')
        )
        serializer = CardWishListSerializer(
            wishes,
            many=True,
            context={'request': request},
        )
        return Response({'count': wishes.count(), 'results': serializer.data})

    def post(self, request):
        serializer = CardWishListSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        try:
            wish = serializer.save(user=request.user)
        except IntegrityError:
            wish = CardWishList.objects.get(
                user=request.user,
                card=serializer.validated_data['card'],
            )
        return Response(
            CardWishListSerializer(wish, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )


class CardWishDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, card_id):
        wish = get_object_or_404(CardWishList, user=request.user, card_id=card_id)
        wish.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
