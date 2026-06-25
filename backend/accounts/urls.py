from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    KakaoOAuthCallbackView,
    KakaoOAuthStartView,
    LoginView,
    LogoutView,
    NaverOAuthCallbackView,
    NaverOAuthStartView,
    ProfileView,
    RegisterView,
    SelectCardView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('select-card/', SelectCardView.as_view(), name='select-card'),
    path('oauth/kakao/', KakaoOAuthStartView.as_view(), name='oauth-kakao'),
    path('oauth/kakao/callback/', KakaoOAuthCallbackView.as_view(), name='oauth-kakao-callback'),
    path('oauth/naver/', NaverOAuthStartView.as_view(), name='oauth-naver'),
    path('oauth/naver/callback/', NaverOAuthCallbackView.as_view(), name='oauth-naver-callback'),
]
