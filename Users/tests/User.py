from rest_framework import response, status
from Core.tests import BaseTestCase
from django.test import tag
import PIL, tempfile

@tag('Users', 'users-tests')
class UserTestCase(BaseTestCase):
    
    def setUp(self): self.baseSetup()
        
    @tag('put','auth')
    def test_current_user_update_auth(self):
        data = {"description": "sdad"}
        response = self.client.put("/api/user/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(data, dict(response.json()))
        
        response = self.client.patch("/api/user/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(data, dict(response.json()))
        
    @tag('put','auth','file')
    def test_current_user_update_image_auth(self):
        image = PIL.Image.new('RGB', size=(1, 1))
        file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(file)
        with open(file.name, 'rb') as file_open:
            response = self.client.patch("/api/user/", data={"image": file_open}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag('put','unauth') 
    def test_current_user_update_unauth(self):
        self.client.logout()
        response = self.client.put("/api/user/", {"description": "sdad"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    @tag('get','auth','file')
    def test_current_user_image_auth(self):
        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.user.image = image
        response = self.client.get('/api/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["image"], f"http://testserver/media{image}")
    
    @tag('get','auth')
    def test_users_list_auth(self):
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    @tag('get','auth')
    def test_users_detail_auth(self):
        response = self.client.get(f"/api/users/{self.user.slug}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
    def test_user_image(self):
        response = self.client.get('/api/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)