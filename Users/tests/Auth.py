from rest_framework import status
from rest_framework.test import APITestCase
from Core.models import User


class LoginRegistrationTestCase(APITestCase):
    first_name    = "prova"
    last_name     = "prova"
    email         = "prova@prova.com"
    password      = "prova1234567_"

    def setUp(self):
        self.user = User.objects.create_user(password=self.password,email=self.email,
                                             first_name=self.first_name,last_name=self.last_name)
        self.data = {"first_name": self.first_name,"last_name":self.last_name, 
                    "email": self.email,"password1": self.password,
                    "password2": self.password} 

    def test_registration_new_user(self):
        data = self.data
        data['email'] = "newemail@prova.com"
        response = self.client.post("/api/auth/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_same_user(self):
        response = self.client.post("/api/auth/registration/", self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        self.client.logout()
        data = {"email": self.email,"password": self.password} 
        response = self.client.post("/api/auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)