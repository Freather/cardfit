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
