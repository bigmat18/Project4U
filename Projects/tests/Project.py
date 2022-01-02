from django.http import request, response
from Core.models import Project, User
from Core.tests import BaseTestCase
from rest_framework import status

class ProjectsTestCase(BaseTestCase):
    
    def setUp(self):
        self.init_test(True)
        self.project = Project.objects.create(name="test", creator=self.user)
        self.new_user = User.objects.create_user(email=f"2{self.email}", password=self.email,
                                            first_name=self.first_name, last_name=self.last_name)
        
        
    def test_projects_list_auth(self):
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_projects_list_unauth(self):
        self.client.logout()
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_projects_create_auth(self):
        response = self.client.post('/api/projects/', data={"name": "test1"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_projects_update_auth(self):
        data = {"name":"new_name"}
        response = self.client.patch(f'/api/projects/{self.project.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(data, dict(response.json()))
        
        response = self.client.put(f'/api/projects/{self.project.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(data, dict(response.json()))

    def test_projects_update_unauth(self):
        data = {"name":"new_name"}
        self.client.force_authenticate(user=self.new_user)
        response = self.client.patch(f'/api/projects/{self.project.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_projects_delete_auth(self):
        response = self.client.delete(f'/api/projects/{self.project.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_projects_delete_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.delete(f'/api/projects/{self.project.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)