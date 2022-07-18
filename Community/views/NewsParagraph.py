from rest_framework import viewsets, generics
from ..serializers import NewsParagraphSerializer, NewsParagraphImageSerializer
from Core.models import News, NewsParagraphImage, NewsParagraph, Project
from django.shortcuts import get_object_or_404
from rest_access_policy.access_policy import AccessPolicy
from rest_framework_api_key.permissions import HasAPIKey
from django.conf import settings
from rest_framework.permissions import IsAuthenticated


class NewsParagraphAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": "*",
            "effect": "allow"
        },
        {
            "action": ["create", "update", "partial_update"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_author"
        },
        {
            "action": ["destroy"],
            "principal": "*",
            "effect": "allow",
            "condition": ["is_project_creator","is_author"]
        }
    ]
    
    def is_author(self, request, view, action) -> bool:
        news = view.get_object()
        if isinstance(news, NewsParagraph): news = news.news
        elif isinstance(news, NewsParagraphImage): news = news.paragraph.news
        return (news.author == request.user)
    
    def is_project_creator(self, request, view, action) -> bool:
        paragraph = view.get_object()
        if not isinstance(paragraph, NewsParagraph): paragraph = paragraph.paragraph
        return (paragraph.news.project.creator == request.user)


class NewsParagraphListCreateView(generics.ListCreateAPIView,
                                  viewsets.GenericViewSet):
    """
    list:
    Visualizza la lista di tutti i paragrafi di una news.
    
    Visualizza la lista di tutti i paragrafi di una news inserita nell'url.
    
    create:
    Aggiungi un paragrafo ad una news.
    
    Aggiungi un paragrafo alla news che è stato inserito nell'url. Soltato l'autore può creare un paragrafo.
    """
    serializer_class = NewsParagraphSerializer
    queryset = NewsParagraph.objects.all()
    permission_classes = [IsAuthenticated, NewsParagraphAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_object(self):
        if not hasattr(self, "news"):
            self.news = get_object_or_404(News, id=self.kwargs['id'])
        return self.news
    
    def get_queryset(self):
        return NewsParagraph.objects.filter(news__id=self.kwargs['id'])
    
    def perform_create(self, serializer):
        serializer.save(news=self.news)


class NewsParagraphUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView,
                                    viewsets.GenericViewSet):
    """
    retrieve:
    Visualizza dati di un paragrafo.
    
    Visualizza dati del paragrafo che ha l'id mandato nell'url.
    
    update:
    Aggiorna dati paragrafo.
    
    Aggiorna dati paragrafo. Soltato l'autore può modificare un paragrafo.
    
    partial_update:
    Aggiorna parzialmente dati paragrafo.
    
    Aggiorna parzialmente dati paragrafo. Soltato l'autore può modificare un paragrafo.
    
    destroy:
    Elimina paragrafo.
    
    Elimina paragrafo che ha l'id mandato nell'url. Soltato l'autore ed il creatore del progetto
    possono eliminare un paragrafo.
    """
    serializer_class = NewsParagraphSerializer
    queryset = NewsParagraph.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, NewsParagraphAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    


class NewsParagraphImageCreateView(generics.CreateAPIView,
                                   viewsets.GenericViewSet):
    """
    create:
    Aggiunta di un'immagine ad un paragrafo.
    
    Aggiunge un'immagine con l'opzionale caption ad il paragrafo di cui l'id è nell'url. 
    Soltato l'autore può aggiungere un immagine paragrafo.
    """
    serializer_class = NewsParagraphImageSerializer
    queryset = NewsParagraphImage.objects.all()
    permission_classes = [IsAuthenticated, NewsParagraphAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_object(self):
        if not hasattr(self, "paragraph"):
            self.paragraph = get_object_or_404(NewsParagraph, id=self.kwargs['id'])
        return self.paragraph
    
    def perform_create(self, serializer):
        serializer.save(paragraph=self.paragraph)
    
    
    
class NewsParagraphImageUpdateDeleteView(generics.UpdateAPIView,
                                        generics.DestroyAPIView,
                                        viewsets.GenericViewSet):
    """
    update:
    Aggiorna immagine di un paragrafo.
    
    Aggiorna immagine di un paragrafo, va inserita l'id dell'immagine nell'url. 
    Soltato l'autore può modificare un immagine nel paragrafo.
    
    partial_update:
    Aggiorna parzialemente immagine di un paragrafo.
    
    Aggiorna parzialemente immagine di un paragrafo, va inserita l'id dell'immagine nell'url. 
    Soltato l'autore può modificare un immagine nel paragrafo.
    
    destroy:
    Elimina un immagine da un paragrafo.
    
    Elimina un immagine da un paragrafo, va inserita l'id dell'immagine nell'url. Soltato l'autore ed il creatore del progetto
    possono eliminare un immagine nel paragrafo.
    """
    serializer_class = NewsParagraphImageSerializer
    queryset = NewsParagraphImage.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, NewsParagraphAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    