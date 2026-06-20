from rest_framework import serializers
from .models import UserSurvey, SpendingTransaction


class SpendingTransactionSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = SpendingTransaction
        fields = (
            'id', 'survey', 'category', 'category_display',
            'merchant', 'amount', 'transaction_date',
        )
        read_only_fields = ('id',)


class SpendingTransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpendingTransaction
        fields = ('category', 'merchant', 'amount', 'transaction_date')


class UserSurveySerializer(serializers.ModelSerializer):
    total_monthly = serializers.ReadOnlyField()
    input_type_display = serializers.CharField(source='get_input_type_display', read_only=True)
    age_group_display = serializers.CharField(source='get_age_group_display', read_only=True)
    income_level_display = serializers.CharField(source='get_income_level_display', read_only=True)

    class Meta:
        model = UserSurvey
        fields = (
            'id',
            'input_type', 'input_type_display',
            'food_monthly', 'transport_monthly', 'shopping_monthly',
            'entertainment_monthly', 'communication_monthly', 'other_monthly',
            'total_monthly',
            'age_group', 'age_group_display',
            'max_annual_fee', 'income_level', 'income_level_display',
            'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class UserSurveyDetailSerializer(UserSurveySerializer):
    transactions = SpendingTransactionSerializer(many=True, read_only=True)

    class Meta(UserSurveySerializer.Meta):
        fields = UserSurveySerializer.Meta.fields + ('transactions',)


class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    age_group = serializers.ChoiceField(choices=UserSurvey.AGE_GROUP_CHOICES, required=False, allow_blank=True)
    income_level = serializers.ChoiceField(choices=UserSurvey.INCOME_LEVEL_CHOICES, required=False, allow_blank=True)
    max_annual_fee = serializers.IntegerField(required=False, min_value=0, default=100000)

    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError('CSV 파일만 업로드 가능합니다.')
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError('파일 크기는 5MB 이하이어야 합니다.')
        return value
    
    def validate_age_group(self, value):
        if value == '' or value is None:
            return '30s'
        return value
    
    def validate_income_level(self, value):
        if value == '' or value is None:
            return 'mid'
        return value
