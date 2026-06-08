from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/cards/', include('cards.urls')),
    path('api/spending/', include('surveys.urls_spending')),
    path('api/transactions/', include('surveys.urls_transactions')),
    path('api/reports/', include('reports.urls')),
    path('api/ai/', include('ai.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
