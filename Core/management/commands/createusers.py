from django.core.management.base import BaseCommand
from Core.models import User

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('--num', type=int)

    def handle(self, *args, **options):
        if options["num"]: num = options["num"]
        else: num = 3 
        for index in range(0,num):
            if not User.objects.filter(email=f"user{index+1}@gmail.com").exists():
                User.objects.create_user(f"user{index+1}@gmail.com", f"user{index+1}", 
                                         f"user-{index+1}", f"user-{index+1}")