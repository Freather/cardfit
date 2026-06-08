from django.urls import path
from .views import CardRecommendView

urlpatterns = [
    path('recommend/', CardRecommendView.as_view(), name='card-recommend'),
]
