from django.http import request
from Core.tests import BaseTestCase
from Core.models import ExternalProject
from rest_framework import status

class ExternalProjectTestCase(BaseTestCase):
    
    def setUp(self):
        self.init_test(True)
        self.project = ExternalProject.objects.create(user=self.user,name="prova")
        
    def test_external_project_list_creation(self):
        request = self.client.post("/api/user/external-projects/", format="json", data=[
                                                                                {"name":"sdasd"},
                                                                                {"name":"sdasd"}])
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
    
    def test_external_project_creation(self):
        request = self.client.post("/api/user/external-projects/", data={"name":"sdasd"})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_external_project_delete(self):
        request = self.client.delete(f"/api/user/external-projects/{self.project.id}/")
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_external_project_updete(self):
        request = self.client.patch(f"/api/user/external-projects/{self.project.id}/",
                                    data={"name":"asdasded"})
        self.assertEqual(request.status_code, status.HTTP_200_OK)