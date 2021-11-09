from django.urls import include, path
from Users.views import EmailCreateView, UserRetriveView, UserListView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', UserRetriveView)
router.register('', UserListView)

urlpatterns = [
    # -------- USER ENDPOINTS ------
    path('', include(router.urls)),
    # -------- USER ENDPOINTS ------
]