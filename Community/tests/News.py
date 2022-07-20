from Core.tests import BaseTestCase
from rest_framework import status
from Core.models import News, NewsParagraph, Project
from django.test import tag


@tag('Community', 'news-tests')
class NewsTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()
        self.project = Project.objects.create(name="test", creator=self.user)
        self.news = News.objects.create(project=self.project, author=self.user, 
                                        title="test", intro="intro")
        self.paragraph = NewsParagraph.objects.create(news=self.news, title="ciao", content="ciao")
    
    @tag("post", "auth")
    def test_create_news_auth(self):
        data = {"title": "test2", "intro": "test2", "content": "test2"}
        response = self.client.post(f'/api/projects/{self.project.id}/news/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    @tag("post", "unauth")
    def test_create_news_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        data = {"title": "test2", "intro": "test2", "content": "test2"}
        response = self.client.post(f'/api/projects/{self.project.id}/news/', data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag("post", "auth")
    def test_create_news_with_paragraph_auth(self):
        paragraphs = [{"title": "test1", "content": "test1"},{"title": "test2", "content": "test2"}]
        data = {"title": "test2", "intro": "test2", "content": "test2", "paragraphs": paragraphs}
        response = self.client.post(f'/api/projects/{self.project.id}/news/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    @tag("post", "auth")
    def test_create_news_with_paragraph_error_auth(self):
        data = {"title": "test2", "intro": "test2", "content": "test2", "paragraphs": "ciao"}
        response = self.client.post(f'/api/projects/{self.project.id}/news/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data = {"title": "test2", "intro": "test2", "content": "test2", "paragraphs": [{"errore":"errore"}]}
        response = self.client.post(f'/api/projects/{self.project.id}/news/', data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    @tag("get", "auth")
    def test_retrive_news_auth(self):
        response = self.client.get(f'/api/news/{self.news.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("delete", "auth")
    def test_delete_news_auth(self):
        response = self.client.delete(f'/api/news/{self.news.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(News.objects.all().count(),0)
        
    @tag("delete", "unauth")
    def test_delete_news_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.delete(f'/api/news/{self.news.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag("patch", "auth")
    def test_update_news_auth(self):
        response = self.client.patch(f'/api/news/{self.news.id}/', data={"title": "titolo1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "titolo1")
        
    @tag("patch", "unauth")
    def test_update_news_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.patch(f'/api/news/{self.news.id}/', data={"title": "titolo1"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)