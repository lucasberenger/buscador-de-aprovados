from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import SignupForm, LoginForm, SearchNameForm, EditProfileForm, CreateCandidatoForm, UploadXlsForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Candidato
from .utils import add_candidatos_from_xls
# Create your views here.


## HomeView do projeto
class HomeView(LoginRequiredMixin, ListView):
    
    model = Candidato
    template_name = 'home.html'
    context_object_name = 'candidatos'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset() 
        name = self.request.GET.get('fullname')  

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchNameForm()
        context['name'] = self.request.GET.get('fullname')
        return context   



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
        upload_form = UploadXlsForm()
        data = { 
            'form': form,
            'upload_form': upload_form,
        }

        return render(request, 'create_candidato.html', data)

    def post(self, request):
        form = CreateCandidatoForm(request.POST)

        if form.is_valid():
            fullname = form.cleaned_data.get('fullname')
            cpf = form.cleaned_data.get('cpf')

            Candidato.objects.create(
                name=fullname,
                cpf=cpf,
            )

            return redirect('home')

        if 'upload_file' in request.POST:
            upload_form = UploadXlsForm(request.POST, request.FILES)

            if upload_form.is_valid():
                archive = upload_form.cleaned_data.get('archive')
                if archive:
                    add_candidatos_from_xls(archive)

            return redirect('home')
        
        form = CreateCandidatoForm(request.POST)

        data = {
            'form': form,
            'upload_form': upload_form,
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