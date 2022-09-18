from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from camhouse.models import Profile, Compte

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control  py-4 ', 'placeholder' : 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control  py-4 ', 'placeholder' : 'mot de passe'}))
    class Meta:
        model = User
        fields = ('username', 'password1')
class UserForm(UserCreationForm): # sa c'est pour l'inscription

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Entrer un nom d\'utilisateur'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Entrer une adresse mail valide'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Entrer un mot de passe'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Confirmer votre mot de passe'}))

    class Meta:
        model= User
        fields = ('username', 'email', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    phonenumber = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'numero de téléphone', 'min': '1'}))

    class Meta:
        model= Profile
        fields = ('phonenumber', 'day', 'pay', 'code')
        widgets = {
            'day': forms.HiddenInput(attrs={'value': '1'}),
            'pay': forms.HiddenInput(attrs={'value': '1'}),
            'code': forms.HiddenInput(attrs={'value': '1'}),
        }

class CompteUser(forms.ModelForm):
    class Meta:
        model = Compte
        fields = ('montant', 'day')
        widgets = {
            'day': forms.HiddenInput(attrs={'value': '1'}),
            'montant': forms.HiddenInput(attrs={'value': '1'})
        }
