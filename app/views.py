from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import SignupForm, LoginForm, SearchNameForm, EditProfileForm, CreateCandidatoForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
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


## View para visualizar Perfil do usuário
class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        data = {
            'user': user,
        }

        return render(request, 'profile.html', data)

## View para editar o Perfil do Usuário
class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = EditProfileForm(instance=request.user)

        data = {
            'form': form,
        }
        return render(request, 'edit_profile.html', data)

    def post(self, request):
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()

            return redirect('profile')

        data = {
            'form': form,
        }

        return render(request, 'edit_profile.html', data)

## View para exibir detalhes dos Candidatos
class DetailsView(LoginRequiredMixin, View):
    def get(self, request, pk):
        candidato = get_object_or_404(Candidato, pk=pk)
        data = {
            'candidato': candidato,
        }
        return render(request, 'details.html', data)

## View para adicionar candidatos
class CreateCandidatoView(LoginRequiredMixin, View):
    def get(self, request):
        form = CreateCandidatoForm()

        data = { 
            'form': form,
        }

        return render(request, 'create_candidato.html', data)

    def post(self, request):
        form = CreateCandidatoForm(data=request.POST)

        if form.is_valid():
            fullname = form.cleaned_data.get('fullname')
            cpf = form.cleaned_data.get('cpf')

            Candidato.objects.create(
                name=fullname,
                cpf=cpf,
            )
        
        data = {
            'form': form,
        }

        return render(request, 'home.html', data)

## View para editar ou excluir candidatos
class EditCandidatoView(LoginRequiredMixin, View):
    def get(self, request, pk):
        candidato = get_object_or_404(Candidato, pk=pk)
        form = CreateCandidatoForm(initial={
            'fullname': candidato.name,
            'cpf': candidato.cpf,
        })

        data = {
            'candidato': candidato,
            'form': form,
        }

        return render(request, 'edit_candidato.html', data)
    
    def post(self, request, pk):
        candidato = get_object_or_404(Candidato, pk=pk)
        form = CreateCandidatoForm(data=request.POST)

        if 'delete' in request.POST:
            candidato.delete()
            messages.success(request, 'Candidato Excluído com Sucesso!')
            return redirect('home')

        if form.is_valid():
            fullname = form.cleaned_data.get('fullname')
            cpf = form.cleaned_data.get('cpf')

            candidato.name=fullname
            candidato.cpf=cpf
            candidato.save()

            messages.success(request, 'Candidato Atualizado com Sucesso!')
            return redirect('home')

        data = {
            'form': form,
            'candidato': candidato,
        }

        return render(request, 'edit_candidato.html', data)