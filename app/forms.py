from django import forms
from django.contrib.auth.models import User

class SignupForm(forms.Form):
    username = forms.CharField(label= "Usuário")
    password1 = forms.CharField(label = "Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label = "Confirme sua Senha", widget=forms.PasswordInput)
    
class LoginForm(forms.Form):
    username = forms.CharField(label= "Usuário")
    password = forms.CharField(label = "Senha", widget=forms.PasswordInput)
    
class SearchNameForm(forms.Form):
    fullname = forms.CharField(label="Nome e Sobrenome do Candidato")

class EditProfileForm(forms.ModelForm):
    password = forms.CharField(label="Senha",
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'style': 'width: 300px;'
                               }), required=False)

    class Meta:
        model = User
        fields = ["username","first_name", "last_name", "email", "password"]
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password']) 
        if commit:
            user.save()
        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome de usuário',
            'style': 'width: 300px;'
        })
        self.fields['first_name'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Primeiro nome',
            'style': 'width: 300px;'
        })
        self.fields['last_name'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sobrenome',
            'style': 'width: 300px;'
        })
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'E-mail',
            'style': 'width: 300px;'
        })

class CreateCandidatoForm(forms.Form):
    fullname = forms.CharField(label="Nome", 
                               max_length=100, 
                               required=True,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Nome Completo', 
                                   'style': 'width: 300px;', 
                                   'class': 'form-control'
                                   }))
    
    cpf = forms.CharField(label="CPF", 
                          max_length=11, 
                          required=True,
                          widget=forms.TextInput(attrs={
                              'placeholder': 'Apenas Números', 
                              'style': 'width: 300px;', 
                              'class': 'form-control'
                              }))

class UploadXlsForm(forms.Form):
    archive = forms.FileField(
        label="Se preferir, você pode cadastrar os candidatos via planilha EXCEL",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'type': 'file',
            'style': 'width: 400px;'
        }))