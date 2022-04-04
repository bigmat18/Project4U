from django.core.management.base import BaseCommand
from Core.models import User, Skill, UserSkill
from ..scripts.generete_slug import generate_random_string
from django.db import IntegrityError
import random

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('--num', type=int)
        parser.add_argument('--create-skills', type=int)

    def handle(self, *args, **options):
        if options["num"]: num_users = options["num"]
        else: num_users = 3 
        
        if options["create_skills"]: num_skills = options["create_skills"]
        else: num_skills = 0
        
        for index in range(0,num_skills):
            Skill.objects.create(name=f"test-{generate_random_string(length=3)}")
        
        for index in range(0,num_users):
            if not User.objects.filter(email=f"user{index+1}@gmail.com").exists():
                user = User.objects.create_user(f"user{index+1}@gmail.com", f"user{index+1}", 
                                         f"user-{index+1}", f"user-{index+1}")
                if num_skills > 0:
                    for index in range(0,random.randint(0,num_skills)):
                        while True:
                            try: UserSkill.objects.create(skill=Skill.objects.order_by('?').first(),
                                                          user=user,level=random.randint(1,5))
                            except IntegrityError: break