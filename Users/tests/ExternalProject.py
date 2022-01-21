from django.http import request
from Core.tests import BaseTestCase
from Core.models import ExternalProject
from rest_framework import status
from django.test import tag
import PIL, tempfile


@tag('Users', 'external-projects-tests')
class ExternalProjectTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()
        self.project = ExternalProject.objects.create(user=self.user,name="prova")
    
    @tag('post','auth') 
    def test_external_project_create_auth(self):
        response = self.client.post("/api/user/external-projects/", data={"name":"sdasd"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post("/api/user/external-projects/",format="json",data=[{"name":"sdasd"},{"name":"sdasd"}])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, list)
       
    @tag('post','unauth')  
    def test_external_project_create_unauth(self):
        self.client.logout()
        response = self.client.post("/api/user/external-projects/", data={"name":"sdasd"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @tag('delete','auth')  
    def test_external_project_delete_auth(self):
        response = self.client.delete(f"/api/user/external-projects/{self.project.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    @tag('put','auth') 
    def test_external_project_update_auth(self):
        data = {"name":"test"}
        response = self.client.patch(f"/api/user/external-projects/{self.project.id}/",data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(data, dict(response.json()))

    @tag('put','auth','file')
    def test_external_project_update_image_auth(self):
        image = PIL.Image.new('RGB', size=(1, 1))
        file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(file)
        with open(file.name, 'rb') as file_open:
            response = self.client.patch(f"/api/user/external-projects/{self.project.id}/", 
                                         data={"image": file_open}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)