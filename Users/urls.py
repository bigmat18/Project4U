from django.urls import include, path
from Users.views import UserRetriveView, UserListView, SkillListSerializer, UserSkillCreateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserRetriveView)
router.register('users', UserListView)
router.register('skills', SkillListSerializer)

urlpatterns = [
    # -------- USER ENDPOINTS ------
    path('', include(router.urls)),
    path('users/<slug:slug>/skills/',UserSkillCreateView.as_view({"post":"create"}), name="userskill-create")
    # -------- USER ENDPOINTS ------
]