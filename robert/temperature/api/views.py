from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import DeviceSerializer
from temperature.models import Device
from rest_framework import status


@api_view()
@permission_classes([AllowAny])
def firstFunction(request, AllowPUTAsCreateMixin):
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
    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        print(params['pk'])
        devices = Device.objects.filter(pk=params['pk'])
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)
    
    # def retrieve(self, request, *args, **kwargs):
    #     params = kwargs
    #     print(params['pk'])
    #     params_list = params['pk'].split('-')
    #     devices = Device.objects.filter(
    #         owner=params_list[0], name=params_list[1])
    #     serializer = DeviceSerializer(devices, many=True)
    #     return Response(serializer.data) 

    # def create(self, request, *args, **kwargs):
    #     device_data = request.data

    #     new_device = Device.objects.create(name=device_data['name'], temperature=device_data['temperature'],
    #                                         online=device_data['online'], owner=int(device_data['owner']))
        
    #     new_device.save()

    #     serializer = DeviceSerializer(new_device)

    #     return Response(serializer.data)

    # def destroy(self, request, *args, **kwargs):
    #     loggedin_user = request.user
    #     if loggedin_user == 'admin':
    #         device = self.get_object()
    #         device.delete()
    #         response_message = {'message': "Item has been deleted"}
    #     else:
    #         response_message = {'message': 'Not Allowed'}

    #     return Response(response_message)

    @permission_classes([AllowAny])
    def destroy(self, request, *args, **kwargs):
        device = self.get_object()
        device.delete()
            
        return Response({'message': "Item has been deleted"})


    def put(self, request, *args, **kwargs):
        device = Device.objects.get()

        data = request.data

        device.name = data['name']
        device.temperature = data['temperature']
        device.humidity = data['humidity']
        device.online = data['online']
        
        device.save()

        serializer = DeviceSerializer(device)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        device = Device.objects.get()
        data = request.data

        device.name = data.get("name", device.name)
        device.temperature = data.get("temperature", device.temperature)
        device.online = data.get("online", device.online)
        device.humidity = data.get("humidity", device.humidity)

        device.save()
        serializer = DeviceSerializer(device)

        return Response(serializer.data)