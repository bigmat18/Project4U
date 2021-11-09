from django.urls import include, path
from Users.views import EmailCreateView, UserRetriveView, UserListView
from rest_framework.routers import DefaultRouter


urlpatterns = [
    # -------- USER ENDPOINTS ------
    path('users/', UserListView.as_view({'get':'list'}), name="users-list"),
    path('users/<slug:slug>/', UserRetriveView.as_view({'get':'get'}), name="user-retrieve"),
    # -------- USER ENDPOINTS ------
]