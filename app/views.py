from django.shortcuts import render
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import SignupForm, LoginForm, SearchNameForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Candidato
# Create your views here.


## HomeView do projeto
class HomeView(LoginRequiredMixin, View):
    
    def get(self, request):
        queryset = Candidato.objects.all()
        name = request.GET.get('fullname')
        form = SearchNameForm()

        if name:
            queryset = Candidato.objects.all().filter(name__icontains=name)


        data = { 
            'user': request.user,
            'candidatos': queryset,
            'form': form,
            'name': name,
        }
        return render(request,'home.html', data)       



## View para Cadastro de Usuário
class SignupView(View):

    def get(self, request):
        data = { 'form': SignupForm() }
        return render(request, "signup.html", data)
    
    def post(self, request):
        form = SignupForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            if username and password1 and password2 and password1 == password2:
                user = User.objects.create_user(
                    username = username,
                    password = password1
                )

                if user:
                    return HttpResponseRedirect(reverse('login'))
        
        data = {
            'form': form,
            'error': 'Usuário ou senha inválidos'
        }

        return render(request, 'signup.html', data)

## View para Logar com usuário cadastrado
class LoginView(View):

    def get(self, request):
        data = { 'form': LoginForm() }
        return render(request, 'login.html', data)

    def post(self, request):
        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            
            
        data = {
            'form': form,
            'error': 'Usuário ou senha inválidos'
        }

        return render(request, 'login.html', data)


## View para logout do usuário
class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))

