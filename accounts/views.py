from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile
from .serializers import (
    PasswordResetSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
)


class RegisterView(generics.CreateAPIView):
    """
    User Registration Endpoint
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "message": "User registered successfully",
                "user": {"id": user.id, "username": user.username, "email": user.email},
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(generics.GenericAPIView):
    """
    User Login Endpoint
    """

    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {"id": user.id, "username": user.username, "email": user.email},
            }
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    User Profile View and Update
    """

    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class PasswordResetView(generics.GenericAPIView):
    """
    Password Reset Endpoint
    """

    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"message": "Password updated successfully"}, status=status.HTTP_200_OK
        )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    Logout endpoint to blacklist refresh token
    """
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(
            {"message": "Successfully logged out"}, status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
