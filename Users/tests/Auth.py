from rest_framework import status
from .BaseTest import BaseTestCase


class LoginRegistrationTestCase(BaseTestCase):

    def setUp(self):
        self.data = self.init_test()
        self.data["password1"] = self.data["password2"] = self.data["password"]
        del self.data["password"]

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