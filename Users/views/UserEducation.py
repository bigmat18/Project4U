from rest_framework import mixins, viewsets
from Users.serializers import UserEducationSerializer
from Core.models import UserEducation

class UserEducationCUDView(mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    
    """
    create:
    Aggiungi un tipo dell'educazione all'utente
    
    Permette di aggiungere un tipo dell'educazione con il livello all'utente a cui è riferito lo slug nell'url
    
    update:
    Aggiorna i dati di un tipo dell'educazione
    
    Aggiorna i dati dell'educazione, l'educazione da aggiornare viene decisa in base all'id della skill messo nell'url ({skill} = id skill)
    
    destroy:
    Rimuovi un tipo dell'educazione da un utente
    
    Rimuovi un tipo dell'educazione da un utente, l'educazione da eliminare viene decisa in base all'id della skill messo nell'url ({skill} = id skill)
    """
    serializer_class = UserEducationSerializer
    queryset = UserEducation.objects.all()
    lookup_field = "id"
    
    def get_queryset(self):
        return UserEducation.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    