from Core.models import Project, Showcase, Poll, PollOption
from Core.tests import BaseTestCase
from rest_framework import status
from django.test import tag

@tag("Showcases", "polls-tests")
class PollTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()
        self.project = Project.objects.create(name="test", creator=self.user)
        self.showcase = Showcase.objects.get(project=self.project, name="Generale")
        self.poll = Poll.objects.create(author=self.user, showcase=self.showcase, name="test1")
        self.option = PollOption.objects.create(text="test", poll=self.poll)
    
    @tag('post', 'auth')
    def test_poll_create_auth(self):
        data = {"name":"test", "text": "test", "anonymus_voters": True, "options": ["ciao", "cioa2"]}
        response = self.client.post(f"/api/showcase/{self.showcase.id}/messages/poll/", data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(PollOption.objects.filter(poll__id=response.data['id']).count(), 2)
    
    @tag('post', 'unauth')  
    def test_poll_create_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        data = {"name":"test", "text": "test", "anonymus_voters": True, "options": ["ciao", "cioa2"]}
        response = self.client.post(f"/api/showcase/{self.showcase.id}/messages/poll/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
    
    @tag('patch', 'auth')  
    def test_poll_update_auth(self):
        data = {"name":"test"}
        response = self.client.patch(f"/api/poll/{self.poll.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
    
    @tag('patch', 'unauth')
    def test_poll_update_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        data = {"name":"test"}
        response = self.client.patch(f"/api/poll/{self.poll.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.showcase.users.add(self.new_user)
        response = self.client.patch(f"/api/poll/{self.poll.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag('delete', 'auth')
    def test_poll_delete_auth(self):
        response = self.client.delete(f"/api/poll/{self.poll.id}/")
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
    
    @tag('delete', 'unauth')
    def test_poll_delete_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.delete(f"/api/poll/{self.poll.id}/")
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.showcase.users.add(self.new_user)
        response = self.client.delete(f"/api/poll/{self.poll.id}/")
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
    
    @tag('post', 'auth')
    def test_poll_option_create_auth(self):
        data = {"text":"test"}
        response = self.client.post(f"/api/poll/{self.poll.id}/options/", data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
    
    @tag('post', 'unauth')
    def test_poll_option_create_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        data = {"text":"test"}
        response = self.client.post(f"/api/poll/{self.poll.id}/options/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.showcase.users.add(self.new_user)
        response = self.client.post(f"/api/poll/{self.poll.id}/options/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
    
    @tag('patch', 'auth')
    def test_poll_option_update_auth(self):
        data = {"text":"test"}
        response = self.client.patch(f"/api/poll/option/{self.option.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
    
    @tag('patch', 'unauth')
    def test_poll_option_update_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        data = {"text":"test"}
        response = self.client.patch(f"/api/poll/option/{self.option.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.showcase.users.add(self.new_user)
        response = self.client.patch(f"/api/poll/option/{self.option.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag('delete', 'auth')
    def test_poll_option_delete_auth(self):
        response = self.client.delete(f"/api/poll/option/{self.option.id}/")
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
    
    @tag('delete', 'unauth')
    def test_poll_option_delete_unuth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.delete(f"/api/poll/option/{self.option.id}/")
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.showcase.users.add(self.new_user)
        response = self.client.delete(f"/api/poll/option/{self.option.id}/")
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag('post', 'auth')
    def test_poll_option_votes_auth(self):
        response = self.client.post(f"/api/poll/option/{self.option.id}/vote/")
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        self.assertEquals(self.option.votes.filter(id=self.user.id).exists(), True)
        
    @tag('post', 'unauth')
    def test_poll_option_votes_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.post(f"/api/poll/option/{self.option.id}/vote/")
        self.assertEquals(response.status_code,status.HTTP_403_FORBIDDEN)
        
    @tag('post', 'auth') 
    def test_poll_option_double_votes_auth(self):
        option = PollOption.objects.create(poll=self.poll, text="test")
        option.votes.add(self.user)
        response = self.client.post(f"/api/poll/option/{self.option.id}/vote/")
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        self.assertEquals(self.option.votes.filter(id=self.user.id).exists(), True)
        self.assertEquals(option.votes.filter(id=self.user.id).exists(), False)