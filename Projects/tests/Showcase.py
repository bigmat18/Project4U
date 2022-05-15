from Core.models.Projects.Showcase import Showcase
from Core.models.Projects.ShowcaseUpdate import ShowcaseUpdate
from Core.tests import BaseTestCase
from rest_framework import status
from Core.models import Project, TextMessage, Event
from django.test import tag
from django.utils import timezone
import datetime

@tag('Showcases', 'showcase-tests')
class ShowcaseTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()
        self.project = Project.objects.create(name="test", 
                                              creator=self.user)
        self.project.users.add(self.new_user)
        self.project.save()
        self.showcase = Showcase.objects.get(project=self.project,name="Generale")

    @tag('get','auth') 
    def test_showcase_list_auth(self):
        response = self.client.get(f'/api/projects/{self.project.id}/showcases/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=self.new_user)
        response = self.client.get(f'/api/projects/{self.project.id}/showcases/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    @tag('get', 'auth')
    def test_showcase_last_message_auth(self):
        showcase = self.project.showcases.all()[0]
        message = TextMessage.objects.create(text="test", author=self.user,
                                            showcase=showcase)
        Event.objects.create(author=self.user,started_at=timezone.now(),
                             ended_at=timezone.now() + datetime.timedelta(days=1),
                             showcase=showcase,type_message="EVENT")
        response = self.client.get(f'/api/showcase/{showcase.id}/last-message/')
        self.assertEqual(dict(response.data)['id'], str(message.id))
        
    @tag('get', 'auth')
    def test_showcase_last_event_auth(self):
        showcase = self.project.showcases.all()[0]
        TextMessage.objects.create(text="test", author=self.user,
                                            showcase=showcase)
        event = Event.objects.create(author=self.user,started_at=timezone.now(),
                             ended_at=timezone.now() + datetime.timedelta(days=1),
                             showcase=showcase,type_message="EVENT")
        response = self.client.get(f'/api/showcase/{showcase.id}/last-event/')
        self.assertEqual(dict(response.data)['id'], str(event.id))
        
    @tag('get', 'auth')
    def test_showcase_users_auth(self):
        response = self.client.get(f'/api/showcase/{self.showcase.id}/users/')
        self.assertEqual(len(dict(response.data)['users']), 1)
        
    @tag('get','unauth') 
    def test_showcase_list_unauth(self):
        self.project.users.remove(self.new_user)
        self.client.force_authenticate(user=self.new_user)
        response = self.client.get(f'/api/projects/{self.project.id}/showcases/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    @tag('post','auth')
    def test_showcase_create_auth(self):
        data = {'name':'test', "users": [str(self.new_user.id)]}
        response = self.client.post(f'/api/projects/{self.project.id}/showcases/',data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['users_list']), 2)
        self.client.force_authenticate(user=self.new_user)
        response = self.client.post(f'/api/projects/{self.project.id}/showcases/',data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['users_list']), 1)
        
    @tag('post','auth')
    def test_showcase_create_no_user_project_auth(self):
        data = {'name':'test', "users": [str(self.new_user.id)]}
        self.project.users.remove(self.new_user)
        response = self.client.post(f'/api/projects/{self.project.id}/showcases/',data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag('post','unauth','this') 
    def test_showcase_create_unauth(self):
        self.project.users.remove(self.new_user)
        self.client.force_authenticate(user=self.new_user)
        data = {'name':'test'}
        response = self.client.post(f'/api/projects/{self.project.id}/showcases/',data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
      
    @tag('get', 'auth')  
    def test_showcase_notify_auth(self):
        self.showcase.users.add(self.new_user), 
        self.showcase.save()
        TextMessage.objects.create(text='test',showcase=self.showcase,author=self.new_user)
        response = self.client.get(f'/api/showcase/{self.showcase.id}/notify/')
        self.assertEqual(dict(response.data)["notify"], 1)
        
        self.client.get(f'/api/showcase/{self.showcase.id}/messages/')
        response = self.client.get(f'/api/showcase/{self.showcase.id}/notify/')
        self.assertEqual(dict(response.data)["notify"], 0)
        
    @tag('patch', 'auth') 
    def test_showcase_update_auth(self):
        data = {"description":"test"}
        response = self.client.patch(f"/api/showcase/{self.showcase.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(ShowcaseUpdate.objects.all().count(), 1)
        
    @tag('patch','auth')
    def test_showcase_update_no_user_project_auth(self):
        data = {'name':'test', "users": [str(self.new_user.id)]}
        self.project.users.remove(self.new_user)
        response = self.client.patch(f"/api/showcase/{self.showcase.id}/",data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    @tag('patch', 'unauth') 
    def test_showcase_update_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        data = {"description":"test"}
        response = self.client.patch(f"/api/showcase/{self.showcase.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.showcase.users.add(self.new_user)
        self.showcase.save()
        response = self.client.patch(f"/api/showcase/{self.showcase.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
    
    @tag('delete', 'auth') 
    def test_showcase_delete_auth(self):
        response = self.client.delete(f"/api/showcase/{self.showcase.id}/")
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
    
    @tag('delete', 'unauth') 
    def test_showcase_delete_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.delete(f"/api/showcase/{self.showcase.id}/")
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.showcase.users.add(self.new_user)
        self.showcase.save()
        response = self.client.delete(f"/api/showcase/{self.showcase.id}/")
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        
    @tag('get', 'auth')   
    def test_showcase_list_not_inside_auth(self):
        Showcase.objects.create(project=self.project, creator=self.new_user, name="test")
        response = self.client.get(f'/api/projects/{self.project.id}/showcases/')
        self.assertEquals(len(response.data), 2)