from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import CenterInfo, Service, Certification
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    CenterInfoSerializer,
    ServiceSerializer,
    ServiceDetailSerializer,
    CertificationSerializer
)


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method='get',
    operation_summary="Health Check",
    operation_description="Returns server health status",
    responses={200: openapi.Response('Server is healthy', openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'message': openapi.Schema(type=openapi.TYPE_STRING)}
    ))},
    tags=['Health']
)
@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
    """Health check endpoint to verify server is running."""
    return Response({"message": "Server is up!"})


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method='post',
    operation_summary="User Registration",
    operation_description="Register a new user account",
    request_body=UserRegistrationSerializer,
    responses={
        201: openapi.Response('User created successfully', UserSerializer),
        400: 'Bad request - validation errors'
    },
    tags=['Authentication']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user.
    
    Accepts username, email, password, and optional first_name/last_name.
    Returns the created user data (excluding password).
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user_data = UserSerializer(user).data
        return Response({
            'message': 'User registered successfully',
            'user': user_data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method='post',
    operation_summary="User Login",
    operation_description="Authenticate user and create session",
    request_body=UserLoginSerializer,
    responses={
        200: openapi.Response('Login successful', UserSerializer),
        401: 'Invalid credentials'
    },
    tags=['Authentication']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Authenticate user and create session.
    
    Accepts username and password.
    Returns user data on successful authentication.
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_data = UserSerializer(user).data
            return Response({
                'message': 'Login successful',
                'user': user_data
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method='post',
    operation_summary="User Logout",
    operation_description="End user session",
    responses={
        200: openapi.Response('Logout successful', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'message': openapi.Schema(type=openapi.TYPE_STRING)}
        ))
    },
    tags=['Authentication']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    End user session.
    
    Requires authentication.
    Logs out the current user.
    """
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method='get',
    operation_summary="Get Current User",
    operation_description="Retrieve authenticated user information",
    responses={
        200: openapi.Response('User data', UserSerializer),
        401: 'Not authenticated'
    },
    tags=['Authentication']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Get current authenticated user information.
    
    Requires authentication.
    Returns user data for the currently logged-in user.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method='get',
    operation_summary="Get Center Information",
    operation_description="Retrieve hallmarking center details",
    responses={
        200: openapi.Response('Center information', CenterInfoSerializer),
        404: 'Center info not found'
    },
    tags=['Center Info']
)
@api_view(['GET'])
@permission_classes([AllowAny])
def center_info(request):
    """
    Get hallmarking center information.
    
    Returns details about the center including name, description,
    address, and contact information.
    """
    try:
        # Assuming there's only one center info record
        center = CenterInfo.objects.first()
        if center is None:
            return Response(
                {'error': 'Center information not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CenterInfoSerializer(center)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method='get',
    operation_summary="List Services",
    operation_description="Retrieve all active hallmarking services",
    manual_parameters=[
        openapi.Parameter(
            'include_inactive',
            openapi.IN_QUERY,
            description="Include inactive services (true/false)",
            type=openapi.TYPE_BOOLEAN,
            required=False
        )
    ],
    responses={
        200: openapi.Response('List of services', ServiceSerializer(many=True))
    },
    tags=['Services']
)
@api_view(['GET'])
@permission_classes([AllowAny])
def service_list(request):
    """
    Get list of hallmarking services.
    
    By default returns only active services.
    Use ?include_inactive=true to include inactive services.
    """
    include_inactive = request.query_params.get('include_inactive', 'false').lower() == 'true'
    
    if include_inactive:
        services = Service.objects.all()
    else:
        services = Service.objects.filter(is_active=True)
    
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method='get',
    operation_summary="Get Service Details",
    operation_description="Retrieve detailed information about a specific service including certifications",
    responses={
        200: openapi.Response('Service details', ServiceDetailSerializer),
        404: 'Service not found'
    },
    tags=['Services']
)
@api_view(['GET'])
@permission_classes([AllowAny])
def service_detail(request, service_id):
    """
    Get detailed information about a specific service.
    
    Returns service details including related certifications.
    """
    try:
        service = Service.objects.get(id=service_id)
        serializer = ServiceDetailSerializer(service)
        return Response(serializer.data)
    except Service.DoesNotExist:
        return Response(
            {'error': 'Service not found'},
            status=status.HTTP_404_NOT_FOUND
        )


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method='get',
    operation_summary="List Certifications",
    operation_description="Retrieve all certifications held by the center",
    responses={
        200: openapi.Response('List of certifications', CertificationSerializer(many=True))
    },
    tags=['Certifications']
)
@api_view(['GET'])
@permission_classes([AllowAny])
def certification_list(request):
    """
    Get list of certifications.
    
    Returns all certifications with related services.
    """
    certifications = Certification.objects.all()
    serializer = CertificationSerializer(certifications, many=True)
    return Response(serializer.data)


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method='get',
    operation_summary="Get Certification Details",
    operation_description="Retrieve detailed information about a specific certification",
    responses={
        200: openapi.Response('Certification details', CertificationSerializer),
        404: 'Certification not found'
    },
    tags=['Certifications']
)
@api_view(['GET'])
@permission_classes([AllowAny])
def certification_detail(request, certification_id):
    """
    Get detailed information about a specific certification.
    
    Returns certification details including related services.
    """
    try:
        certification = Certification.objects.get(id=certification_id)
        serializer = CertificationSerializer(certification)
        return Response(serializer.data)
    except Certification.DoesNotExist:
        return Response(
            {'error': 'Certification not found'},
            status=status.HTTP_404_NOT_FOUND
        )


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method='get',
    operation_summary="Get Portfolio Data",
    operation_description="Retrieve complete portfolio including services and certifications",
    responses={
        200: openapi.Response('Portfolio data', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'services': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT)),
                'certifications': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT))
            }
        ))
    },
    tags=['Portfolio']
)
@api_view(['GET'])
@permission_classes([AllowAny])
def portfolio(request):
    """
    Get complete portfolio data.
    
    Returns all services and certifications in a single response.
    Useful for displaying the center's complete portfolio.
    """
    services = Service.objects.filter(is_active=True)
    certifications = Certification.objects.all()
    
    return Response({
        'services': ServiceSerializer(services, many=True).data,
        'certifications': CertificationSerializer(certifications, many=True).data
    })
