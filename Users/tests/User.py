from rest_framework import response, status
from .BaseTest import BaseTestCase, User


class UsersTestCase(BaseTestCase):
    
    def setUp(self): self.init_test(True)
        
    def test_current_user_update_auth(self):
        response = self.client.put("/api/user/", {"description": "sdad"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_current_user_update_unauth(self):
        self.client.logout()
        response = self.client.put("/api/user/", {"description": "sdad"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_current_user_image_auth(self):
        response = self.client.get('/api/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_user_list_auth(self):
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_user_detail_auth(self):
        response = self.client.get(f"/api/users/{self.user.slug}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)