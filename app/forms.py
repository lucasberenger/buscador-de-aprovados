from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(label= "Usuário")
    password1 = forms.CharField(label = "Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label = "Confirme sua Senha", widget=forms.PasswordInput)
    
class LoginForm(forms.Form):
    username = forms.CharField(label= "Usuário")
    password = forms.CharField(label = "Senha", widget=forms.PasswordInput)
    
class SearchNameForm(forms.Form):
    fullname = forms.CharField(label="Nome e Sobrenome do Candidato")