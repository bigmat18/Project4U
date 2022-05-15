from Core.models import Project, Role
from Core.tests import BaseTestCase
from rest_framework import status
from django.test import tag

@tag('Projects','roles-tests')
class RoleTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()
        self.project = Project.objects.create(name="test",creator=self.user)
        self.role1 = Role.objects.create(name="role1", project=self.project)
        
    @tag('get', 'auth')   
    def test_role_list_auth(self):
        response = self.client.get(f"/api/projects/{self.project.id}/roles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    @tag('get', 'unauth')
    def test_role_list_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.get(f"/api/projects/{self.project.id}/roles/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    @tag('post', 'auth')
    def test_role_create_auth(self):
        data = {"name":"new_role"}
        response = self.client.post(f"/api/projects/{self.project.id}/roles/", data=data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
       
    @tag('post', 'unauth')
    def test_role_create_unauth(self):
        data = {"name":"new_role"}
        self.client.force_authenticate(user=self.new_user)
        self.project.users.add(self.new_user)
        response = self.client.post(f"/api/projects/{self.project.id}/roles/", data=data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    @tag('put', 'auth')
    def test_role_update_auth(self):
        data = {"name":"new_name"}
        response = self.client.patch(f"/api/role/{self.role1.id}/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(data, dict(response.json()))
       
    @tag('put', 'unauth')
    def test_role_update_unauth(self):
        data = {"name":"new_name"}
        self.client.force_authenticate(user=self.new_user)
        response = self.client.patch(f"/api/role/{self.role1.id}/", data=data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
      
    @tag('delete', 'auth')
    def test_role_delete_auth(self):
        response = self.client.delete(f"/api/role/{self.role1.id}/")
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        
    @tag('delete', 'unauth','this')  
    def test_role_delete_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.delete(f"/api/role/{self.role1.id}/")
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)