from Core.models import Project, Showcase, ProjectTag
from Core.tests import BaseTestCase
from rest_framework import status
from django.test import tag
import tempfile, PIL

@tag('Projects', 'projects-tests')
class ProjectsTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()
        self.project = Project.objects.create(name="test", creator=self.user)
        
    @tag('get','auth')  
    def test_projects_list_auth(self):
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    @tag('get','unauth')  
    def test_projects_list_unauth(self):
        self.client.logout()
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    @tag('post','auth')  
    def test_projects_create_auth(self):
        data = {"name": "test1", "tags": ["prova", "prova", "ciao"]}
        response = self.client.post('/api/projects/', data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(ProjectTag.objects.all().count(), 2)
        
    @tag('post','auth')  
    def test_projects_create_showcases_auth(self):
        response = self.client.post('/api/projects/', data={"name": "test1"})
        showcases = Showcase.objects.filter(project=response.data['id'])
        self.assertEqual(showcases.count(), 2)
    
    @tag('put','unauth')  
    def test_projects_update_auth(self):
        data = {"name":"new_name"}
        response = self.client.patch(f'/api/projects/{self.project.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(data, dict(response.json()))
        
        response = self.client.put(f'/api/projects/{self.project.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(data, dict(response.json()))
    
    @tag('put','auth','file')
    def test_projects_update_image_auth(self):
        image = PIL.Image.new('RGB', size=(1, 1))
        file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(file)
        with open(file.name, 'rb') as file_open:
            response = self.client.patch(f'/api/projects/{self.project.id}/', 
                                       data={"image": file_open}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag('put','unauth')  
    def test_projects_update_unauth(self):
        data = {"name":"new_name"}
        self.client.force_authenticate(user=self.new_user)
        response = self.client.patch(f'/api/projects/{self.project.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    @tag('delete','auth')  
    def test_projects_delete_auth(self):
        response = self.client.delete(f'/api/projects/{self.project.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    @tag('delete','unauth')   
    def test_projects_delete_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.delete(f'/api/projects/{self.project.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)