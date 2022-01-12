from Core.models.Showcases.Showcase import Showcase
from Core.tests import BaseTestCase
from rest_framework import status
from Core.models import Project
from django.test import tag

@tag('Showcases', 'showcase-tests')
class ShowcaseTestCase(BaseTestCase):
    
    def setUp(self):
        self.init_test(True)
        self.project = Project.objects.create(name="test", 
                                              creator=self.user)
        self.showcase = Showcase.objects.create(name="test",
                                                project=self.project)
        
    @tag('get','auth') 
    def test_showcase_list_auth(self):
        response = self.client.get(f'/api/projects/{self.project.id}/showcases/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    @tag('post','auth')
    def test_showcase_create_auth(self):
        data = {'name':'test'}
        response = self.client.post(f'/api/projects/{self.project.id}/showcases/',data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['users'][0]['slug'], self.user.slug)