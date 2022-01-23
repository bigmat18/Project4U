from unicodedata import name
from Core.models import Project, ProjectTag
from Core.tests import BaseTestCase
from rest_framework import status
from django.test import client, tag


@tag("Projects", "projects-tags-tests")
class ProjectTagTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()
        self.project = Project.objects.create(name="test",creator=self.user)
        self.tag = ProjectTag.objects.create(name="test")
        
    @tag('get','auth')
    def test_projects_tags_list_auth(self):
        response = self.client.get("/api/projects-tags/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    @tag('post','auth')
    def test_projects_tags_create_auth(self):
        response = self.client.post("/api/projects-tags/",data={"name":"test"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    @tag('patch','auth')  
    def test_add_tags_to_projects_auth(self):
        data = {"tags":[str(self.tag.id)]}
        response = self.client.patch(f"/api/projects/{self.project.id}/",data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data), data)