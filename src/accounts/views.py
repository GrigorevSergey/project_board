from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Users, VerificationCode
from .serializers import ConfirmCodeSerializer, PhoneNumberSerializer
from .signals import user_registered
from .tasks import send_sms


class RegistrationView(APIView):
    @swagger_auto_schema(
        operation_description="Регистрация по номеру телефона",
        request_body=PhoneNumberSerializer,
    )
    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            number_phone = serializer.validated_data["number_phone"]

            verification = VerificationCode.generate_code(number_phone)
            print(f"Код подтверждения для {number_phone}: {verification.code}")

            return Response({"detail": "Код отправлен"}, status=200)
        return Response(serializer.errors, status=400)


class ConfirmCodeView(APIView):
    @swagger_auto_schema(
        operation_description="Подтверждение телефона",
        request_body=ConfirmCodeSerializer,
    )
    def post(self, request):
        serializer = ConfirmCodeSerializer(data=request.data)
        if serializer.is_valid():
            number_phone = serializer.validated_data["number_phone"]
            code = serializer.validated_data["code"]

            try:
                verification = VerificationCode.objects.get(
                    number_phone=number_phone,
                    code=code,
                    is_used=False,
                    created_at__gte=timezone.now() - timezone.timedelta(minutes=5),
                )
            except VerificationCode.DoesNotExist:
                return Response({"error": "Неверный код"}, status=400)

            user, created = Users.objects.get_or_create(
                number_phone=number_phone, defaults={"username": number_phone}
            )

            if created:
                user_registered.send(sender=self.__class__, user=user)

            send_sms.delay(user.number_phone)

            verification.is_used = True
            verification.save()

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        return Response(serializer.errors, status=400)
