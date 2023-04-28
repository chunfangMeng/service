from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('api/v1/', include('apps.member.urls')),
    path('api/v1/manager', include('apps.manager.urls')),
    path('api/v1/open/', include('apps.webapp.urls')),
    path('api/v1/stock/', include('apps.product.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
]
