from rest_framework import serializers
from .models import Card, CardBenefit


class CardBenefitSerializer(serializers.ModelSerializer):
    benefit_category_display = serializers.CharField(source='get_benefit_category_display', read_only=True)
    benefit_type_display = serializers.CharField(source='get_benefit_type_display', read_only=True)

    class Meta:
        model = CardBenefit
        fields = (
            'id', 'benefit_category', 'benefit_category_display',
            'benefit_type', 'benefit_type_display',
            'discount_rate', 'monthly_limit', 'condition_description',
        )


class CardListSerializer(serializers.ModelSerializer):
    card_type_display = serializers.CharField(source='get_card_type_display', read_only=True)
    benefit_count = serializers.IntegerField(source='benefits.count', read_only=True)
    benefits = CardBenefitSerializer(many=True, read_only=True)

    class Meta:
        model = Card
        fields = (
            'id', 'card_company', 'card_name',
            'card_type', 'card_type_display',
            'annual_fee', 'min_prev_month_spending',
            'apply_url', 'image_url', 'benefit_count', 'benefits', 'synced_at',
        )


class CardDetailSerializer(serializers.ModelSerializer):
    card_type_display = serializers.CharField(source='get_card_type_display', read_only=True)
    benefits = CardBenefitSerializer(many=True, read_only=True)

    class Meta:
        model = Card
        fields = (
            'id', 'card_company', 'card_name',
            'card_type', 'card_type_display',
            'annual_fee', 'min_prev_month_spending',
            'apply_url', 'image_url', 'benefits', 'synced_at',
        )
