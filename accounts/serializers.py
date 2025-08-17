from .models import User
from accounts.utils import send_email
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class SignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email exists")

        return value.lower()

    def validate(self, data):
        first_name = data.get("first_name", None)
        last_name = data.get("last_name", None)
        password = data.get("password", None)

        if password is not None:
            validate_password(password)

        if len(first_name) < 4 or len(first_name) > 30 or first_name.isdigit():
            raise ValidationError("Invalid first name")

        if len(last_name) < 4 or len(last_name) > 30 or last_name.isdigit():
            raise ValidationError("Invalid last name")
        return data

    def to_representation(self, instance):
        data = super(SignUpSerializer, self).to_representation(instance)
        data.update(instance.token())

        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        code = user.create_code()
        send_email(code, user.email)
        return user


class VerifyViewSerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)
    verify_type = serializers.CharField(write_only=True, required=True)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        value = value.lower()
        return value


class ResetPasswordFinishSer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        password = data.get("password", None)
        password2 = data.get("confirm_password", None)

        if password != password2:
            data = {"msg": "Parol does not match"}
            raise ValidationError(data)

        if password is not None:
            validate_password(password)
            validate_password(password2)

        return data


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    def auth_validate(self, data):
        user = authenticate(email=data.get("email"), password=data.get("password"))

        if user is not None:
            self.user = user
        else:
            raise ValidationError({"msg": "Invalid Credentials"})
        
        return user

    def validate(self, data):
        self.auth_validate(data)
        data = super().validate(data) 
        return data
