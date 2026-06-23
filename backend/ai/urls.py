from django.urls import path
from .views import CardRecommendView, CardReasonView

urlpatterns = [
    path('recommend/', CardRecommendView.as_view(), name='card-recommend'),
    path('cards/<int:card_id>/reason/', CardReasonView.as_view(), name='card-reason'),
]
