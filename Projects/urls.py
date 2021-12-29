from django.urls import path
import Projects.views as vw
from rest_framework.routers import DefaultRouter
    
router = DefaultRouter()
router.register(r"projects", vw.ProjectsListCreateView)
router.register(r"projects", vw.ProjectsRUDView)

urlpatterns = router.urls
