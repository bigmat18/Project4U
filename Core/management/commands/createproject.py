from django.core.management.base import BaseCommand
from Core.models import Project, User

class Command(BaseCommand):

    def handle(self, *args, **options):
        if not Project.objects.filter(name="Project4U").exists():
            try:
                user = User.objects.get(email="project4u@gmail.com")
                Project.objects.create(name="Project4U", creator=user)
            except: print("Non esiste un utente da abbinare al progetto")