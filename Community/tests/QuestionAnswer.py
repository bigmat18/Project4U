from Core.tests import BaseTestCase
from rest_framework import status
from django.test import tag
from django.core.files.uploadedfile import SimpleUploadedFile
from Core.models import Project, ProjectAnswer, ProjectQuestion

@tag('Community', 'question-tests')
class QuestionTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()
        self.project = Project.objects.create(creator=self.user, name="test")
        self.question = ProjectQuestion.objects.create(author=self.user, content="test", project=self.project)
        
    def test_create_question_auth(self):
        response = self.client.post(f"/api/projects/{self.project.id}/questions/", data={"content": "test"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_question_auth(self):
        response = self.client.patch(f"/api/project/question/{self.question.slug}/", data={"content": "new test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], "new test")

    def test_update_question_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.patch(f"/api/project/question/{self.question.slug}/", data={"content": "new test"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_question_auth(self):
        response = self.client.delete(f"/api/project/question/{self.question.slug}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_delete_question_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.delete(f"/api/project/question/{self.question.slug}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    
    
@tag('Community', 'question-tests')
class AnswerTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()
        self.project = Project.objects.create(creator=self.user, name="test")
        self.question = ProjectQuestion.objects.create(project=self.project,content="test",author=self.user)
        
    def test_create_answer_auth(self):
        pass
    
    def test_create_answer_unauth(self):
        pass
    
    def test_update_answer_auth(self):
        pass

    def test_update_answer_unauth(self):
        pass
    
    def test_delete_answer_auth(self):
        pass
    
    def test_delete_answer_unauth(self):
        pass