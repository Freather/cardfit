import secrets
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.core import signing
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError

from .models import User
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserProfileSerializer,
    SelectCardSerializer,
)


OAUTH_STATE_SALT = 'cardfit-oauth-state'


def build_frontend_oauth_redirect(tokens=None, error='', next_path=''):
    frontend_url = settings.FRONTEND_URL.rstrip('/')
    params = {}

    if tokens:
        params.update(tokens)
    if error:
        params['error'] = error
    if next_path:
        params['next'] = next_path

    query = urlencode(params)
    return f'{frontend_url}/login/oauth/callback{f"?{query}" if query else ""}'


def build_redirect_uri(request, provider):
    configured = {
        'kakao': settings.KAKAO_REDIRECT_URI,
        'naver': settings.NAVER_REDIRECT_URI,
    }.get(provider)

    if configured:
        return configured

    return request.build_absolute_uri(f'/api/accounts/oauth/{provider}/callback/')


def build_oauth_state(provider, next_path=''):
    return signing.dumps(
        {
            'provider': provider,
            'next': next_path or '/',
            'nonce': secrets.token_urlsafe(12),
        },
        salt=OAUTH_STATE_SALT,
    )


def read_oauth_state(raw_state, provider):
    try:
        state = signing.loads(raw_state, salt=OAUTH_STATE_SALT, max_age=600)
    except signing.BadSignature:
        return None

    if state.get('provider') != provider:
        return None

    return state


def issue_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


def unique_username(base):
    cleaned = ''.join(ch for ch in base if ch.isalnum() or ch in ('_', '-')).strip()[:120]
    prefix = cleaned or 'cardfit_user'
    username = prefix
    suffix = 1

    while User.objects.filter(username=username).exists():
        suffix += 1
        username = f'{prefix}_{suffix}'[:150]

    return username


def get_or_create_oauth_user(email, nickname, provider):
    normalized_email = User.objects.normalize_email(email)
    user = User.objects.filter(email=normalized_email).first()
    if user:
        return user

    username_base = nickname or normalized_email.split('@')[0] or provider
    return User.objects.create_user(
        email=normalized_email,
        username=unique_username(username_base),
        password=None,
    )


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'message': '회원가입이 완료되었습니다.',
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'message': '로그인 성공',
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                },
            }
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'detail': 'refresh 토큰이 필요합니다.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': '로그아웃 완료'})
        except TokenError:
            return Response(
                {'detail': '유효하지 않은 토큰입니다.'},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        request.user.is_active = False
        request.user.save()
        return Response({'message': '계정이 비활성화되었습니다.'}, status=status.HTTP_204_NO_CONTENT)


class SelectCardView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = SelectCardSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'message': '대표 카드가 설정되었습니다.',
                'selected_card_id': request.user.selected_card_id,
            }
        )


class KakaoOAuthStartView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if not settings.KAKAO_REST_API_KEY:
            return Response({'detail': '카카오 로그인 설정이 필요합니다.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        state = build_oauth_state('kakao', request.query_params.get('next', '/'))
        params = {
            'client_id': settings.KAKAO_REST_API_KEY,
            'redirect_uri': build_redirect_uri(request, 'kakao'),
            'response_type': 'code',
            'state': state,
        }
        return redirect(f'https://kauth.kakao.com/oauth/authorize?{urlencode(params)}')


class KakaoOAuthCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.query_params.get('code')
        state = read_oauth_state(request.query_params.get('state', ''), 'kakao')

        if not code or not state:
            return redirect(build_frontend_oauth_redirect(error='카카오 로그인 정보를 확인하지 못했어요.'))

        try:
            token_response = requests.post(
                'https://kauth.kakao.com/oauth/token',
                data={
                    'grant_type': 'authorization_code',
                    'client_id': settings.KAKAO_REST_API_KEY,
                    'redirect_uri': build_redirect_uri(request, 'kakao'),
                    'code': code,
                },
                timeout=8,
            )
            token_response.raise_for_status()
            access_token = token_response.json().get('access_token')

            user_response = requests.get(
                'https://kapi.kakao.com/v2/user/me',
                headers={'Authorization': f'Bearer {access_token}'},
                timeout=8,
            )
            user_response.raise_for_status()
            profile = user_response.json()
        except requests.RequestException:
            return redirect(build_frontend_oauth_redirect(error='카카오 로그인 처리 중 오류가 발생했어요.'))

        kakao_account = profile.get('kakao_account') or {}
        email = kakao_account.get('email')
        nickname = (kakao_account.get('profile') or {}).get('nickname')

        if not email:
            return redirect(build_frontend_oauth_redirect(error='카카오 계정 이메일 제공 동의가 필요해요.'))

        user = get_or_create_oauth_user(email, nickname, 'kakao')
        return redirect(build_frontend_oauth_redirect(issue_tokens_for_user(user), next_path=state.get('next', '/')))


class NaverOAuthStartView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if not settings.NAVER_CLIENT_ID or not settings.NAVER_CLIENT_SECRET:
            return Response({'detail': '네이버 로그인 설정이 필요합니다.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        state = build_oauth_state('naver', request.query_params.get('next', '/'))
        params = {
            'response_type': 'code',
            'client_id': settings.NAVER_CLIENT_ID,
            'redirect_uri': build_redirect_uri(request, 'naver'),
            'state': state,
        }
        return redirect(f'https://nid.naver.com/oauth2.0/authorize?{urlencode(params)}')


class NaverOAuthCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.query_params.get('code')
        raw_state = request.query_params.get('state', '')
        state = read_oauth_state(raw_state, 'naver')

        if not code or not state:
            return redirect(build_frontend_oauth_redirect(error='네이버 로그인 정보를 확인하지 못했어요.'))

        try:
            token_response = requests.get(
                'https://nid.naver.com/oauth2.0/token',
                params={
                    'grant_type': 'authorization_code',
                    'client_id': settings.NAVER_CLIENT_ID,
                    'client_secret': settings.NAVER_CLIENT_SECRET,
                    'code': code,
                    'state': raw_state,
                },
                timeout=8,
            )
            token_response.raise_for_status()
            access_token = token_response.json().get('access_token')

            user_response = requests.get(
                'https://openapi.naver.com/v1/nid/me',
                headers={'Authorization': f'Bearer {access_token}'},
                timeout=8,
            )
            user_response.raise_for_status()
            profile = user_response.json().get('response') or {}
        except requests.RequestException:
            return redirect(build_frontend_oauth_redirect(error='네이버 로그인 처리 중 오류가 발생했어요.'))

        email = profile.get('email')
        nickname = profile.get('nickname') or profile.get('name')

        if not email:
            return redirect(build_frontend_oauth_redirect(error='네이버 계정 이메일 제공 동의가 필요해요.'))

        user = get_or_create_oauth_user(email, nickname, 'naver')
        return redirect(build_frontend_oauth_redirect(issue_tokens_for_user(user), next_path=state.get('next', '/')))
