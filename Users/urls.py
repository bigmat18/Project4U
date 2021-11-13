from django.urls import include, path
import Users.views as vw
from rest_framework.routers import DefaultRouter
    
    
router = DefaultRouter()
router.register(r'users', vw.UserRetriveView)
router.register(r'users', vw.UserListView)
router.register(r'skills', vw.SkillListView)
router.register(r'user/skills', vw.UserSkillCUDView)
router.register(r'user/external-projects', vw.ExternalProjectCUDView)

urlpatterns = router.urls
