from django.http import request, response
from Core.models import Project, User, Role, UserProject
from Core.tests import BaseTestCase
from rest_framework import status


class UserProjectTestCase(BaseTestCase):
    
    def setUp(self):
        self.init_test(True)
        self.project = Project.objects.create(name="test",creator=self.user)
        self.role = Role.objects.create(name="test1", project=self.project)
        self.user1 = User.objects.create_user(email=f"2{self.email}",password=self.password,
                                              first_name=self.first_name,last_name=self.last_name)
        self.user_project = UserProject.objects.create(user=self.user,project=self.project)
        
        
    def test_user_project_list_auth(self):
        response = self.client.get(f"/api/projects/{self.project.id}/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_user_project_list_unauth(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(f"/api/projects/{self.project.id}/users/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    
    def test_user_project_create_auth(self):
        response = self.client.post(f"/api/projects/{self.project.id}/users/", data={"user":str(self.user1.id)})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(f"/api/projects/{self.project.id}/users/", data={"user":str(self.user.id)})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(dict(response.json()),{"Error":"Utente già aggiunto al progetto"})
        
    def test_user_project_create_unauth(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(f"/api/projects/{self.project.id}/users/", data={"user":str(self.user1.id)})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    
    def test_user_project_update_auth(self):
        data = {"role":[str(self.role.id)]}
        response = self.client.patch(f"/api/projects/users/{self.user_project.id}/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(data, dict(response.json()))
        
    def test_user_project_update_unauth(self):
        self.client.force_authenticate(user=self.user1)
        data = {"role":[str(self.role.id)]}
        response = self.client.patch(f"/api/projects/users/{self.user_project.id}/", data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    
    def test_user_project_delete_auth(self):
        response = self.client.delete(f"/api/projects/users/{self.user_project.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_user_project_delete_unauth(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f"/api/projects/users/{self.user_project.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)