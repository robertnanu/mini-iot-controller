from django.urls import reverse
from rest_framework.test import APITestCase, APIClient, RequestsClient
from .views import HTTP_200_OK, HTTP_201_CREATED
from .models import Device
from temperature.api.serializers import DeviceSerializer

# class DeviceViewsTest(APITestCase):
    # @classmethod
    # def setUpTestData(cls):
    #     # (1)
    #     cls.devices = [Device.objects.create() for _ in range(5)]
    #     cls.device = cls.devices[0]

    # def test_can_browse_all_devices(self):
    #     # (2)
    #     response = self.client.get(reverse("devices:device-list"))

    #     # (3)
    #     self.assertEquals(status.HTTP_200_OK, response.status_code)
    #     self.assertEquals(len(self.devices), len(response.data))

    #     for device in self.items:
    #         # (4)
    #         self.assertIn(
    #             DeviceSerializer(instance=device).data,
    #             response.data
    #         )
    
    # def test_cand_read_a_specific_device(self):
    #     # (5)
    #     response = self.client.get(
    #         reverse("devices:device-details", args=[self.device.id])
    #     )

    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     self.assertEqual(
    #         DeviceSerializer(instance=self.device).data,
    #         response.data
    #     )

    # def test_can_delete_a_device(self):
    #     response = self.client.delete(
    #         reverse("devices:device-detail", args=[self.device.id])
    #     )

    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     self.assertFalse(Device.objects.filter(pk=self.device.id))

# class RegistrationTestCase(APITestCase):

#     def test_registration(self):
#         data = {"name": "Testare", "online": True,
#                 "temperature": 23, "owner": 1}
#         response = self.client.post(reverse('get:devices'), data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeviceTestCases(APITestCase):

    def test_create(self):
        url = 'http://127.0.0.1:8888/get/devices/'
        data = {"name": "Testare", "online": True,
                "temperature": 23, "owner": 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
    
    def test_get(self):
        url = 'http://127.0.0.1:8888/get/devices/1/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_delete(self):
        url = 'http://127.0.0.1:8888/get/devices/'
        data = {4}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)