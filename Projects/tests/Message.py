from Core.tests import BaseTestCase
from rest_framework import status
from Core.models import Project, Showcase, TextMessage, MessageFile
from django.test import tag
from django.core.files.uploadedfile import SimpleUploadedFile

@tag('Showcases', 'messages-tests')
class MessageTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()
        self.project = Project.objects.create(name='test',creator=self.user)
        self.showcase = Showcase.objects.create(name='test',project=self.project,creator=self.user)
        self.text_message = TextMessage.objects.create(text='test',showcase=self.showcase,author=self.user)
    
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
    
    @tag('post','auth','file') 
    def test_message_file_create_auth(self):
        file = SimpleUploadedFile("file.txt", b"abc", content_type="text/plain")
        data = {"file": file}
        response = self.client.post(f'/api/text/{self.text_message.id}/files/', data=data, format="multipart")
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    @tag('post','auth','file') 
    def test_message_file_create_list_auth(self):
        file1 = SimpleUploadedFile("file.txt", b"abc", content_type="text/plain")
        file2 = SimpleUploadedFile("file.txt", b"abc", content_type="text/plain")
        data = {"file": [file1, file2]}
        response = self.client.post(f'/api/text/{self.text_message.id}/files/', data=data, format="multipart")
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(MessageFile.objects.all().count(), 2)

    @tag('get', 'auth')
    def test_message_list_filter_gt_updated_at_auth(self):
        message = TextMessage.objects.create(text='test2',showcase=self.showcase,author=self.user)
        date = message.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        response = self.client.get(f'/api/showcase/{self.showcase.id}/messages/?gt_updated_at={date}')
        self.assertEquals(len(list(response.data['results'])), 0)