from django.conf import settings
from django.db import models


class UserSurvey(models.Model):
    INPUT_TYPE_CHOICES = [
        ('manual', '직접입력'),
        ('csv', 'CSV 업로드'),
        ('api', 'API 연동'),
    ]
    AGE_GROUP_CHOICES = [
        ('20s', '20대'),
        ('30s', '30대'),
        ('40s', '40대'),
        ('50s', '50대'),
        ('60s', '60대 이상'),
    ]
    INCOME_LEVEL_CHOICES = [
        ('low', '저소득'),
        ('mid', '중소득'),
        ('high', '고소득'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='surveys',
    )
    input_type = models.CharField(max_length=20, choices=INPUT_TYPE_CHOICES, default='manual')
    food_monthly = models.PositiveIntegerField(default=0, verbose_name='식비(원/월)')
    transport_monthly = models.PositiveIntegerField(default=0, verbose_name='교통비(원/월)')
    fuel_monthly = models.PositiveIntegerField(default=0, verbose_name='주유비(원/월)')
    shopping_monthly = models.PositiveIntegerField(default=0, verbose_name='쇼핑비(원/월)')
    entertainment_monthly = models.PositiveIntegerField(default=0, verbose_name='여가비(원/월)')
    communication_monthly = models.PositiveIntegerField(default=0, verbose_name='통신비(원/월)')
    health_monthly = models.PositiveIntegerField(default=0, verbose_name='의료/건강비(원/월)')
    other_monthly = models.PositiveIntegerField(default=0, verbose_name='기타(원/월)')
    age_group = models.CharField(max_length=10, choices=AGE_GROUP_CHOICES, verbose_name='연령대')
    max_annual_fee = models.PositiveIntegerField(default=0, verbose_name='최대 연회비(원)')
    income_level = models.CharField(max_length=10, choices=INCOME_LEVEL_CHOICES, verbose_name='소득 수준')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'surveys_usersurvey'
        verbose_name = '지출 설문'
        verbose_name_plural = '지출 설문 목록'
        ordering = ['-created_at']

    @property
    def total_monthly(self):
        return (
            self.food_monthly
            + self.transport_monthly
            + self.fuel_monthly
            + self.shopping_monthly
            + self.entertainment_monthly
            + self.communication_monthly
            + self.health_monthly
            + self.other_monthly
        )

    def __str__(self):
        return f'{self.user.email} - {self.created_at.strftime("%Y-%m-%d")}'


class SpendingTransaction(models.Model):
    CATEGORY_CHOICES = [
        ('food', '식비'),
        ('transport', '교통'),
        ('fuel', '주유'),
        ('shopping', '쇼핑'),
        ('entertainment', '여가'),
        ('communication', '통신'),
        ('health', '의료/건강'),
        ('other', '기타'),
    ]

    survey = models.ForeignKey(
        UserSurvey,
        on_delete=models.CASCADE,
        related_name='transactions',
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='카테고리')
    merchant = models.CharField(max_length=200, verbose_name='가맹점')
    amount = models.IntegerField(verbose_name='금액(원)')
    transaction_date = models.DateField(verbose_name='거래일')

    class Meta:
        db_table = 'surveys_spendingtransaction'
        verbose_name = '지출 거래내역'
        verbose_name_plural = '지출 거래내역 목록'
        ordering = ['-transaction_date']

    def __str__(self):
        return f'{self.merchant} {self.amount:,}원 ({self.transaction_date})'
