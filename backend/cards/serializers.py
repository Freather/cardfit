from rest_framework import serializers
from .models import Card, CardBenefit, CardWishList


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
    is_wished = serializers.SerializerMethodField()

    def get_is_wished(self, obj):
        wish_card_ids = self.context.get('wish_card_ids')
        if wish_card_ids is not None:
            return obj.id in wish_card_ids
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return False
        return CardWishList.objects.filter(user=user, card=obj).exists()

    class Meta:
        model = Card
        fields = (
            'id', 'card_company', 'card_name',
            'card_type', 'card_type_display',
            'annual_fee', 'min_prev_month_spending',
            'apply_url', 'image_url', 'benefit_count', 'benefits', 'is_wished', 'synced_at',
        )


class CardDetailSerializer(serializers.ModelSerializer):
    card_type_display = serializers.CharField(source='get_card_type_display', read_only=True)
    benefits = CardBenefitSerializer(many=True, read_only=True)
    is_wished = serializers.SerializerMethodField()

    def get_is_wished(self, obj):
        wish_card_ids = self.context.get('wish_card_ids')
        if wish_card_ids is not None:
            return obj.id in wish_card_ids
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return False
        return CardWishList.objects.filter(user=user, card=obj).exists()

    class Meta:
        model = Card
        fields = (
            'id', 'card_company', 'card_name',
            'card_type', 'card_type_display',
            'annual_fee', 'min_prev_month_spending',
            'apply_url', 'image_url', 'benefits', 'is_wished', 'synced_at',
        )


class CardWishListSerializer(serializers.ModelSerializer):
    card = CardListSerializer(read_only=True)
    card_id = serializers.PrimaryKeyRelatedField(
        source='card',
        queryset=Card.objects.all(),
        write_only=True,
    )

    class Meta:
        model = CardWishList
        fields = ('id', 'user', 'card', 'card_id', 'source', 'created_at')
        read_only_fields = ('id', 'user', 'card', 'created_at')
