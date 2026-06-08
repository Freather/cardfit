from django.urls import path
from .views import SpendingSurveyListCreateView, SpendingSurveyDetailView, SpendingCSVUploadView

urlpatterns = [
    path('', SpendingSurveyListCreateView.as_view(), name='spending-list-create'),
    path('<int:pk>/', SpendingSurveyDetailView.as_view(), name='spending-detail'),
    path('upload-csv/', SpendingCSVUploadView.as_view(), name='spending-upload-csv'),
]
