from urllib import response
from Core.tests import BaseTestCase
from rest_framework import status
from Core.models import News, NewsParagraph, Project
from django.test import tag
from django.core.files.uploadedfile import SimpleUploadedFile


@tag('Community', 'news-tests')
class NewsTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()
        self.project = Project.objects.create(name="test", creator=self.new_user)
        self.news = News.objects.create(project=self.project, author=self.new_user, 
                                        title="test", intro="intro")
        self.paragraph = NewsParagraph.objects.create(news=self.news, title="ciao", content="ciao")
        
    def test_create_news_auth(self):
        data = {"title": "test2", "intro": "test2", "content": "test2"}
        response = self.client.post(f'/api/projects/{self.project.id}/news/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_news_with_paragraph_auth(self):
        paragraphs = [{"title": "test1", "content": "test1"},{"title": "test2", "content": "test2"}]
        data = {"title": "test2", "intro": "test2", "content": "test2", "paragraphs": paragraphs}
        response = self.client.post(f'/api/projects/{self.project.id}/news/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_news_with_paragraph_error_auth(self):
        data = {"title": "test2", "intro": "test2", "content": "test2", "paragraphs": "ciao"}
        response = self.client.post(f'/api/projects/{self.project.id}/news/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data = {"title": "test2", "intro": "test2", "content": "test2", "paragraphs": [{"errore":"errore"}]}
        response = self.client.post(f'/api/projects/{self.project.id}/news/', data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_retrive_news_auth(self):
        response = self.client.get(f'/api/news/{self.news.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete_news_auth(self):
        response = self.client.delete(f'/api/news/{self.news.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(News.objects.all().count(),0)
        
    def test_update_news_auth(self):
        response = self.client.patch(f'/api/news/{self.news.id}/', data={"title": "titolo1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "titolo1")
        
    def test_list_paragraph_auth(self):
        response = self.client.get(f'/api/news/{self.news.id}/paragraphs/',)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list(response.data)), 1)
        
    def test_list_paragraph_auth(self):
        data = {"title": "test1", "content": "test1"}
        response = self.client.post(f'/api/news/{self.news.id}/paragraphs/',data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NewsParagraph.objects.all().count(), 2)
        
    def test_update_paragraph_auth(self):
        response = self.client.patch(f'/api/paragraph/{self.paragraph.id}/', data={"title": "titolo1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "titolo1")
        
    def test_delete_paragraph_auth(self):
        response = self.client.delete(f'/api/paragraph/{self.paragraph.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(NewsParagraph.objects.all().count(),0)
        