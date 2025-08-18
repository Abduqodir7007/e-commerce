from .utils import send_email
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import Http404
from rest_framework_simplejwt.views import TokenObtainPairView


class CreateUser(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [
        AllowAny,
    ]


class LoginView(TokenObtainPairView):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = LoginSerializer


class VerifyView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = VerifyViewSerializer()

    def post(self, request):

        serializers = VerifyViewSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)

        user = request.user
        code = serializers.validated_data["code"]  # type: ignore
        verify_type = serializers.validated_data["verify_type"]  # type: ignore
        self.check_code(user, code, verify_type)

        return Response(
            {
                "success": True,
                "access": user.token()["access"],
                "refresh": user.token()["refresh"],
            }
        )

    @staticmethod
    def check_code(user, code, verify_type):

        otp = user.codes.filter(
            user=user,
            code=code,
            expiration_time__gte=datetime.now(),
            is_confirmed=False,
        )

        if not otp.exists():
            data = {"msg": "Invalid code"}
            raise ValidationError(data)
        else:
            otp.update(is_confirmed=True, type=verify_type)

        return True


class ResetPassword(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = ResetPasswordSerializer()

    def post(self, request):
        try:
            data = request.data
            serializers = ResetPasswordSerializer(data=data)
            serializers.is_valid(raise_exception=True)

            user: User = User.objects.get(email=data.get("email"))

            if user is not None:
                code = user.create_code()
                send_email(code, user)

                return Response({"msg": "Code sent", "verification": ""})

        except User.DoesNotExist:
            raise Http404
        except Exception as e:
            raise e


class ResetPasswordFinish(UpdateAPIView):
    serializer_class = ResetPasswordFinishSer

    def get_object(self):
        return self.request.user


class GetNewCodeView(APIView):
    authentication_class = [
        IsAuthenticated,
    ]

    def post(self, request):
        user = request.user
        verify_type = request.data.get("type")
        self.check_code_exists(user, verify_type)
        code = user.create_code()

        send_email(code, user)

        return Response({"msg": "New code sent"})

    @staticmethod
    def check_code_exists(user, verify_type):
        code = user.codes.filter(
            user=user,
            expiration_time__gte=datetime.now(),
            is_confirmed=False,
        )

        code.update(type=verify_type)
        if code.exists():
            raise ValidationError({"msg": "You have valid code!"})
