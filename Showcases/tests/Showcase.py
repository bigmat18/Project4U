from Core.tests import BaseTestCase
from rest_framework import status
from Core.models import Project, User, Showcase
from django.test import tag

@tag('Showcases', 'showcase-tests')
class ShowcaseTestCase(BaseTestCase):
    
    def setUp(self):
        self.init_test(True)
        self.project = Project.objects.create(name="test", 
                                              creator=self.user)
        self.showcase = Showcase.objects.create(name="test",
                                                project=self.project)
        self.new_user = User.objects.create_user(email=f"2{self.email}", password=self.email,
                                            first_name=self.first_name, last_name=self.last_name)
        
    @tag('get','auth') 
    def test_showcase_list_auth(self):
        response = self.client.get(f'/api/projects/{self.project.id}/showcases/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    @tag('get','unauth') 
    def test_showcase_list_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.get(f'/api/projects/{self.project.id}/showcases/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    @tag('post','auth')
    def test_showcase_create_auth(self):
        data = {'name':'test', "users": [str(self.new_user.id)]}
        response = self.client.post(f'/api/projects/{self.project.id}/showcases/',data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['users'][0]['slug'], self.user.slug)
        
    @tag('post','unauth') 
    def test_showcase_create_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        data = {'name':'test'}
        response = self.client.post(f'/api/projects/{self.project.id}/showcases/',data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)