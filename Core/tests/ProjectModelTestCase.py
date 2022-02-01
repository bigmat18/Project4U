from django.test import TestCase
from Core.models import Project, User, Showcase
from django.test import tag

@tag("ProjectModel")
class ProjectModelTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com", password="test123456",
                                             first_name="test", last_name="test")
        self.new_user = User.objects.create_user(email="test2@test.com", password="test123456",
                                             first_name="test", last_name="test")
        self.project = Project.objects.create(name="test", creator=self.user)
    
    def test_project_creation(self):
        self.assertEquals(Showcase.objects.filter(project=self.project,
                                                  name="Generale").exists(),True)
        self.assertEquals(Showcase.objects.filter(project=self.project,
                                                  name="Idee").exists(),True)
        self.assertEquals(self.project.users.filter(id=self.user.id).exists(),True)


    def test_project_update(self):
        Showcase.objects.filter(project=self.project,
                                name="Generale").delete()
        self.project.creator = self.new_user
        self.project.save()
        self.assertEquals(Showcase.objects\
                          .filter(project=self.project,
                                  name="Generale").exists(),True)
        self.assertEquals(self.project.users\
                          .filter(id=self.new_user.id).exists(),True)