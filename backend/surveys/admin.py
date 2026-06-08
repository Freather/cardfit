from django.contrib import admin
from .models import UserSurvey, SpendingTransaction


class SpendingTransactionInline(admin.TabularInline):
    model = SpendingTransaction
    extra = 0
    fields = ('transaction_date', 'category', 'merchant', 'amount')
    readonly_fields = ('transaction_date', 'category', 'merchant', 'amount')


@admin.register(UserSurvey)
class UserSurveyAdmin(admin.ModelAdmin):
    list_display = ('user', 'input_type', 'total_monthly', 'age_group', 'income_level', 'created_at')
    list_filter = ('input_type', 'age_group', 'income_level')
    search_fields = ('user__email',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [SpendingTransactionInline]


@admin.register(SpendingTransaction)
class SpendingTransactionAdmin(admin.ModelAdmin):
    list_display = ('survey', 'transaction_date', 'category', 'merchant', 'amount')
    list_filter = ('category', 'transaction_date')
    search_fields = ('merchant',)
