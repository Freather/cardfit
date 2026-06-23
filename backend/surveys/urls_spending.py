from django.urls import path
from .views import SpendingSurveyListCreateView, SpendingSurveyDetailView, SpendingCSVUploadView, SpendingStatusView

urlpatterns = [
    path('', SpendingSurveyListCreateView.as_view(), name='spending-list-create'),
    path('status/', SpendingStatusView.as_view(), name='spending-status'),
    path('<int:pk>/', SpendingSurveyDetailView.as_view(), name='spending-detail'),
    path('upload-csv/', SpendingCSVUploadView.as_view(), name='spending-upload-csv'),
]
