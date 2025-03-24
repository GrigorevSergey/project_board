from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import ConfirmCodeView, RegistrationView

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("confirm/", ConfirmCodeView.as_view(), name="confirm_code"),
]
