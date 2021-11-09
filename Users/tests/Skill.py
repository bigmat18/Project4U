from django.http import response
from rest_framework import status
from rest_framework.test import APITestCase
from Core.models import Skill,User
from rest_framework_api_key.models import APIKey


class SkillTestCase(APITestCase):
    first_name = "prova"
    last_name = "prova"
    email_user = "prova@prova.com"
    password = "prova1234567_"
    
    def setUp(self):
        self.user = User.objects.create_user(password=self.password,email=self.email_user,
                                             first_name=self.first_name,last_name=self.last_name)
        key = APIKey.objects.create_key(name="prova")
        self.client.credentials(HTTP_X_API_KEY=key[1])

            
    def test_list_skill(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/skills/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
class UserSkillTestCase(APITestCase):
    first_name = "prova"
    last_name = "prova"
    email_user = "prova@prova.com"
    password = "prova1234567_"
    
    def setUp(self):
        self.user = User.objects.create_user(password=self.password,email=self.email_user,
                                             first_name=self.first_name,last_name=self.last_name)
        key = APIKey.objects.create_key(name="prova")
        self.skill = Skill.objects.create(name="prova1")
        self.client.credentials(HTTP_X_API_KEY=key[1])
        
    def test_user_skill_create(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f"/api/users/{self.user.slug}/skills/", data={"level":1, "skill": self.skill.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)