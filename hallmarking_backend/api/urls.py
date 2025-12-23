from django.urls import path
from .views import (
    health,
    register,
    login_view,
    logout_view,
    current_user,
    center_info,
    service_list,
    service_detail,
    certification_list,
    certification_detail,
    portfolio
)

urlpatterns = [
    # Health check
    path('health/', health, name='health'),
    
    # Authentication endpoints
    path('auth/register/', register, name='register'),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/user/', current_user, name='current_user'),
    
    # Center information
    path('center/', center_info, name='center_info'),
    
    # Services
    path('services/', service_list, name='service_list'),
    path('services/<int:service_id>/', service_detail, name='service_detail'),
    
    # Certifications
    path('certifications/', certification_list, name='certification_list'),
    path('certifications/<int:certification_id>/', certification_detail, name='certification_detail'),
    
    # Portfolio (combined services and certifications)
    path('portfolio/', portfolio, name='portfolio'),
]
