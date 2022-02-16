from django.utils import timezone
from Core.tests import BaseTestCase
from rest_framework import status
from Core.models import Project, Showcase, Event, EventTask
from django.test import tag
import datetime

@tag("Showcase", "events-tests")
class EventTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()
        self.project = Project.objects.create(name="test", creator=self.user)
        self.showcase = Showcase.objects.get(project=self.project, name="Generale")
        self.event = Event.objects.create(started_at=timezone.now(),ended_at=timezone.now() + datetime.timedelta(days=1),
                                          author=self.user,type_message="EVENT",showcase=self.showcase)
        self.task = EventTask.objects.create(event=self.event, name="test0")
      
    @tag("post", "auth")  
    def test_event_create_auth(self):
        data = {"started_at": timezone.now(), "ended_at": timezone.now() + datetime.timedelta(days=1), "partecipants": [str(self.new_user.id)]}
        response = self.client.post(f"/api/showcase/{self.showcase.id}/messages/event/", data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(len(response.data["partecipants"]), 2)
        
    @tag("post", "unauth")  
    def test_event_create_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        data = {"started_at": timezone.now(), "ended_at": timezone.now() + datetime.timedelta(days=1), "partecipants": [str(self.new_user.id)]}
        response = self.client.post(f"/api/showcase/{self.showcase.id}/messages/event/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
    
    @tag("post", "auth")  
    def test_event_task_create_auth(self):
        data = {"name": "test"}
        response = self.client.post(f"/api/event/{self.event.id}/tasks/", data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        
        data = [{"name": "test"}, {"name": "test2"}]
        response = self.client.post(f"/api/event/{self.event.id}/tasks/", format="json",data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        
    @tag("post", "unauth")  
    def test_event_task_create_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        self.event.partecipants.add(self.new_user)
        data = {"name": "test"}
        response = self.client.post(f"/api/event/{self.event.id}/tasks/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        
    
    @tag("patch", "auth")  
    def test_event_update_auth(self):
        data = {"partecipants": [str(self.new_user.id)]}
        response = self.client.patch(f"/api/event/{self.event.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data["partecipants"]), 1)
        
    @tag("patch", "unauth")  
    def test_event_update_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        data = {"partecipants": [str(self.new_user.id)]}
        response = self.client.patch(f"/api/event/{self.event.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
    
    @tag("patch", "auth")  
    def test_event_task_update_auth(self):
        data = {"name": "test2"}
        response = self.client.patch(f"/api/event/task/{self.task.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        
        self.client.force_authenticate(user=self.new_user)
        self.event.partecipants.add(self.new_user)
        response = self.client.patch(f"/api/event/task/{self.task.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        
    @tag("patch", "unauth")  
    def test_event_task_update_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        data = {"name": "test2"}
        response = self.client.patch(f"/api/event/task/{self.task.id}/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
    
    @tag("delete", "auth")  
    def test_event_delete_auth(self):
        response = self.client.delete(f"/api/event/{self.event.id}/")
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        
    @tag("delete", "unauth")  
    def test_event_delete_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.delete(f"/api/event/{self.event.id}/")
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
    
    @tag("delete", "auth")  
    def test_event_task_delete_auth(self):
        response = self.client.delete(f"/api/event/task/{self.task}/")
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    @tag("delete", "unauth")  
    def test_event_task_delete_unauth(self):
        self.client.force_authenticate(user=self.new_user)
        self.event.partecipants.add(self.new_user)
        response = self.client.delete(f"/api/event/task/{self.task}/")
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
    
    @tag('post', "auth")  
    def test_event_task_create_in_event_auth(self):
        data = {"started_at": timezone.now(), "ended_at": timezone.now() + datetime.timedelta(days=1), "partecipants": [str(self.new_user.id)],
                "tasks": ["prova1", "prova2"]}
        response = self.client.post(f"/api/showcase/{self.showcase.id}/messages/event/", data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(EventTask.objects.all().count(),3)
