from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

# router = SimpleRouter()     # Работает по viewset #
# router.register(r'', views.FilmViewSet, basename='kino')     

app_name = 'films'

urlpatterns = [
    path('', views.Home, name="home"),
    path('films/<int:genres_id>/', views.genre_f, name="genres"),
    path('search/', views.FilmSearchView.as_view(), name='film-search'), 
    path('add/', views.AddFilm.as_view(), name='add'),
    path('delete_film/<int:film_id>/', views.delete_film, name='delete'), 
    path('edit_film/<int:film_id>/', views.EditFilm.as_view(), name='edit'),
    path('filmsl/<int:film_id>/<str:film_name>/', views.films_l, name='filmsl'),
    path('films_remove/<int:film_id>/<str:film_name>/', views.films_remove, name='films_remove'),


    path('cmadd/', views.AddComment.as_view(), name='cmadd'),
    path('testcommentview/<int:blog_id>/', views.FilmDetail.as_view(), name='comments-category'),
    path('delete_comment/<int:blog_id>/', views.delete_comment, name='delete-comment'), 



    path('api', views.FilmListAPIView.as_view()),
    path('<int:pk>/',views.FilmDetailAPIView.as_view()),
    path('auth/', include('rest_framework.urls')),


    # path('', views.FilmViewSet.as_view({'get':'list'})),
    # path('<int:pk>/',views.FilmViewSet.as_view({'get':'retrieve'}))
    # path('', include(router.urls)),
]