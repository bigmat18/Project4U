from django.http import request, response
from Core.models import Project, User, Role
from Core.tests import BaseTestCase
from rest_framework import status


class RoleTestCase(BaseTestCase):
    
    def setUp(self):
        self.init_test(True)
        self.project = Project.objects.create(name="test",creator=self.user)
        self.role1 = Role.objects.create(name="role1", project=self.project)
        self.user1 = User.objects.create_user(email=f"2{self.email}",password=self.password,
                                              first_name=self.first_name,last_name=self.last_name)
        
        
    def test_role_list_auth(self):
        response = self.client.get(f"/api/projects/{self.project.id}/roles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_role_list_unauth(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f"/api/projects/{self.project.id}/roles/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
    def test_role_create_auth(self):
        data = {"name":"new_role"}
        response = self.client.post(f"/api/projects/{self.project.id}/roles/", data=data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
       
        
    def test_role_create_unauth(self):
        data = {"name":"new_role"}
        self.client.force_authenticate(user=self.user1)
        self.project.users.add(self.user1)
        response = self.client.post(f"/api/projects/{self.project.id}/roles/", data=data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)


    def test_role_update_auth(self):
        data = {"name":"new_name"}
        response = self.client.patch(f"/api/role/{self.role1.id}/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(data, dict(response.json()))
       
        
    def test_role_update_unauth(self):
        data = {"name":"new_name"}
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(f"/api/role/{self.role1.id}/", data=data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
      
        
    def test_role_delete_auth(self):
        response = self.client.delete(f"/api/role/{self.role1.id}/")
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        
        
    def test_role_delete_unauth(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f"/api/role/{self.role1.id}/")
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)