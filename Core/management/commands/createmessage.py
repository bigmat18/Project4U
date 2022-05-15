from django.core.management.base import BaseCommand
from Core.models import Project, User, Showcase, Event, TextMessage, Poll
import datetime
from django.utils import timezone

class Command(BaseCommand):

    def handle(self, *args, **options):
        project = Project.objects.all().first()
        for i in range(0,1):
            Showcase.objects.create(project=project, creator=project.creator)
        for el in list(Showcase.objects.all()):
            for i in range(0,1):
                TextMessage.objects.create(text="prova", author=project.creator, showcase=el)
                Event.objects.create(name="prova", started_at=timezone.now(), ended_at=timezone.now() + datetime.timedelta(days=1), 
                                     author=project.creator, showcase=el)
                Poll.objects.create(name="prova", author=project.creator, showcase=el)
                print("messaggi fatti")
            print("---------------bachecha fatta---------------")

        