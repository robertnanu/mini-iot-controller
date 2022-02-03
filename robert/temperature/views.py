import json
import requests
from django.contrib import auth
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
import paho.mqtt.client as mqtt
import time

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Device
from .forms import CreateUserForm, DeviceForm
# from .serializers import DeviceSerializer
# from temperature import serializers

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created succesfully for the user: ' + user)
            return redirect('login')

    context = {'form':form}

    return render(request, 'temperature/register.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect!')

    context = {}

    return render(request, 'temperature/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def Index(request):
    devices = Device.objects.order_by('id')

    context = {'devices' : devices}

    return render(request, 'temperature/index.html', context)

def home(request):
    devices = Device.objects.filter(owner=request.user)

    context = {'devices':devices}

    return render(request, 'temperature/home.html', context)

def change_state(request):
    device_id = request.POST.get('device_id')

    device = Device.objects.get(id=device_id)
    
    if device is None:
        return JsonResponse({'error' : 'Device not found!'})

    device.online = False if device.online else True
    device.save()

    return JsonResponse({'online' : device.online })
from rest_framework import status
HTTP_201_CREATED = status.HTTP_400_BAD_REQUEST
HTTP_200_OK = status.HTTP_405_METHOD_NOT_ALLOWED
def change_temp(request):
    device_id = request.POST.get('device_id')
    temperature = request.POST.get('temperature')
    device = Device.objects.get(id=device_id)

    if device is None:
        return JsonResponse({'error' : 'Device not found!'})

    device.temperature = temperature

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("connected OK")
        else:
            print("Bad connection; Returned code: ", rc)

    def on_disconnect(client, userdata, flags, rc = 0):
        print("Disconnected result code:" + str(rc))

    def on_message(client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        print("message received:", m_decode)

    broker = "test.mosquitto.org"
    client = mqtt.Client("python1")

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    print("Connecting to broker:", broker)

    client.connect(broker)
    client.loop_start()
    client.subscribe("house/device")
    client.publish("house/device", temperature)
    time.sleep(1)
    client.loop_stop()
    client.disconnect()

    device.save()

    return JsonResponse({'temperature' : device.temperature})

@csrf_exempt
def addThermostat(request):
    form = DeviceForm()

    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/home')

    context = {'form':form}

    return render(request, 'temperature/thermostat.html', context)

# @csrf_exempt
# def add_thermostat_api(request):
#     if request.method == 'POST':
#         payload = json.loads(request.body)
#         thermostat_name = payload['thermostat_name']
#         thermostat_temperature = payload['thermostat_temperature']
#         thermostat_owner = payload['thermostat_owner']
#         device = Device(name=thermostat_name, temperature=thermostat_temperature, owner=thermostat_owner)
#         try:
#             device.save()
#             response = json.dumps([{ 'Success': 'Device added successfully!'}])
#         except:
#             response = json.dumps([{ 'Error': 'Device could not be added!'}])
    
#     return HttpResponse(response, content_type='text/json')

# class DeviceList(APIView):

#     ENDPOINTS = {
#         'DELETE_DEVICE': 'localhost:8888/delete/{}',
#     }

#     serializer_class = DeviceSerializer

#     def get_queryset(self):
#         devices = Device.objects.all()
#         return devices

#     def get(self, request, *args, **kwargs):
#         devices = self.get_queryset()
#         serializer_class = DeviceSerializer(devices, many=True)

#         return Response(serializer_class.data)

#     @csrf_exempt
#     def post(self, request):
#         if request.method == 'POST':
#             payload = json.loads(request.body)
#             thermostat_name = payload['thermostat_name']
#             thermostat_temperature = payload['thermostat_temperature']
#             thermostat_owner = payload['thermostat_owner']
#             device = Device(name=thermostat_name, temperature=thermostat_temperature, owner=thermostat_owner)
#             try:
#                 device.save()
#                 response = json.dumps([{ 'Success': 'Device added successfully!'}])
#             except:
#                 response = json.dumps([{ 'Error': 'Device could not be added!'}])
    
#         return HttpResponse(response, content_type='text/json')

#     def delete_device(self, device_id):
#         try:
#             response = requests.delete(self.ENDPOINTS['DELETE_DEVICE'].format(device_id))

#             if response.status_code == 204:
#                 response = json.dumps([{ 'Success': 'Device added successfully!'}])
#         except:
#             response = json.dumps([{ 'Error': 'Device could not be added!'}])

#         return HttpResponse(response, content_type='test/json')
            