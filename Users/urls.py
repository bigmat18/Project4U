from django.urls import include, path
from Users.subviews.Email import EmailCreateView

urlpatterns = [
    path('email/', EmailCreateView.as_view(), name="email-create"),
]