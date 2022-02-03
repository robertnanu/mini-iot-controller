"""robert URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from temperature import views
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('temperature.urls')),
    # path('addDevice', views.add_thermostat_api),
    # path('devices/', views.DeviceList.as_view()),
    path('get/', include('temperature.api.urls')),
    path('docs/', include_docs_urls(title='Snippet API')),
    path('schema', get_schema_view(
        title="DeviceAPI",
        description="API for Device",
        version='1.0.0'
    ), name='openapi-schema'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)