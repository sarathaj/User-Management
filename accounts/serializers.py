from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    password_confirm = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )
    full_name = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ("email", "password", "password_confirm", "full_name")
        extra_kwargs = {
            "email": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Passwords don't match"}
            )
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        full_name = validated_data.pop("full_name", "")
        validated_data.pop("password_confirm")

        # Use email as username
        user = User.objects.create_user(
            username=validated_data["email"], **validated_data
        )

        # Update profile if full_name is provided
        if full_name:
            user.profile.full_name = full_name
            user.profile.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            # We need to find the user by email first, then authenticate
            try:
                user_obj = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid credentials")

            user = authenticate(username=user_obj.username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled")
            attrs["user"] = user
        else:
            raise serializers.ValidationError("Must include email and password")

        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = UserProfile
        fields = [
            "username",
            "email",
            "full_name",
            "date_of_birth",
            "address",
            "gender",
            "mobile_number",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate_email(self, value):
        """
        Check that the email is not already in use by another user.
        """
        # The user is available in the context when updating
        user = self.context["request"].user
        if User.objects.filter(email__iexact=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def update(self, instance, validated_data):
        # Pop the 'user' data which contains the email
        user_data = validated_data.pop("user", {})
        email = user_data.get("email")

        if email:
            instance.user.email = email
            instance.user.save()

        # Update profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PasswordResetSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={"input_type": "password"})
    new_password = serializers.CharField(
        validators=[validate_password], style={"input_type": "password"}
    )
    new_password_confirm = serializers.CharField(style={"input_type": "password"})

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError("New passwords don't match")
        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Invalid old password")
        return value
