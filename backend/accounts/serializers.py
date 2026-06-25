from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password_confirm')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password': '비밀번호가 일치하지 않습니다.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data['email'].strip().lower()
        user = authenticate(email=email, password=data['password'])
        if not user:
            raise serializers.ValidationError('이메일 또는 비밀번호가 올바르지 않습니다.')
        if not user.is_active:
            raise serializers.ValidationError('비활성화된 계정입니다.')
        data['user'] = user
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    selected_card_id = serializers.PrimaryKeyRelatedField(
        source='selected_card',
        read_only=True,
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'selected_card_id', 'created_at', 'updated_at')
        read_only_fields = ('id', 'email', 'created_at', 'updated_at')


class SelectCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('selected_card',)

    def validate_selected_card(self, value):
        from cards.models import Card
        if value and not Card.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError('존재하지 않는 카드입니다.')
        return value
