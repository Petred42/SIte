from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import *
from django.core.exceptions import ValidationError
from django.db.transaction import commit
from django.forms import ModelForm
from django.forms.fields import EmailField
from django.forms.forms import Form
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import *


class LoginForm(AuthenticationForm):  # форма авторизации
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        "class": "form-input u-form-group u-form-name u-label-top"
    }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        "class": "div-form form-input u-form-group u-label-top"
    }))


class CreateUserForm(UserCreationForm):  # форма создания пользователя
    username = forms.EmailField(label='Почта', min_length=5, max_length=150, widget=forms.TextInput())
    first_name = forms.CharField(label='ФИО', max_length=200, widget=forms.TextInput())
    password1 = forms.CharField( label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError("Пользователь уже существует")
        return username

    # def clean_email(self):
    #     email = self.cleaned_data['email'].lower()
    #     new = User.objects.filter(email=email)
    #     if new.count():
    #         raise ValidationError("Пользователь с таким e-mail уже зарегестрирован")
    #     return email
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name'].lower()
        return first_name

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают", code='invalid')
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.clean_username(),
            self.clean_first_name(),
            self.clean_password2()
        )
        return user

class UserUpdateForm(forms.ModelForm):  # форма редактирования пользователя
    username = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name']


class StudentUpdateForm(forms.ModelForm):  # форма редактирования профиля
    class Meta:
        model = Student
        fields = ['phone_number', 'organization', 'about', 'image']


class ArticleEdit(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'file', 'about', 'date', 'image']
        labels = {
            'title': _('Название Статьи'),
            'date': _('Дата публикации'),
            'about': _('Аннотация статьи'),
            'file': _('Файл со статьей'),
            'image': _('Фотография для статьи'),
        }
        max_length = {
            'title': _(100),
        }
        required = {
            'file': _(False),
            'about': _(False),
        }
        widget = {
            'about': _(forms.Textarea),
            'image': _(forms.ImageField),
            'file': _(forms.FileField),
        }


class EventEdit(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'place', 'address', 'date_start', 'date_end', 'about', 'image']
        labels = {
            'name': _('Название'),
            'place': _('Место'),
            'address': _('Адрес'),
            'date_start': _('Начало мероприятия'),
            'date_end': _('Конец мероприятия'),
            'about': _('Описание мероприятия'),
            'image': _('Фотография'),
        }
        max_length = {
            'name': _(100),
        }
        required = {
            'about': _(False),
        }
        widget = {
            'about': _(forms.Textarea),
            'image': _(forms.ImageField),
            'date_start': _(forms.DateField),
            'date_end': _(forms.DateField),
        }