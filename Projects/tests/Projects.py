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
        
        
    def test_projects_list(self):
        self.client.logout()
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_login(user=self.user)
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        
    def test_projects_create(self):
        response = self.client.post('/api/projects/', data={"name": "test1"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    
    def test_projects_update(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.put(f'/api/projects/{self.project.id}/', data={"name":"new_name"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.put(f'/api/projects/{self.project.id}/', data={"name":"new_name"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    
    def test_projects_delete(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.delete(f'/api/projects/{self.project.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/projects/{self.project.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)