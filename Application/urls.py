from django.urls import path, include
from django.conf.urls import url
from .views import homepageView

urlpatterns = [
   path("", homepageView, name="homepage"),
] 