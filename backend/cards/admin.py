from django.contrib import admin
from .models import Card, CardBenefit, CardWishList


class CardBenefitInline(admin.TabularInline):
    model = CardBenefit
    extra = 1
    fields = ('benefit_category', 'benefit_type', 'discount_rate', 'monthly_limit', 'condition_description')


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('card_company', 'card_name', 'card_type', 'annual_fee', 'min_prev_month_spending', 'synced_at')
    list_filter = ('card_company', 'card_type')
    search_fields = ('card_name', 'card_company')
    inlines = [CardBenefitInline]


@admin.register(CardBenefit)
class CardBenefitAdmin(admin.ModelAdmin):
    list_display = ('card', 'benefit_category', 'benefit_type', 'discount_rate', 'monthly_limit')
    list_filter = ('benefit_category', 'benefit_type')
    search_fields = ('card__card_name',)


@admin.register(CardWishList)
class CardWishListAdmin(admin.ModelAdmin):
    list_display = ('user', 'card', 'source', 'created_at')
    list_filter = ('source', 'created_at')
    search_fields = ('user__email', 'card__card_name', 'card__card_company')
