from django.http import request
from Core.tests import BaseTestCase
from Core.models import ExternalProject
from rest_framework import status
from django.test import tag


@tag('Users')
class ExternalProjectTestCase(BaseTestCase):
    
    def setUp(self):
        self.init_test(True)
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
    def test_external_project_updete_auth(self):
        data = {"name":"test"}
        response = self.client.patch(f"/api/user/external-projects/{self.project.id}/",data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(data, dict(response.json()))
