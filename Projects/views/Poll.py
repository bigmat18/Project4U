from rest_framework import generics, viewsets
from rest_framework.views import APIView
from ..serializers import PollWriteSerializer, PollOptionSerializer
from Core.models import Poll, PollOption, Showcase
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_access_policy import AccessPolicy
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from django.conf import settings


class PollAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["create"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_inside_showcase"
        },
        {
            "action": ["update","partial_update","destroy"],
            "principal": "*",
            "effect": "allow",
            "condition": ["is_author"]
        }
    ]
    
    def is_author(self, request, view, action) -> bool:
        poll = view.get_object()
        return request.user == poll.author
        
    def is_inside_showcase(self, request, view, action) -> bool:
        showcase = view.get_object()
        return (request.user == showcase.creator or 
                showcase.users.filter(id=request.user.id).exists())
        
        

class PollOptionAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["create","destroy","update","partial_update"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_author"
        }
    ]
    
    def is_author(self, request, view, action) -> bool:
        poll = view.get_object().poll
        return request.user == poll.author



class PollCreateView(generics.CreateAPIView,
                     viewsets.GenericViewSet):
    """
    create:
    Crea un nuovo sondaggio.
    
    Crea un nuovo messaggio di tipo sondaggio nella bacheca nella quale è stato messo l'id.
    Soltato coloro che sono all'interno dalla bacheca possono creare un sondaggio.
    Di default colore che votano il sondaggio NON sono anonimi.
    """
    serializer_class = PollWriteSerializer
    permission_classes = [IsAuthenticated, PollAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_object(self):
        return get_object_or_404(Showcase, id=self.kwargs['id'])
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            if "options" in request.data:
                for option_text in dict(request.data)["options"]:
                    poll = get_object_or_404(Poll,id=response.data['id'])
                    PollOption.objects.create(text=option_text,poll=poll)
        return response
    
    def perform_create(self, serializer):
        instance = serializer.save(showcase=self.get_object(), 
                                   type_message = "POLL",
                                   author=self.request.user)
        instance.viewed_by.add(self.request.user)



class PollUpdateDestroyView(generics.UpdateAPIView,
                            generics.DestroyAPIView,
                            viewsets.GenericViewSet):
    """
    update:
    Aggiorna un sondaggio.
    
    Aggiorna il sondaggio del quale è stato mandato l'id. Soltato il creatore
    del sondaggio può modificare il sondaggio.
    
    partial_update:
    Aggiorna un sondaggio.
    
    Aggiorna il sondaggio del quale è stato mandato l'id. Soltato il creatore
    del sondaggio può modificare il sondaggio.
    
    destroy:
    Elimina il sondaggio.
    
    Elimini il sondaggio di cui è stato mandato l'id nell'url. Soltato l'autore del
    sondaggio lo può eliminare.
    """
    serializer_class = PollWriteSerializer
    queryset = Poll.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, PollAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    

class PollOptionCreateView(generics.CreateAPIView,
                           viewsets.GenericViewSet):
    """
    create:
    
    Crea una opzione di un sondaggio.
    
    Crea una nuova opzione da vontare dentro il sondaggio di cui è stato mandato l'id nell'url.
    Soltato il creatore del sondaggio può creare una opzione da votare.
    """
    serializer_class = PollOptionSerializer
    permission_classes = [IsAuthenticated, PollOptionAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_object(self):
        return get_object_or_404(Poll, id=self.kwargs['id'])
    
    def perform_create(self, serializer):
        serializer.save(poll=self.get_object())
        


class PollOptionUpdateDestroyView(generics.UpdateAPIView,
                                  generics.DestroyAPIView,
                                  viewsets.GenericViewSet):
    """
    update:
    Aggiorna una opzione di scelta di una votazione.
    
    Aggiorna una opzione di scelta di una votazione, aggioni l'opzione del quale è 
    stato mandato l'id nell'url. Soltato il creatore del sondaggio può agiornare la votazione.
    
    partial_update:
    Aggiorna una opzione di scelta di una votazione.
    
    Aggiorna una opzione di scelta di una votazione, aggioni l'opzione del quale è 
    stato mandato l'id nell'url. Soltato il creatore del sondaggio può agiornare la votazione.
    
    destroy:
    Elimina un opzione sondaggio.
    
    Elimina l'opzione sondaggio il quale è stato mandato l'id nell'url. Soltato il creatore
    del sondaggio può eliminare un opzione.
    """
    serializer_class = PollOptionSerializer
    queryset = PollOption.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, PollOptionAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    
class PollOptionVotesAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        """
        Questo endpoints serve per quando un utente clicca per votare un opzione del sondaggio ad aggiunere
        il voto dell'utente che manda la richiesta. Quando viene aggiunto il voto si controlla automanticamente se ci sono
        voti già dati di quell'utente in quel sondaggio e nel caso lo rimuove.
        Soltato colore che si trovano dentro la bacheca possono effetuare questa operazione.
        """
        option = self.kwargs['id']
        option = get_object_or_404(PollOption, id=option)
        if not (option.poll.showcase.users.filter(id=request.user.id).exists() or 
                option.poll.showcase.creator == request.user):
            return Response(status=status.HTTP_403_FORBIDDEN)
        if PollOption.objects.filter(votes=request.user, poll=option.poll).exists():
            PollOption.objects.get(votes=request.user, poll=option.poll).votes.remove(request.user)    
        option.votes.add(self.request.user)
        return Response(status=status.HTTP_200_OK)