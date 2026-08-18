from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Wildberries API",
        default_version='v1',
        description="Документация API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('store_app.urls')),
    path('accounts/', include('allauth.urls')),
)

urlpatterns += [
    re_path(r'^docs(?P<format>\.json|\.yaml)$', schema_view(cache_timeout=0).without_ui(), name='schema-json'),
    path('docs/', schema_view(cache_timeout=0).with_ui('swagger'), name='schema-swagger-ui'),
    path('redoc/', schema_view(cache_timeout=0).with_ui('redoc'), name='schema-redoc'),
]