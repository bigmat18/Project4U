from Core.tests import BaseTestCase
from rest_framework import status
from Core.models import Project, TextPost, PostComment
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


@tag('Community', 'posts-comments-tests')
class PostCommentTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()
        self.project = Project.objects.create(creator=self.user,name="test")
        self.post = TextPost.objects.create(author=self.user, project=self.project)
        self.comment = PostComment.objects.create(author=self.user, post=self.post, text="test")
        
    @tag('get', 'auth')
    def test_list_post_comment_auth(self):
        response = self.client.get(f"/api/post/{self.post.id}/comments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    @tag('post', 'auth')
    def test_create_post_comment_auth(self):
        response = self.client.post(f"/api/post/{self.post.id}/comments/", data={"text": "test"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    @tag('delete', 'auth')
    def test_delete_post_comment_auth(self):
        response = self.client.delete(f"/api/post/comment/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    @tag('delete', 'unauth')
    def test_delete_post_comment_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.delete(f"/api/post/comment/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    @tag('patch', 'auth')
    def test_update_post_comment_auth(self):
        response = self.client.patch(f"/api/post/comment/{self.comment.id}/", data={"text": "new test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    @tag('patch', 'unauth')
    def test_update_post_comment_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.patch(f"/api/post/comment/{self.comment.id}/", data={"text": "new test"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    @tag('post', 'auth')
    def test_post_comment_like_auth(self):
        response = self.client.post(f"/api/post/comment/{self.comment.id}/likes/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['msg'], "Like inserito")
        
        response = self.client.post(f"/api/post/comment/{self.comment.id}/likes/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['msg'], "Like già inserito")
        
    @tag('delete', 'auth')
    def test_post_comment_unlike_auth(self):
        self.comment.likes.add(self.user)
        self.comment.save()
        response = self.client.delete(f"/api/post/comment/{self.comment.id}/likes/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['msg'], "Like eliminato")
        
        response = self.client.delete(f"/api/post/comment/{self.comment.id}/likes/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['msg'], "Like non inserito")