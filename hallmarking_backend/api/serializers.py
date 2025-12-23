from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import CenterInfo, Service, Certification


# PUBLIC_INTERFACE
class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Validates password and creates new user accounts.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def validate_email(self, value):
        """Validate that email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        """Validate that username is unique."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def create(self, validated_data):
        """Create and return a new user."""
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


# PUBLIC_INTERFACE
class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Accepts username and password credentials.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )


# PUBLIC_INTERFACE
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user data.
    Returns user information (excluding password).
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('id', 'date_joined')


# PUBLIC_INTERFACE
class CenterInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for hallmarking center information.
    Returns details about the center including contact information.
    """
    class Meta:
        model = CenterInfo
        fields = ('id', 'name', 'description', 'address', 'contact_email', 'contact_phone')
        read_only_fields = ('id',)


# PUBLIC_INTERFACE
class ServiceSerializer(serializers.ModelSerializer):
    """
    Serializer for hallmarking services.
    Returns service details including pricing and active status.
    """
    class Meta:
        model = Service
        fields = ('id', 'name', 'description', 'price', 'is_active')
        read_only_fields = ('id',)


# PUBLIC_INTERFACE
class CertificationSerializer(serializers.ModelSerializer):
    """
    Serializer for certifications.
    Returns certification details with optional related services.
    """
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Certification
        fields = ('id', 'title', 'description', 'issued_date', 'certificate_number', 'services')
        read_only_fields = ('id',)


# PUBLIC_INTERFACE
class ServiceDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for services including related certifications.
    Returns service with all associated certifications.
    """
    certifications = CertificationSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = ('id', 'name', 'description', 'price', 'is_active', 'certifications')
        read_only_fields = ('id',)
