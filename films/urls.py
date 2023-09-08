from django.urls import path
from . import views

urlpatterns = [
    path('', views.FilmApiView.as_view())
]