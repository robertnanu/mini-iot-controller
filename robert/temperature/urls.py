from django.urls import path, include
from rest_framework import routers

from . import views

# router = routers.DefaultRouter()
# router.register('devices', views.DeviceView)

urlpatterns = [
    path('', views.Index, name = 'index'),

    path('register/', views.registerPage, name = 'register'),
    path('login/', views.loginPage, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('home/', views.home, name = 'home'),
    path('ajax/change-state/', views.change_state, name = 'change-state'),
    path('ajax/change-temp/', views.change_temp, name = 'change-temp'),
    path('addThermostat/', views.addThermostat, name = 'addThermostat'),
    # path('test/', include(router.urls))
]
