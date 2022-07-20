from rest_framework import viewsets, generics
from ..serializers import NewsSerializer, NewsParagraphSerializer, NewsParagraphImageSerializer
from Core.models import News, Project
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_access_policy.access_policy import AccessPolicy
from rest_framework_api_key.permissions import HasAPIKey
from django.conf import settings


class NewsAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["create"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_inside_project"
        },
        {
            "action": ["retrieve"],
            "principal": "*",
            "effect": "allow",
        },
        {
            "action": ["destroy"],
            "principal": "*",
            "effect": "allow",
            "condition": ["is_author", "is_project_creator"]
        },
        {
            "action": ["update", "partial_update"],
            "principal": "*",
            "effect": "allow",
            "condition": ["is_author"]
        },
    ]
    
    def is_inside_project(self, request, view, action) -> bool:
        project = view.get_object()
        return (request.user == project.creator or 
                project.users.filter(id=request.user.id).exists())
        
    def is_author(self, request, view, action) -> bool:
        news = view.get_object()
        return request.user == news.author
    
    def is_project_creator(self, request, view, action) -> bool:
        news = view.get_object()
        return (news.project.creator == request.user)


class NewsCreateView(generics.CreateAPIView,
                     viewsets.GenericViewSet):
    """
    create:
    Crea nuove news all'interno di un progetto.
    
    Crea news all'interno di un progetto a cui partecipi. E' possibile oltre i dati della news mandare anche
    una lista chiamata 'paragraphs' contentente i dati dei paragrafi da aggiungere alla news. All'interno di questa lista si
    può anche inserire 'images' per mandare i dati delle immagini legati al paragrafo. Esempio:
    {
        "dati news": ....
        "paragraphs": [
            {"dati paragrafo1"},
            {
                "dati paragrafo2",
                "images": [
                    {"dati immagine 1"}
                ]
            }
        ]
    }
    """
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    permission_classes = [IsAuthenticated, NewsAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_object(self):
        if not hasattr(self, "project"): 
            self.project = get_object_or_404(Project, id=self.kwargs['id'])
        return self.project
    
    def create(self, request, *args, **kwargs):
        if "paragraphs" in request.data: 
            paragraphs = request.data["paragraphs"]
            del request.data["paragraphs"]
        else: paragraphs = None
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        news = self.perform_create(serializer)
        
        if paragraphs:
            if not isinstance(paragraphs, list):
                news.delete()
                return Response({"Error": "Paragraphs fields must be a list"},
                                status=status.HTTP_400_BAD_REQUEST)
                
            for index, paragraph in enumerate(paragraphs):
                if "images" in paragraph: 
                    images = paragraph['images']
                    del paragraph['images']
                else: images = None
                
                serializer_paragraph = NewsParagraphSerializer(data=paragraph)
                
                try: serializer_paragraph.is_valid(raise_exception=True)
                except Exception as e: news.delete(); raise e
                
                paragraph = serializer_paragraph.save(news=news, order_paragraph=index)
                
                if images:
                    if not isinstance(images,list):
                        news.delete()
                        return Response({"Error": "Images in paragraph fields must be a list"},
                                        status=status.HTTP_201_CREATED)
                    
                    for image in images:
                        serializer_image = NewsParagraphImageSerializer(data=image)
                        
                        try: serializer_image.is_valid(raise_exception=True)
                        except Exception as e: news.delete(); raise e
                        
                        serializer_image.save(paragraph=paragraph)
                        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user,
                                   project=self.get_object())
        return instance


class NewsRUDView(generics.RetrieveUpdateDestroyAPIView,
                  viewsets.GenericViewSet):
    """
    retrieve:
    Vedi dati news.
    
    Dato un id vedi tutti i dati di una news.
    
    update:
    Aggiorna una news.
    
    Aggiorna tutti i dati di una news. Solo l'autore può farlo.
    
    partial_update:
    Aggiorna una news parzialmente.
    
    Aggiorna parzialmente tutti i dati di una news. Solo l'autore può farlo.
    
    destroy:
    Elimina una news.
    
    Elimina una news. Solo l'autore della news ed il creatore del progetto possono farlo.
    """
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, NewsAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)