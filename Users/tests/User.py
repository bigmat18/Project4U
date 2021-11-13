from rest_framework import status
from rest_framework.test import APITestCase
from Core.models import User
from rest_framework_api_key.models import APIKey


class UsersTestCase(APITestCase):
    first_name = "prova"
    last_name = "prova"
    email_user = "prova@prova.com"
    password = "prova1234567_"
    
    def setUp(self):
        self.user = User.objects.create_user(password=self.password,email=self.email_user,
                                             first_name=self.first_name,last_name=self.last_name)
        key = APIKey.objects.create_key(name="prova")
        self.client.credentials(HTTP_X_API_KEY=key[1])
        
    def test_current_user_put_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put("/api/user/", {"highscool": "sdad"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_current_user_put_un_auth(self):
        response = self.client.put("/api/user/", {"highscool": "sdad"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 

    def test_user_list_un_auth(self):
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_user_list_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_user_detail_un_auth(self):
        response = self.client.get(f"/api/users/{self.user.slug}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_user_detail_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/users/{self.user.slug}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)