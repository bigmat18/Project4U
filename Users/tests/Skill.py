from rest_framework import status
from Core.tests import BaseTestCase
from Core.models import Skill
from django.test import tag


@tag('Users', 'skills-tests')
class SkillTestCase(BaseTestCase):
    
    def setUp(self): self.baseSetup()
            
    @tag('get','auth')
    def test_skill_list_auth(self):
        response = self.client.get("/api/skills/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag('post','unauth')
    def test_skill_create_unauth(self):
         self.client.logout()
         response = self.client.post("/api/skills/", data={"name":"prova"})
         self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    
    @tag('post','auth')
    def test_skill_create_auth(self):
         response = self.client.post("/api/skills/", data={"name":"prova"})
         self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        

@tag('Users', 'user-skills-tests')
class UserSkillTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()
        self.skill1 = Skill.objects.create(name="prova1")
        self.skill2 = Skill.objects.create(name="prova2")
        self.skill3 = Skill.objects.create(name="prova3")
        
    @tag('post','auth')
    def test_user_skill_create_auth(self):
        response = self.client.post(f"/api/user/skills/", data={"level":1, "skill": self.skill1.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(f"/api/user/skills/", format='json', data=[{"level":1, "skill": self.skill2.id},
                                                                        {"level":1, "skill": self.skill3.id}])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, list)
    
    @tag('put','auth')
    def test_user_skill_update_auth(self):
        self.user.skills.add(self.skill1)
        data = {"name": "newName"}
        response = self.client.patch(f"/api/user/skills/{self.skill1.id}/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(data, dict(response.json()))
        
    @tag('delete','auth')
    def test_user_skill_delete_auth(self):
        self.user.skills.add(self.skill1)
        response = self.client.delete(f"/api/user/skills/{self.skill1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)