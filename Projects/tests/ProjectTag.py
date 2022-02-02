from Core.models import Project, ProjectTag
from Core.tests import BaseTestCase
from rest_framework import status
from django.test import client, tag


@tag("Projects", "projects-tags-tests")
class ProjectTagTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()
        self.project = Project.objects.create(name="test",creator=self.user)
        self.tag = ProjectTag.objects.create(name="test1")
        
        
    def test_tags_list_create_auth(self):
        data = [{'name':"test1"},{"name":"test2"}]
        response = self.client.post(f'/api/projects/{self.project.id}/tags/',data=data,format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(self.project.tags.count(),2)
        self.assertEquals(ProjectTag.objects.all().count(),2)
        
    def test_tags_single_create_auth(self):
        data = {'name':"test2"}
        response = self.client.post(f'/api/projects/{self.project.id}/tags/', data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(self.project.tags.count(),1)
        self.assertEquals(ProjectTag.objects.all().count(),2)