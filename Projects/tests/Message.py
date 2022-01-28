from Core.tests import BaseTestCase
from rest_framework import status
from Core.models import Project, Showcase, Event, TextMessage
from django.test import tag

@tag('Showcases', 'messages-tests')
class MessageTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()
        self.project = Project.objects.create(name='test',creator=self.user)
        self.showcase = Showcase.objects.create(name='test',project=self.project,creator=self.user)
    
    @tag('get','auth')
    def test_message_list_auth(self):
        response = self.client.get(f'/api/showcase/{self.showcase.id}/messages/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    @tag('get','unauth')
    def test_message_list_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.get(f'/api/showcase/{self.showcase.id}/messages/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    @tag('post','auth')   
    def test_text_message_create_auth(self):
        data = {"text":"text"}
        response = self.client.post(f'/api/showcase/{self.showcase.id}/messages/text/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @tag('post','unauth')   
    def test_text_message_create_unauth(self):
        data = {"text":"text"}
        self.client.force_authenticate(user=self.new_user)
        response = self.client.post(f'/api/showcase/{self.showcase.id}/messages/text/', data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    @tag('get','auth')  
    def test_message_pagination_empty_auth(self):
        response = self.client.get(f'/api/showcase/{self.showcase.id}/messages/?page=2')
        self.assertEqual(str(response.data['detail']), "Pagina non valida.")
        
    @tag('get','auth') 
    def test_message_pagination_limit_auth(self):
        TextMessage.objects.create(text='test',showcase=self.showcase,author=self.user)
        TextMessage.objects.create(text='test',showcase=self.showcase,author=self.user)
        response = self.client.get(f'/api/showcase/{self.showcase.id}/messages/?size=1')
        self.assertIsNone(response.data['previous'])
        self.assertIsNotNone(response.data['next'])