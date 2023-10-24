from typing import Any, Dict
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView     
from rest_framework.viewsets import ModelViewSet  
from rest_framework.decorators import action 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy 
from django.http import HttpResponse
from rest_framework.views import APIView     
from rest_framework.response import Response 
from django.views.generic import View
from .permissions import *
from .models import *
from .forms import *
from .serializers import *
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect


# Create your views here.

menu = [
    {'title':'Home', 'url':'films:home'},
]

def Home(request):
    data = {
        'title':'Главная',
        'menu':menu,
        'country':Country.objects.all(),
        'genres':Genre.objects.all(),
        'grade':Grade.objects.all(),
        'films':Film.objects.all()
    }
    return render(request, 'films/home.html', context=data)

def genre_f(request, genres_id):
    films = Film.objects.filter(genre_id = genres_id)
    genres = Genre.objects.all()

    data = {
        'films':films,
        'genres':genres,
        'menu':menu,
        'title':'Жанры',
        'genre_id':genres_id
    }
    return render(request, 'films/home.html', context=data)

class FilmSearchView(View):
    template_name = 'films/home.html'

    def post(self, request):
        form = FilmSearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search']    # Получение данных введенных в форму #
            films = Film.objects.filter(title_ru__icontains=search_query)  # Поиск записей в Blog  #
            return render(request, 'films/home.html', {'films':films, 'query':search_query})
        return render(request, self.template_name, {'form':form})

class AddFilm(CreateView):
    form_class = FilmForm
    template_name = 'films/Add-films.html'
    success_url = reverse_lazy('decode_films:home.html')     # Переход после создания блога #

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)

        context['title'] = 'Новый блог'
        context['menu'] = menu

        return context

def delete_film(request, film_id):           
    try:
        film = Film.objects.get(pk=film_id)
        film.delete()
        return redirect('decode_authe:profile')    # Переход после удаления #
    except Film.DoesNotExist:
        return HttpResponse("Film DoesNotExist") 

class EditFilm(UpdateView): 
    model = Film
    form_class = FilmForm
    template_name = 'films/Edit-film.html'  
    success_url = reverse_lazy('films:home')
    
    def get_object(self):
        film_id = self.kwargs['film_id']
        return Film.objects.get(pk=film_id)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    


def films_l(request, film_id, film_name):
    if not request.user.is_authenticated:
        return redirect('authe:signin')

    film = get_object_or_404(Film, pk=film_id, title_ru=film_name)

    # Проверьте, не добавлен ли фильм уже в понравившиеся
    liked_films = LikedFilm.objects.filter(user=request.user, film=film)
    if not liked_films.exists():
        liked_film = LikedFilm(user=request.user, film=film)
        liked_film.save()

    # Обновить список понравившихся фильмов
    user_liked_films = LikedFilm.objects.filter(user=request.user)
    liked_films = [liked_film.film for liked_film in user_liked_films]
 
    # Вернутся на страницу профиля #
    return redirect(reverse('films:home'))

def films_remove(request, film_id, film_name): 
    if not request.user.is_authenticated: 
        return redirect('authe:signin')
    else:
        film = get_object_or_404(Film, pk=film_id, title_ru=film_name)       
        # Удаление фильма из списка понравившихся #

        liked_film = get_object_or_404(LikedFilm, user=request.user, film=film) 
        liked_film.delete()

        # Обновить список #
        user_liked_films = LikedFilm.objects.filter(user=request.user) 
        liked_films = [liked_film.film for liked_film in user_liked_films]

        return redirect(reverse('authe:profile'))

class AddComment(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    template_name = 'films/Add-comment.html'
    success_url = reverse_lazy('films:home')     # Переход после создания продукта #
    
    def form_valid(self, form):
        form.instance.user = self.request.user  # Привязать комментарий к текущему пользователю #
        film_id = self.kwargs.get('film_id')

        if film_id:                                # Связка комментария с определенным блогом #
            form.instance.film_id = film_id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новый комментарий'
        context['menu'] = menu

        return context
    
def delete_comment(request, film_id):           
    try:
        comment = Comment.objects.get(pk=film_id)
        comment.delete()
        return redirect('films:home')   
    except Comment.DoesNotExist:
        return HttpResponse("Comment DoesNotExist") 
 

class ShowComment(DetailView):
    model = Comment                     # Изменено на модель Comment, чтобы отображать комментарии
    template_name = 'decode_films/comment.html'
    pk_url_kwarg = 'comment_id'


    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.none()
        return queryset.filter(film_id=self.film_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обзор комментариев'
        context['film'] = Film.objects.get(id=self.film_id)
        context['menu'] = menu
        return context
    

class FilmDetail(DetailView):
    model = Film
    template_name = 'decode_films/comment.html'
    pk_url_kwarg = 'film_id'
    context_object_name = 'film'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обзор блога'
        context['comments'] = Comment.objects.filter(film_id=self.kwargs['film_id'])  # Комментарии относящиеся к этому блогу #
        context['genre'] = Genre.objects.all()
        context['menu'] = menu
        return context

        # API #
class FilmListAPIView(ListCreateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    # permission_classes = (IsAdminOrReadOnly,)    # Класс для пред доступа #


class FilmDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    # permission_classes = (IsOwnerOrReadOnly,)    # Класс для пред доступа #

# class FilmViewSet(ModelViewSet):
#     queryset = Film.objects.all()
#     serializer_class = FilmSerializer

#     @action(methods=['get'], detail=False)    # ДЛя блогов  #
#     def genres(self, request):
#         genres = Genre.objects.all()
#         return Response([genre.name for genre in genres])
    
#     @action(methods=['get'], detail=False)
#     def genre_filter(self, request):
#         films = Film.objects.filter(genre_id=self.request.query_params.get('genre_id'))   # Для категорий #
#         serializer = FilmSerializer(films, many=True)
#         return Response(serializer.data)



# class FilmApiView(APIView):           
#     def get(self,request):
#         films = Film.objects.all()
#         return Response({'film': FilmSerializer(films, many=True).data})
    
#     def post(self, request):
#         # new_film = Film.objects.create(
#         #     poster = request.data['poster'],
#         #     title_ru = request.data['title_ru'],
#         #     title_orig = request.data['title_orig'],
#         #     prod_year = request.data['prod_year'],
#         #     timing = request.data['timing'],
#         #     premiere_date = request.data['premiere_date'],
#         #     country_id = request.data['country_id'],
#         #     genre_id = request.data['genre_id'],
#         #     director_id = request.data['director_id'],
#         # )

#         # new_film.save()
#         # return Response({'film': FilmSerializer(new_film).data})   # Отправка добавленного фильма #

#         serializer = FilmSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)        # raise_exeption = Отправляет ошибку #
#         serializer.save()

#         return Response({'film':serializer.data})
    
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)

#         if not pk:
#             return Response({'error':'method "Put" not allowed'})
        
#         try:
#             instance = Film.objects.get(pk=pk)

#         except:
#             return Response({'error':'Object does not exist'})
        
#         serializer = FilmSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)        # raise_exeption - Отправляет ошибку #
#         serializer.save()

#         return Response({'film': serializer.data})
    
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)

#         if not pk:
#             return Response({'error':'method "delete" not allowed'})

#         try:
#             instance = Film.objects.get(pk=pk)
#             instance.delete()

#         except:
#             return Response({'error':'Object does not exist'})

#         return Response({'status': 'film was deleted'})



# get - получить инф #
# post - передать данные #
# delete - удалить данные #
# put - Изменить/обновить данные #
# Patch - изменение нескольких данных #