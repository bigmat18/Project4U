from .BaseTest import BaseTestCase
from Core.models import UserEducation
from django.utils import timezone
from rest_framework import status

class UserEducationTestCase(BaseTestCase):

    def setUp(self):
        self.init_test(True)
        self.education = UserEducation.objects.create(text="prova",user=self.user,
                                                      started_at=timezone.now())
        
    def test_education_create(self):
        request = self.client.post("/api/user/educations/", data={"text":self.education.text, 
                                                                  "started_at":"20-3-2020"})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        
    def test_education_update(self):
        request = self.client.patch(f"/api/user/educations/{self.education.id}/", data={"text":"prova2"})
        self.assertEqual(request.status_code, status.HTTP_200_OK)
    
    def test_education_delete(self):
        request = self.client.delete(f"/api/user/educations/{self.education.id}/")
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)