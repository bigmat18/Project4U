from Core.tests import BaseTestCase
from rest_framework import status
from Core.models import News, NewsParagraph, Project, NewsParagraphImage
from django.test import tag
import tempfile, PIL
from django.test.utils import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile


@tag('Community', 'news-paragraph-tests', 'file')
class NewsParagraphTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()
        self.project = Project.objects.create(name="test", creator=self.user)
        self.news = News.objects.create(project=self.project, author=self.user, 
                                        title="test", intro="intro")
        self.paragraph = NewsParagraph.objects.create(news=self.news, title="ciao", content="ciao")
        image = SimpleUploadedFile("test.jpg", b"")
        self.image = NewsParagraphImage.objects.create(image=image, caption="test", paragraph=self.paragraph)
            
    @tag("get", "auth")
    def test_list_paragraph_auth(self):
        response = self.client.get(f'/api/news/{self.news.id}/paragraphs/',)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list(response.data)), 1)

    @tag("post", "auth")
    def test_create_paragraph_auth(self):
        data = {"title": "test1", "content": "test1"}
        response = self.client.post(f'/api/news/{self.news.id}/paragraphs/',data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NewsParagraph.objects.all().count(), 2)

    @tag("post", "unauth")
    def test_create_paragraph_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        data = {"title": "test1", "content": "test1"}
        response = self.client.post(f'/api/news/{self.news.id}/paragraphs/',data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag("patch", "auth")
    def test_update_paragraph_auth(self):
        response = self.client.patch(f'/api/paragraph/{self.paragraph.id}/', data={"title": "titolo1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "titolo1")

    @tag("patch", "unauth")
    def test_update_paragraph_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.patch(f'/api/paragraph/{self.paragraph.id}/', data={"title": "titolo1"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag("delete", "auth")
    def test_delete_paragraph_auth(self):
        response = self.client.delete(f'/api/paragraph/{self.paragraph.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(NewsParagraph.objects.all().count(),0)

    @tag("delete", "auth")
    def test_delete_paragraph_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.delete(f'/api/paragraph/{self.paragraph.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    @tag("post", "auth")
    def test_create_paragraph_image_auth(self):
        image = PIL.Image.new('RGB', size=(1, 1))
        file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(file)
        with open(file.name, 'rb') as file_open:
            response = self.client.post(f'/api/paragraph/{self.paragraph.id}/image/', 
                                       data={"image": file_open, "caption": "test"}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @tag("post", "unauth")
    def test_create_paragraph_image_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.post(f'/api/paragraph/{self.paragraph.id}/image/', data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag("patch", "auth")
    def test_update_paragraph_image_auth(self):
        response = self.client.patch(f"/api/paragraph-image/{self.image.id}/", data={"caption": "test2"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("patch", "unauth")
    def test_update_paragraph_image_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.patch(f"/api/paragraph-image/{self.image.id}/", data={"caption": "test2"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    @tag("delete", "auth")
    @override_settings(DEBUG=True)
    def test_delete_paragraph_image_auth(self):
        response = self.client.delete(f"/api/paragraph-image/{self.image.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    @tag("delete", "unauth")
    def test_delete_paragraph_image_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.delete(f"/api/paragraph-image/{self.image.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
