from django.test.testcases import TestCase
from django.test import tag
from Core.models import User, UserEducation, Skill, UserSkill, TextMessage, UserProject
from django.db import IntegrityError
from django.utils import timezone
import datetime

from Core.models.Projects.Project import Project
from Core.models.Projects.Showcase import Showcase

@tag("Contraints")
class ConstraintsTestCase(TestCase):
    
    def test_user_date_birth_check(self):
        tommorow_date = datetime.date.today() + datetime.timedelta(days=1)
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email="test@test.com",password="prova123456",
                    first_name="prova",last_name="prova",date_birth=tommorow_date)


    def test_user_education_start_date_check(self):
        tommorow_date = datetime.date.today() + datetime.timedelta(days=1)
        user = User.objects.create_user(email="test@test.com",password="prova123456",
                                        first_name="prova",last_name="prova")
        with self.assertRaises(IntegrityError):
            UserEducation.objects.create(user=user,started_at=tommorow_date,
                                         ended_at=datetime.date.today())
            
            
    def test_skill_level_check(self):
        skill = Skill.objects.create(name="test")
        user = User.objects.create_user(email="test@test.com",password="prova123456",
                                        first_name="prova",last_name="prova")
        with self.assertRaises(IntegrityError):
            UserSkill.objects.create(user=user,skill=skill,level=6)


    def test_project_date_ended_check(self):
        tommorow_date = datetime.date.today() + datetime.timedelta(days=1)
        user = User.objects.create_user(email="test@test.com",password="prova123456",
                                        first_name="prova",last_name="prova")
        with self.assertRaises(IntegrityError):
            Project.objects.create(name="test", creator=user, ended_at=tommorow_date)
           
            
    def test_message_update_at_check(self):
        user = User.objects.create_user(email="test@test.com",password="prova123456",
                                        first_name="prova",last_name="prova")
        project = Project.objects.create(name="test", creator=user)
        showcase = Showcase.objects.get(project=project,name="Generali")
        with self.assertRaises(IntegrityError):
            message = TextMessage.objects.create(text="test", author=user, showcase=showcase)
            message.created_at = timezone.now() + datetime.timedelta(days=1)
            message.save()


    def test_project_update_at_check(self):
        user = User.objects.create_user(email="test@test.com",password="prova123456",
                                        first_name="prova",last_name="prova")
        project = Project.objects.create(name="test", creator=user)
        with self.assertRaises(IntegrityError):
            project.created_at = timezone.now() + datetime.timedelta(days=1)
            project.save()
            
    def test_user_project_update_at_check(self):
        user = User.objects.create_user(email="test@test.com",password="prova123456",
                                        first_name="prova",last_name="prova")
        project = Project.objects.create(name="test", creator=user)
        user = UserProject.objects.get(user=user,project=project)
        with self.assertRaises(IntegrityError):
            user.created_at = timezone.now() + datetime.timedelta(days=1)
            user.save()