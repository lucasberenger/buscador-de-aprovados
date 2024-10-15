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
    password = forms.CharField(label="Senha" ,widget=forms.PasswordInput(), required=False)

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