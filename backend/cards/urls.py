from django.urls import path
from .views import CardListView, CardDetailView, CardBenefitListView

urlpatterns = [
    path('', CardListView.as_view(), name='card-list'),
    path('<int:pk>/', CardDetailView.as_view(), name='card-detail'),
    path('<int:pk>/benefits/', CardBenefitListView.as_view(), name='card-benefits'),
]
