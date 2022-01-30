from time import time
from Core.tests import BaseTestCase
from rest_framework import status
from Core.models import Project, TextMessage, Event
from django.test import tag
from django.utils import timezone

@tag('Showcases', 'showcase-tests')
class ShowcaseTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()
        self.project = Project.objects.create(name="test", 
                                              creator=self.user)
        
    @tag('get','auth') 
    def test_showcase_list_auth(self):
        response = self.client.get(f'/api/projects/{self.project.id}/showcases/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    @tag('get', 'auth')
    def test_showcase_list_last_message(self):
        showcase = self.project.showcases.all()[0]
        message = TextMessage.objects.create(text="test", author=self.user,
                                            showcase=showcase)
        Event.objects.create(author=self.user, date=timezone.now(),
                             showcase=showcase)
        response = self.client.get(f'/api/projects/{self.project.id}/showcases/')
        self.assertEqual(list(response.data)[0]['last_message']['id'], str(message.id))
        
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
        self.assertEqual(response.data['users'][0]['secret_key'], self.user.secret_key)
        
    @tag('post','unauth') 
    def test_showcase_create_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        data = {'name':'test'}
        response = self.client.post(f'/api/projects/{self.project.id}/showcases/',data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

