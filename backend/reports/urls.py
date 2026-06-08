from django.urls import path
from .views import SpendingSummaryView, CategoryBreakdownView, MonthlyTrendView, TopMerchantsView

urlpatterns = [
    path('spending-summary/', SpendingSummaryView.as_view(), name='spending-summary'),
    path('category-breakdown/', CategoryBreakdownView.as_view(), name='category-breakdown'),
    path('monthly-trend/', MonthlyTrendView.as_view(), name='monthly-trend'),
    path('top-merchants/', TopMerchantsView.as_view(), name='top-merchants'),
]
