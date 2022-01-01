from rest_framework import mixins, viewsets
from Users.serializers import ExternalProjectSerializer
from Core.models import ExternalProject

from rest_framework import status
from rest_framework.response import Response

class ExternalProjectCUDView(mixins.CreateModelMixin, 
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    """
    create:
    Aggiungi un progetto esterno all'utente
    
    Permette di aggiungere un progetto esterno con il livello all'utente a cui è riferito lo slug nell'url.
    Puoi mandare un singolo progetto oppure una lista di progetti usando questo formato:
    [ { dati progetto }, { ... }, ... ]
    L'endponts non ritrona nessun valore.
    ------ Anche se non mostrato è possibili inviare anche un'immagine del progetto ------

    
    update:
    Aggiorna i dati di un progetto esterno
    
    Aggiorna i dati della skill, il proggetto da aggiornare viene decisa in base all'id della skill messo nell'url ({skill} = id skill).
     ------ Anche se non mostrato è possibili aggiornare anche un'immagine del progetto ------
    
    destroy:
    Rimuovi un progetto esterno da un utente
    
    Rimuovi un progetto esterno da un utente, il progetto da eliminare viene decisa in base all'id della skill messo nell'url ({skill} = id skill)
    """
    serializer_class = ExternalProjectSerializer
    queryset = ExternalProject.objects.all()
    loockup_filds = "id"

    def get_queryset(self):
        return ExternalProject.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            return super(ExternalProjectCUDView, self).create(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)