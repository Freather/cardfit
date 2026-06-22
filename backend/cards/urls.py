from django.urls import path
from .views import (
    CardListView,
    CardDetailView,
    CardBenefitListView,
    CardWishListView,
    CardWishDetailView,
)

urlpatterns = [
    path('', CardListView.as_view(), name='card-list'),
    path('wishlist/', CardWishListView.as_view(), name='card-wishlist'),
    path('wishlist/<int:card_id>/', CardWishDetailView.as_view(), name='card-wish-detail'),
    path('<int:pk>/', CardDetailView.as_view(), name='card-detail'),
    path('<int:pk>/benefits/', CardBenefitListView.as_view(), name='card-benefits'),
]
