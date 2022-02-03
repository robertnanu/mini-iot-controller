from rest_framework import serializers
from temperature.models import Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'name', 'online', 'temperature', 'owner']
        # fields = ['temperature']