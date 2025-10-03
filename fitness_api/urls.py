from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
    openapi.Info(
        title = 'Fitness API',
        default_version = 'v1',
        description = 'Fitness Api for tracking weight and making workout plans'
    ),
    public = True,
    permission_classes = [AllowAny]
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fitness_app.urls')),
    path('api/swagger(<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
