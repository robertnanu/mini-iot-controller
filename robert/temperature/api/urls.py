from xml.etree.ElementInclude import default_loader
from django.urls import path, include
from .views import firstFunction
from rest_framework.routers import DefaultRouter
from .views import DeviceViewset
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
router.register('devices', DeviceViewset, basename='devices')

urlpatterns = [
    path('first', firstFunction),
    path('', include(router.urls)),
    # path('docs/', include_docs_urls(title='Snippet API')),
]