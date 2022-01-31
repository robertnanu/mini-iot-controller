from django.contrib import auth
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import paho.mqtt.client as mqtt
import time

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Device
from .forms import CreateUserForm, DeviceForm

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

def addThermostat(request):
    form = DeviceForm()

    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/home')

    context = {'form':form}

    return render(request, 'temperature/thermostat.html', context)