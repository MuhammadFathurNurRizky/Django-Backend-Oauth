from rest_framework import serializers
from .models import NewUser
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class CustomUserSerializer(serializers.ModelSerializer):
    email     = serializers.EmailField(required=True)
    user_name = serializers.CharField(required=True)
    password  = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model        = NewUser
        fields       = ("email", "user_name", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model  = NewUser
        fields = ["token"]

class LoginSerializer(serializers.ModelSerializer):
    email     = serializers.EmailField(max_length=255, min_length=3)
    password  = serializers.CharField(max_length=68, min_length=8, write_only=True)
    user_name = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens    = serializers.CharField(max_length=68, min_length=6, read_only=True)

    class Meta:
        model  = NewUser
        fields = ["email", "password", "user_name", "tokens"]

    def validate(self, attrs):
        email    = attrs.get("email", "")
        password = attrs.get("password", "")
        filtered_user_by_email = NewUser.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != "email":
            raise AuthenticationFailed(detail="Please continue your login using " + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed("Theres no user with that account, try again")

        if not user.is_active:
            raise AuthenticationFailed("Account disabled, contact admin")
        
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")

        return {
            "email": user.email,
            "user_name": user.user_name,
            "tokens": user.tokens()
        }

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ["email"]

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=68, write_only=True)
    token    = serializers.CharField(min_length=1, write_only=True)
    uidb64   = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["password", "token", "uidb64"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token    = attrs.get("token")
            uidb64   = attrs.get("uidb64")

            id   = urlsafe_base64_decode(uidb64).decode()
            user = NewUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("Token is already hangus", 401)

            user.set_password(password)
            user.save()

            return(user)
        except Exception as e:
            raise AuthenticationFailed("Error bos", 401)

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        "bad_token": ("Token is expired or invalid")
    }

    def validate(self, attrs):
        self.token = attrs["refresh"]

        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except:
            self.fail("bad_token")