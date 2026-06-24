from django.urls import path
from .views import CardRecommendView, CardReasonView, FinancialChatView

urlpatterns = [
    path('recommend/', CardRecommendView.as_view(), name='card-recommend'),
    path('cards/<int:card_id>/reason/', CardReasonView.as_view(), name='card-reason'),
    path('chat/', FinancialChatView.as_view(), name='financial-chat'),
]
