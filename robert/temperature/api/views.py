from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import DeviceSerializer
from temperature.models import Device

@api_view()
@permission_classes([AllowAny])
def firstFunction(request):
    print(request.query_params)
    print(request.query_params['num'])
    number = request.query_params['num']
    new_number = int(number) * 2
    return Response({'message': "we received your request", 'result': new_number})


class DeviceViewset(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        devices = Device.objects.all()
        return devices

    # Endpoint for filtering only by owner id
    # def retrieve(self, request, *args, **kwargs):
    #     params = kwargs
    #     print(params['pk'])
    #     devices = Device.objects.filter(owner=params['pk'])
    #     serializer = DeviceSerializer(devices, many=True)
    #     return Response(serializer.data) 
    
    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        print(params['pk'])
        params_list = params['pk'].split('-')
        devices = Device.objects.filter(
            owner=params_list[0], name=params_list[1])
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data) 