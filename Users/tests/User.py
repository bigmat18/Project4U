from rest_framework import status
from Core.tests import BaseTestCase
from Core.models import Project, Skill, UserSkill
from django.test import tag
import PIL, tempfile

@tag('Users', 'users-tests')
class UserTestCase(BaseTestCase):
    
    def setUp(self): self.baseSetup()
        
    @tag('put','auth')
    def test_current_user_update_auth(self):
        data = {"description": "sdad"}
        response = self.client.put("/api/user/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(data, dict(response.json()))
        
        response = self.client.patch("/api/user/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(data, dict(response.json()))
        
    @tag('put','auth','file')
    def test_current_user_update_image_auth(self):
        image = PIL.Image.new('RGB', size=(1, 1))
        file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(file)
        with open(file.name, 'rb') as file_open:
            response = self.client.patch("/api/user/", data={"image": file_open}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag('put','unauth') 
    def test_current_user_update_unauth(self):
        self.client.logout()
        response = self.client.put("/api/user/", {"description": "sdad"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    @tag('get','auth','file')
    def test_current_user_image_auth(self):
        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.user.image = image
        response = self.client.get('/api/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["image"], f"http://testserver/media{image}")
    
    @tag('get','auth')
    def test_users_list_auth(self):
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag('get','auth')
    def test_users_list_auth(self):
        skill1 = Skill.objects.create(name="test1")
        UserSkill.objects.create(user=self.user, skill=skill1, level=2)
        
        skill2 = Skill.objects.create(name="test2")
        UserSkill.objects.create(user=self.user, skill=skill2, level=4)
        
        skill3 = Skill.objects.create(name="test3")
        UserSkill.objects.create(user=self.user, skill=skill3, level=1)
        
        skill4 = Skill.objects.create(name="test4")
        UserSkill.objects.create(user=self.user, skill=skill4, level=1)
        
        response = self.client.get("/api/users/")
        self.assertEqual(len(list(response.data)[0]['skills']), 3)
        
    @tag('get','auth')
    def test_users_detail_auth(self):
        response = self.client.get(f"/api/users/{self.user.slug}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)    
        
    @tag('get','auth')  
    def test_user_image_auth(self):
        response = self.client.get('/api/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    @tag('get', 'auth')  
    def test_user_projects_auth(self):
        project = Project.objects.create(name='test', creator=self.new_user)
        project.users.add(self.user)
        response = self.client.get('/api/user/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data)[0]['name'],project.name)
    
    @tag('get', 'auth') 
    def test_user_info_auth(self):
        response = self.client.get('/api/user/info/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data)['id'], str(self.user.id))
    
    @tag('get', 'auth')
    def test_user_filter(self):
        skill1 = Skill.objects.create(name="test1")
        UserSkill.objects.create(user=self.user, skill=skill1, level=2)
        
        skill2 = Skill.objects.create(name="test2")
        UserSkill.objects.create(user=self.user, skill=skill2, level=4)
        
        skill3 = Skill.objects.create(name="test3")
        UserSkill.objects.create(user=self.user, skill=skill3, level=1)
        
        response = self.client.get(f'/api/users/?skills={skill1.id},1,3')
        self.assertEquals(len(list(response.data)),1)
        
        response = self.client.get(f'/api/users/?skills={skill1.id},1,3&skills={skill2.id},1,2')
        self.assertEquals(len(list(response.data)),0)
        
        response = self.client.get(f'/api/users/?skills={skill1.id},1,3&skills={skill2.id},2,5')
        self.assertEquals(len(list(response.data)),1)