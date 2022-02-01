from rest_framework import serializers
from temperature.models import Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['name', 'online', 'temperature', 'owner']