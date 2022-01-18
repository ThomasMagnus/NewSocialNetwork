from django import forms
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, PasswordInput, CharField, EmailField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserAuthForm(forms.Form):
    email = CharField(widget=EmailInput(attrs={'class': 'user__data', 'placeholder': 'Введите email..', 'id': 'email'}),
                      label='')
    password = CharField(
        widget=PasswordInput(attrs={'class': 'user__data', 'placeholder': 'Введите пароль..', 'id': 'password'}),
        label='')


class RegisterUserForm(UserCreationForm):
    first_name = CharField(widget=TextInput(attrs={'class': 'user__data', 'placeholder': 'Введите имя..'}), label='')
    last_name = CharField(widget=TextInput(attrs={'class': 'user__data', 'placeholder': 'Введите фамилию..'}), label='')
    username = CharField(widget=TextInput(attrs={'class': 'user__data', 'placeholder': 'Введите логин..'}), label='')
    email = EmailField(widget=EmailInput(attrs={'class': 'user__data', 'placeholder': 'Введите email..'}), label='')
    password1 = CharField(widget=PasswordInput(attrs={'class': 'user__data', 'placeholder': 'Введите пароль..'}),
                          label='')
    password2 = CharField(widget=PasswordInput(attrs={'class': 'user__data', 'placeholder': 'Повторите пароль..'}),
                          label='')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class AuthUserForm(AuthenticationForm):
    username = EmailField(widget=EmailInput(attrs={'class': 'user__data', 'placeholder': 'Введите email..'}), label='')
    password = CharField(widget=PasswordInput(attrs={'class': 'user__data', 'placeholder': 'Введите пароль..'}),
                          label='')

