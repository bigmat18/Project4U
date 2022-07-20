from urllib import response
from Core.tests import BaseTestCase
from rest_framework import status
from Core.models import Project, TextPost
from django.test import tag
import tempfile, PIL
from django.core.files.uploadedfile import SimpleUploadedFile

@tag('Community', 'posts-tests')
class PostTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()
        self.project = Project.objects.create(creator=self.user,name="test")
        self.post = TextPost.objects.create(author=self.user, project=self.project)

    @tag('post', 'auth')
    def test_create_text_post_auth(self):
        response = self.client.post(f'/api/projects/{self.project.id}/text-posts/', data={'text': "test"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @tag('post', 'unauth')
    def test_create_text_post_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.post(f'/api/projects/{self.project.id}/text-posts/', data={'text': "test"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    @tag('post', "auth", "file")
    def test_create_file_text_post_auth(self):
        image = PIL.Image.new('RGB', size=(1, 1))
        file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(file)
        with open(file.name, 'rb') as file_open:
            response = self.client.post(f'/api/projects/{self.project.id}/text-posts/', 
                                       data={"file": file_open, "text": "test"}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    @tag('patch', 'auth')
    def test_update_text_post_auth(self):
        response = self.client.patch(f'/api/text-post/{self.post.id}/', data={'text':"test2"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TextPost.objects.first().text, "test2")

    @tag('post', 'unauth')
    def test_update_text_post_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.patch(f'/api/text-post/{self.post.id}/', data={'text':"test2"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    @tag('delete', 'auth')
    def test_delete_text_post_auth(self):
        response = self.client.delete(f'/api/text-post/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TextPost.objects.all().count(), 0)

    @tag('post', 'unauth')
    def test_delete_text_post_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.delete(f'/api/text-post/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

