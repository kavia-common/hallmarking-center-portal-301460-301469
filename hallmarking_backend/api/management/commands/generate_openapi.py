import json
import os
import django

from django.core.management.base import BaseCommand
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator

class Command(BaseCommand):
    help = 'Generate OpenAPI schema for the API'
    
    def handle(self, *args, **options):
        # Ensure Django is set up
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        django.setup()
        
        # Create schema generator
        generator = OpenAPISchemaGenerator(
            info=openapi.Info(
                title='Hallmarking Center API',
                default_version='v1',
                description="""
API for Hallmarking Center Portal

This API provides endpoints for:
- User registration and authentication
- Hallmarking center information
- Services portfolio
- Certifications management

## Authentication
The API uses session-based authentication. Users must register and login to access protected endpoints.

## CORS
The API is configured to accept requests from the frontend at http://localhost:3000
                """,
                contact=openapi.Contact(email="admin@hallmarkingcenter.com"),
            ),
            version='v1',
            url='http://localhost:3001',
        )
        
        # Get the schema
        schema = generator.get_schema(None, True)
        
        # Convert to dictionary
        schema_dict = schema.as_odict()
        
        output_dir = "interfaces"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "openapi.json")

        with open(output_path, "w") as f:
            json.dump(schema_dict, f, indent=2)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully generated OpenAPI schema at {output_path}'))
        self.stdout.write(self.style.SUCCESS(f'Total endpoints: {len(schema_dict.get("paths", {}))}'))
