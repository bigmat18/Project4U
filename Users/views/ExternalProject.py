from rest_framework import mixins, viewsets
from Users.serializers import ExternalProjectSerializer
from Core.models import ExternalProject


class ExternalProjectCUDView(mixins.CreateModelMixin, 
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    """
    create:
    Aggiungi un progetto esterno all'utente
    
    Permette di aggiungere un progetto esterno con il livello all'utente a cui è riferito lo slug nell'url
    
    update:
    Aggiorna i dati di un progetto esterno
    
    Aggiorna i dati della skill, il proggetto da aggiornare viene decisa in base all'id della skill messo nell'url ({skill} = id skill)
    
    destroy:
    Rimuovi un progetto esterno da un utente
    
    Rimuovi un progetto esterno da un utente, il progetto da eliminare viene decisa in base all'id della skill messo nell'url ({skill} = id skill)
    """
    serializer_class = ExternalProjectSerializer
    queryset = ExternalProject.objects.all()
    loockup_filds = "id"

    def get_queryset(self):
        return ExternalProject.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)