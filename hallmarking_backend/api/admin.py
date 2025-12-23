from django.contrib import admin
from .models import CenterInfo, Service, Certification, ServiceCertification


@admin.register(CenterInfo)
class CenterInfoAdmin(admin.ModelAdmin):
    """Admin interface for CenterInfo model."""
    list_display = ('name', 'contact_email', 'contact_phone')
    search_fields = ('name', 'description')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Admin interface for Service model."""
    list_display = ('name', 'price', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    """Admin interface for Certification model."""
    list_display = ('title', 'certificate_number', 'issued_date')
    search_fields = ('title', 'description', 'certificate_number')
    date_hierarchy = 'issued_date'


@admin.register(ServiceCertification)
class ServiceCertificationAdmin(admin.ModelAdmin):
    """Admin interface for ServiceCertification junction model."""
    list_display = ('service', 'certification')
    list_filter = ('service', 'certification')
