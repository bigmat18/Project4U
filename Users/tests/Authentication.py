from rest_framework import status
from Core.tests import BaseTestCase
from django.test import tag


@tag('Users', 'authentication-tests')
class LoginRegistrationTestCase(BaseTestCase):

    def setUp(self):
        self.data = self.init_test(True)
        self.data["password1"] = self.data["password2"] = self.data["password"]
        del self.data["password"]

    @tag('post')
    def test_registration_new_user(self):
        data = self.data
        data['email'] = "newemail@prova.com"
        data['date_birth'] = "2000-3-20"
        response = self.client.post("/api/auth/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @tag('post')
    def test_registration_same_user(self):
        response = self.client.post("/api/auth/registration/", self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag('post')
    def test_login(self):
        self.client.logout()
        data = {"email": self.email,"password": self.password} 
        response = self.client.post("/api/auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    @tag('get')  
    def test_logout_get(self):
        response = self.client.get("/api/auth/logout/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
     
    @tag('post')   
    def test_logout_post(self):
        response = self.client.post("/api/auth/logout/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)