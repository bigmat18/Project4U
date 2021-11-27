from rest_framework import status
from .BaseTest import BaseTestCase
from Core.models import Skill


class SkillTestCase(BaseTestCase):
    
    def setUp(self): self.init_test(True)
            
    def test_list_skill(self):
        response = self.client.get("/api/skills/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_skill_unauth(self):
         self.client.logout()
         response = self.client.post("/api/skills/", data={"name":"prova"})
         self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
         
    def test_create_skill_auth(self):
         response = self.client.post("/api/skills/", data={"name":"prova"})
         self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        
        
class UserSkillTestCase(BaseTestCase):
    
    def setUp(self):
        self.init_test(True)
        self.skill = Skill.objects.create(name="prova")
        self.skill2 = Skill.objects.create(name="prova2")
        
    def test_user_skill_list_create(self):
        response = self.client.post(f"/api/user/skills/", format='json', data=[{"level":1, "skill": self.skill.id},
                                                                        {"level":1, "skill": self.skill2.id}])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_user_skill_create(self):
        response = self.client.post(f"/api/user/skills/", data={"level":1, "skill": self.skill.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_user_skill_update(self):
        self.user.skills.add(self.skill)
        response = self.client.patch(f"/api/user/skills/{self.skill.id}/", data={"level": 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_user_skill_delete(self):
        self.user.skills.add(self.skill)
        response = self.client.delete(f"/api/user/skills/{self.skill.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)