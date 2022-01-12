from django.urls import path
from . import views as vw
from rest_framework.routers import DefaultRouter
    
router = DefaultRouter()

urlpatterns = router.urls

urlpatterns = [
    path('projects/<uuid:id>/showcases/', 
         vw.ShowcaseListCreateView.as_view({"get":"list","post":"create"}),
         name="users-projects-list-create")
]

