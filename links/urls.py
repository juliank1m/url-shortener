from django.urls import path
from .views import create_link, redirect_link

urlpatterns = [
    path("api/links/", create_link, name="create_link"),
    path("<str:code>", redirect_link, name="redirect_link"),
]