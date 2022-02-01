from rest_framework import serializers
from .models import Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        # fields = ('name', 'temperature', 'owner')
        fields = '__all__'