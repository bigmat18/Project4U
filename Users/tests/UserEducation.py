from Core.tests import BaseTestCase
from Core.models import UserEducation
from django.utils import timezone
from rest_framework import status
from django.test import tag

@tag('Users', 'user-educations-tests')
class UserEducationTestCase(BaseTestCase):

    def setUp(self):
        self.init_test(True)
        self.education = UserEducation.objects.create(text="prova",user=self.user,
                                                      started_at=timezone.now())
    @tag('post')
    def test_education_create_auth(self):
        response = self.client.post("/api/user/educations/", data={"text":self.education.text, 
                                                                  "started_at":"2020-3-20"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post("/api/user/educations/", format= "json", data=[
            {"text":self.education.text,"started_at":"2020-3-20"},
            {"text":self.education.text,"started_at":"2020-3-20"}])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, list)
    
    @tag('put')
    def test_education_update_auth(self):
        data = {"text":"prova2"}
        response = self.client.patch(f"/api/user/educations/{self.education.id}/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(data, dict(response.json()))
    
    @tag('delete')
    def test_education_delete_auth(self):
        response = self.client.delete(f"/api/user/educations/{self.education.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)