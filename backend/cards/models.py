from django.db import models


class Card(models.Model):
    CARD_TYPE_CHOICES = [
        ('credit', '신용카드'),
        ('debit', '체크카드'),
        ('prepaid', '선불카드'),
    ]

    card_company = models.CharField(max_length=100, verbose_name='카드사')
    card_name = models.CharField(max_length=200, verbose_name='카드명')
    card_type = models.CharField(max_length=20, choices=CARD_TYPE_CHOICES, verbose_name='카드 종류')
    annual_fee = models.PositiveIntegerField(default=0, verbose_name='연회비(원)')
    min_prev_month_spending = models.PositiveIntegerField(default=0, verbose_name='전월 실적 기준(원)')
    apply_url = models.URLField(blank=True, verbose_name='신청 URL')
    synced_at = models.DateTimeField(auto_now=True, verbose_name='동기화 시각')

    class Meta:
        db_table = 'cards_card'
        verbose_name = '카드'
        verbose_name_plural = '카드 목록'
        ordering = ['card_company', 'card_name']

    def __str__(self):
        return f'[{self.card_company}] {self.card_name}'


class CardBenefit(models.Model):
    BENEFIT_CATEGORY_CHOICES = [
        ('food', '식비'),
        ('transport', '교통'),
        ('shopping', '쇼핑'),
        ('entertainment', '여가/문화'),
        ('communication', '통신'),
        ('travel', '여행'),
        ('health', '의료/건강'),
        ('other', '기타'),
    ]
    BENEFIT_TYPE_CHOICES = [
        ('discount', '할인'),
        ('cashback', '캐시백'),
        ('point', '포인트 적립'),
        ('mileage', '마일리지'),
    ]

    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='benefits')
    benefit_category = models.CharField(max_length=50, choices=BENEFIT_CATEGORY_CHOICES, verbose_name='혜택 카테고리')
    benefit_type = models.CharField(max_length=20, choices=BENEFIT_TYPE_CHOICES, verbose_name='혜택 유형')
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='할인/적립률(%)')
    monthly_limit = models.PositiveIntegerField(null=True, blank=True, verbose_name='월 한도(원)')
    condition_description = models.TextField(blank=True, verbose_name='조건 설명')

    class Meta:
        db_table = 'cards_cardbenefit'
        verbose_name = '카드 혜택'
        verbose_name_plural = '카드 혜택 목록'

    def __str__(self):
        return f'{self.card.card_name} - {self.get_benefit_category_display()} {self.discount_rate}%'
