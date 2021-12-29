from django.http import request
from .BaseTest import BaseTestCase
from Core.models import ExternalProject
from rest_framework import status

class ExternalProjectTestCase(BaseTestCase):
    
    def setUp(self):
        self.init_test(True)
        self.project = ExternalProject.objects.create(user=self.user,name="prova")
        
    def test_external_project_create_auth(self):
        request = self.client.post("/api/user/external-projects/", data={"name":"sdasd"})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        request = self.client.post("/api/user/external-projects/",format="json",data=[{"name":"sdasd"},{"name":"sdasd"}])
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        
    def test_external_project_create_unauth(self):
        self.client.logout()
        request = self.client.post("/api/user/external-projects/", data={"name":"sdasd"})
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_external_project_delete_auth(self):
        request = self.client.delete(f"/api/user/external-projects/{self.project.id}/")
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_external_project_updete_auth(self):
        request = self.client.patch(f"/api/user/external-projects/{self.project.id}/",
                                    data={"name":"asdasded"})
        self.assertEqual(request.status_code, status.HTTP_200_OK)