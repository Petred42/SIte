import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Student(models.Model):  # модель профиля
    phone_number = models.CharField(max_length=12, verbose_name="Контактный телефон")
    organization = models.CharField(max_length=50, verbose_name="Учреждение",  null=True, blank=True)
    about = models.TextField(verbose_name="О себе", null=True, blank=True)
    image = models.ImageField(upload_to="photos/", verbose_name="Фото")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Student'


class Event(models.Model):  # модель конференции
    name = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    address = models.TextField(null=True, blank=True)
    date_start = models.DateField(default=timezone.now())
    date_end = models.DateField(default=timezone.now())
    about = models.TextField()
    image = models.ImageField(upload_to="photos/events", verbose_name="Фото")
    user = models.ManyToManyField(User, through="Event_User")


class Article(models.Model):  # модель статьи
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='articles/')
    about = models.TextField(max_length=300, null=True, blank=True)
    date = models.DateField(default=timezone.now())
    image = models.ImageField(upload_to="photos/articles", verbose_name="Фото")
    user = models.ManyToManyField(User, through="Article_User")
    event = models.ManyToManyField(Event, through="Event_Article")


class Article_User(models.Model):  # статья_пользователь
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Event_User(models.Model):  # конференция_пользователь
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_org = models.BooleanField()


class Event_Article(models.Model):  # конференция_статья
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    allowed = models.BooleanField(default=False)