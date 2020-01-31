from django.conf import settings
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.serializers.auth import *

from api.serializers.user import ProfileSerializer

sensitive = method_decorator(
    sensitive_post_parameters("password", "old_password", "new_password")
)


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    @sensitive
    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def get_response_data(self, user):
        data = {"user": user, "refresh": str(self.refresh), "access": str(self.access)}
        return JWTSerializer(data).data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            self.get_response_data(user),
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer):
        user = serializer.create(self.request.data)
        self.refresh = RefreshToken.for_user(user)
        self.access = self.refresh.access_token
        return user


class VerifyEmailView(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ("POST", "OPTIONS", "HEAD")

    def get_object(self):
        pass

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs["key"] = serializer.validated_data["key"]
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({"detail": _("ok")}, status=status.HTTP_200_OK)


class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @sensitive
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def process_login(self):
        django_login(self.request, self.user)

    def login(self):
        self.user = self.serializer.validated_data["user"]
        self.refresh = RefreshToken.for_user(self.user)
        self.access = self.refresh.access_token

        self.process_login()

    def get_response(self):
        serializer_class = JWTSerializer

        data = {
            "user": self.user,
            "refresh": str(self.refresh),
            "access": str(self.access),
        }

        serializer = serializer_class(instance=data, context={"request": self.request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(
            data=self.request.data, context={"request": request}
        )
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        return self.logout(request)

    def logout(self, request):
        if settings.REST_SESSION_LOGIN:
            django_logout(request)

        return Response(
            {"detail": _("Logged out successfully.")}, status=status.HTTP_200_OK
        )


class ProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return User.objects.all()

    def perform_update(self, serializer):
        instance = self.get_object()

        birth_date = self.request.data.get("birth_date", None)
        pincode = self.request.data.get("pincode", None)
        about = self.request.data.get("about", None)

        if instance.is_student and birth_date:
            instance.student.birth_date = birth_date
            instance.student.save()

        if instance.is_institute:
            if pincode:
                instance.institute.pincode = pincode
            instance.institute.about = about
            instance.institute.save()

        serializer.save()