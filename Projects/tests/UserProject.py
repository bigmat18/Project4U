from Core.models import Project, Role, UserProject, Showcase
from Core.tests import BaseTestCase
from rest_framework import status
from django.test import tag
from django.db.models import Q


@tag('Projects','users-projects-tests')
class UserProjectTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()
        self.project = Project.objects.create(name="test",creator=self.user)
        self.role = Role.objects.create(name="test1", project=self.project)
        self.user_project = UserProject.objects.get(Q(user=self.user) & Q(project=self.project))
        
    @tag('get', 'auth') 
    def test_user_project_list_auth(self):
        response = self.client.get(f"/api/projects/{self.project.id}/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    @tag('get', 'unauth')  
    def test_user_project_list_unauth(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(f"/api/projects/{self.project.id}/users/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    @tag('post', 'auth')
    def test_user_project_create_auth(self):
        response = self.client.post(f"/api/projects/{self.project.id}/users/", data={"user":str(self.new_user.id)})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(f"/api/projects/{self.project.id}/users/", data={"user":str(self.user.id)})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(dict(response.json()),{"Error":"Utente già aggiunto al progetto"})
    
    @tag('post', 'unauth') 
    def test_user_project_create_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.post(f"/api/projects/{self.project.id}/users/", data={"user":str(self.new_user.id)})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    @tag('put', 'auth')
    def test_user_project_update_auth(self):
        data = {"role":[str(self.role.id)]}
        response = self.client.patch(f"/api/projects/users/{self.user_project.id}/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(data, dict(response.json()))
    
    @tag('put', 'unauth')
    def test_user_project_update_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        data = {"role":[str(self.role.id)]}
        response = self.client.patch(f"/api/projects/users/{self.user_project.id}/", data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    @tag('delete', 'auth')
    def test_user_project_delete_auth(self):
        response = self.client.delete(f"/api/projects/users/{self.user_project.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    @tag('delete', 'unauth')
    def test_user_project_delete_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.delete(f"/api/projects/users/{self.user_project.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag('get', 'auth')
    def test_user_project_create_adding_showcase_auth(self):
        response = self.client.post(f"/api/projects/{self.project.id}/users/", data={"user":str(self.new_user.id)})
        general = Showcase.objects.get(project=self.project,name="Generale")
        idea = Showcase.objects.get(project=self.project,name="Idee")
        self.assertListEqual(list(general.users.all()), list(self.project.users.all()))
        self.assertListEqual(list(idea.users.all()), list(self.project.users.all()))