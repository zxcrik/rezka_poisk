from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import response
from rest_framework import mixins
from  .models import *
from .serializer import *
from .forms import *
from films.models import Film, LikedFilm


# Create your views here.
menu = [
    {'title':'Home', 'url':'films:home'},
    {'title':'Description', 'url':'films:category'},
    {'title':'Регистрация', 'url':'authe:signup'},
    {'title':'Вход', 'url':'authe:signin'}
]
class UserDetailAPIView(RetrieveAPIView):
    
    def get_queryset(self):
        return User.objects.get(id=self.request.user.id)
    
class UserViewSet(GenericViewSet, mixins.CreateModelMixin, ):
    def get_queryset(self):
        if self.action == 'retrieve':
            return User.objects.get(id=self.request.user.id)
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'retrieve':
            return UserRetrieveSerializer
        
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance)
        return response(serializer.data)

# Create your views here.

class SignUpUser(CreateView):
    form_class = SignUpUserForm
    template_name = 'authe/signup.html'
    success_url = reverse_lazy('films:home')     # Переход после создания пользователя #

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)

        context['title'] = 'Регистрация'
        context['menu'] = menu

        return context
    
class SignInUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'authe/signin.html'


    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)

        context['title'] = 'Авторизация'
        context['menu'] = menu

        return context
    
    def get_success_url(self):
        return reverse_lazy('films:home')



class UserDetailAPIView(RetrieveAPIView):
    def get_queryset(self):
        return User.objects.get(id=self.request.user.id)
    
class UserViewSet(GenericViewSet, mixins.CreateModelMixin,):
    def get_queryset(self):
        if self.action == 'retrieve':
            return User.objects.get(id=self.request.user.id)
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'retrieve':
            return UserRetrieveSerializer
        
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

def signout_user(request):             # Выход из аккаунта  #
    logout(request)   
    return redirect('authe:signin')     

def profile(request):
    if not request.user.is_authenticated:
        return redirect('authe:signin')
    
    # Список понравившихся фильмов текущего пользователя #
    user_liked_films = LikedFilm.objects.filter(user=request.user)

    # Извлечь фильмы из объектов #
    liked_films = [liked_film.film for liked_film in user_liked_films]

    data = {
        'title': 'Профиль',
        'menu': menu,
        'user_liked_films': liked_films,}
     
    return render(request, 'authe/profile.html', data)




@login_required             # Только зарегистрированные user-ы #
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user) # использование данных user-a для редактирования #
        if form.is_valid():
            form.save()
            return redirect('authe:profile')  
    else:
        form = EditProfileForm(instance=request.user)
    
    return render(request, 'authe/edit-profile.html', {'form': form})