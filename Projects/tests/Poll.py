from Core.models import Project, Showcase, Poll, PollOption
from Core.tests import BaseTestCase
from rest_framework import status
from django.test import tag

@tag("this")
class PollTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()
        self.project = Project.objects.create(name="test", creator=self.user)
        self.showcase = Showcase.objects.get(project=self.project, name="Generale")
        self.poll = Poll.objects.create(author=self.user, showcase=self.showcase, name="test1")
        self.option = PollOption.objects.create(text="test", poll=self.poll)
    
    def test_poll_create_auth(self):
        data = {"name":"test", "text": "test", "anonymus_voters": True, "options": ["ciao", "cioa2"]}
        response = self.client.post(f"/api/showcase/{self.showcase.id}/messages/poll/", data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(PollOption.objects.filter(poll__id=response.data['id']).count(), 2)
        
    def test_poll_create_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        data = {"name":"test", "text": "test", "anonymus_voters": True, "options": ["ciao", "cioa2"]}
        response = self.client.post(f"/api/showcase/{self.showcase.id}/messages/poll/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_poll_update_auth(self):
        data = {"name":"test"}
        response = self.client.patch(f"/api/poll/{self.poll.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
                
    def test_poll_update_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        data = {"name":"test"}
        response = self.client.patch(f"/api/poll/{self.poll.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.showcase.users.add(self.new_user)
        response = self.client.patch(f"/api/poll/{self.poll.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_poll_delete_auth(self):
        response = self.client.delete(f"/api/poll/{self.poll.id}/")
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_poll_delete_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.delete(f"/api/poll/{self.poll.id}/")
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.showcase.users.add(self.new_user)
        response = self.client.delete(f"/api/poll/{self.poll.id}/")
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_poll_option_create_auth(self):
        data = {"text":"test"}
        response = self.client.post(f"/api/poll/{self.poll.id}/options/", data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        
    def test_poll_option_create_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        data = {"text":"test"}
        response = self.client.post(f"/api/poll/{self.poll.id}/options/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.showcase.users.add(self.new_user)
        response = self.client.post(f"/api/poll/{self.poll.id}/options/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_poll_option_update_auth(self):
        data = {"text":"test"}
        response = self.client.patch(f"/api/poll/option/{self.option.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        
    def test_poll_option_update_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        data = {"text":"test"}
        response = self.client.patch(f"/api/poll/option/{self.option.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.showcase.users.add(self.new_user)
        response = self.client.patch(f"/api/poll/option/{self.option.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_poll_option_delete_auth(self):
        response = self.client.delete(f"/api/poll/option/{self.option.id}/")
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_poll_option_delete_unuth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.delete(f"/api/poll/option/{self.option.id}/")
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.showcase.users.add(self.new_user)
        response = self.client.delete(f"/api/poll/option/{self.option.id}/")
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
