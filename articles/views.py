from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .utils import DataMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from .models import Student
from .forms import *
from .models import *


def main(request):  # главная страница
    welcome_h2 = "Возможности"
    welcome_about = "Мероприятия, статьи.  Помогаем работать, учиться и находить единомышленников в любом городе."
    # теги блока 3-last-conference
    conference_h2 = "Последние мероприятия"
    conference_a = "все мероприятия"
    conference_a += " >"
    events = list(Event.objects.order_by('-id')[:3])
    # теги блока 3-last-article
    data = {"welcome_h2": welcome_h2, "welcome_about": welcome_about,
            "conference_h2": conference_h2, "conference_a": conference_a, "events": events}
    return render(request, "main.html", context=data)


def event_speakers(request, pk):  # страница участников
    event = get_object_or_404(Event, pk=pk)
    articles = Article.objects.filter(event=event)
    context = {
        'articles': articles,
    }
    return render(request, "event_speakers.html", context)


@login_required
def download_article(request, id):  # загрузка статьи
    obj = Article.objects.get(id=id)
    filename = obj.file.path
    response = FileResponse(open(filename, 'rb'))
    return response


def register(request):  # страница регистрации
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            student = Student.objects.create(
                phone_number="Телефон", organization="Введите учреждение", about="",
                user=form.save(), image="zoro.jpg"
            )  # создание профиля для пользователя
            messages.success(request, f'Вы успешно зарегистрировались. Теперь вы можете войти.')
            return HttpResponseRedirect("log_in")  # перевод на страницу входа
        else:
            mes = form.errors
            messages.success(request, mes)

    form = CreateUserForm()
    context = {
        'form': form
    }
    return render(request, "registration.html", context)


def article_delete(request, pk):  # удаление статьи
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        messages.success(request, f'Ваша статья успешно удалена.')
        return redirect('/articles')
    context = {
        'article': article,
    }
    return render(request, "article_delete.html", context)


def article_edit(request, pk):  # редактирование статьи
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleEdit(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ваша статья успешно обновлена.')
            return HttpResponseRedirect("/articles")
    else:
        form = ArticleEdit(instance=article)
    context = {
        'form': form,
    }
    return render(request, "article_edit.html", context)


def article(request, pk):  # страница информации о статье
    article = get_object_or_404(Article, pk=pk)
    author = get_object_or_404(Article_User, article_id=pk)
    user = get_object_or_404(User, username=author.user_id)
    context = {
        'article': article,
        'author': user
    }
    return render(request, "article.html", context)


@login_required
def take_part(request, pk):  # страница для принятия учатстия
    event = get_object_or_404(Event, pk=pk)
    articles = Article.objects.filter(user=request.user)
    context = {
        'event': event,
        'articles': articles,
    }
    return render(request, "take_part.html", context)


@login_required
def choose_article(request, pk, art):  # страница выбора статьи для участия
    event = get_object_or_404(Event, pk=pk)
    article = get_object_or_404(Article, pk=art)
    if request.method == 'POST':
        con = Event_Article.objects.filter(event_id=pk, article_id=art)
        if con.exists():
            messages.success(request, f'Эта статья уже зарегистрированна. Выберите другую статью')
            return redirect('/events/event/' + str(pk) + '/take_part')
        con = Event_Article.objects.create(article_id=article, event_id=event)
        us = Event_User.objects.create(event_id=event, user_id=request.user, is_org=False)
        messages.success(request, f'Ваша статья успешно зарегистрирована. Вас будут ожидать на мероприятии')
        return redirect('/events/event/' + str(pk))
    context = {
        'event': event,
        'article': article,
    }
    return render(request, "choose_article.html", context)


@login_required
def article_add(request):  # добавление статьи
    if request.method == 'POST':
        form = ArticleEdit(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            user = User.objects.filter(username=request.user)
            obj.save()
            obj.user.set(user)
            obj.save()
            messages.success(request, f'Ваша статья успешно добавлена.')
            return redirect('/articles')
        else:
            mes = form.errors
            messages.success(request, mes)
    else:
        form = ArticleEdit(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, "article_add.html", context)


@login_required
def articles(request):  # список статей
    article = Article.objects.filter(user=request.user)
    context = {
        'articles': article,
    }
    return render(request, "select_article.html", context)


@login_required
def event_delete(request, pk):  # удаление мероприятия
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, f'Ваше мероприятие успешно удалено')
        return redirect('/events')
    context = {
        'event': event,
    }
    return render(request, "event_delete.html", context)


@login_required
def event_edit(request, pk):  # редактирование события
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventEdit(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f'Вашe мероприятие успешно обновлена.')
            return HttpResponseRedirect("/events")
    else:
        form = EventEdit(instance=event)
    context = {
        'form': form,
    }
    return render(request, "event_edit.html", context)


def event(request, pk):  # страница информации о конференции
    event = get_object_or_404(Event, pk=pk)
    orgs = User.objects.filter(event_user__event_id_id=pk, event_user__is_org="True")
    stud = Student.objects.get(user__username=orgs[0])
    try:
        org = Event_User.objects.get(event_id=pk, user_id=request.user, is_org=True)
        context = {
            'event': event,
            'stud':stud,
            'orgs': orgs,
            'org': org,
        }
    except Exception:
        context = {
            'event': event,
            'stud': stud,
            'orgs': orgs,
        }
    return render(request, "conference.html", context)


@login_required
def add_event(request):   # добавить событие
    if request.method == 'POST':
        form = EventEdit(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            user = User.objects.filter(username=request.user)
            obj.save()
            obj.user.set(user, through_defaults={"is_org": True})
            obj.save()
            messages.success(request, f'Ваше мероприятие успешно добавлено.')
            return redirect('/events')
        else:
            mes = form.errors
            messages.success(request, mes)
    else:
        form = EventEdit(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, "add_event.html", context)


def events(request):  # список событий
    events = Event.objects.all()
    context = {
        'events': events,
    }
    return render(request, "select_conference.html", context)


@login_required
def my_events(request):  # мои события
    events = Event.objects.filter(user=request.user)
    context = {
        'events': events
    }
    return render(request, "select_conference.html", context)


@login_required
def profile_edit(request):  # редактировать профиль
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = StudentUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.student)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Ваш профиль успешно обновлен.')  # сообщение об успехе
            return redirect('profile')  # перевод на страницу профиля
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = StudentUpdateForm(instance=request.user.student)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, "edit_profile.html", context)


@login_required
def profile(request):  # страница профиля
    stud = Student.objects.get(user=request.user)
    if stud.phone_number == "Телефон":  # перевод на страницу редактирования профиля
        return HttpResponseRedirect("/profile/edit")
    # теги блока 3-last-conference
    conference_h2 = "Последние мероприятия"
    conference_a = "Мои мероприятия"
    conference_a += " >"
    events = Event.objects.filter(user=request.user).distinct().order_by('-id')[:3]
    # теги блока 3-last-article
    article_h2 = "Последние статьи"
    article_a = "все статьи"
    article_a += " >"
    articles = Article.objects.filter(user=request.user).order_by('-id')[:3]  # Нужно ограничить до 3 элементов
    data = {"conference_h2": conference_h2, "conference_a": conference_a, "events": events,
            "article_h2": article_h2, "article_a": article_a, "articles": articles}
    return render(request, "profile.html", context=data)


class LoginUser(DataMixin, LoginView):  # класс для авторизации пользователя
    form_class = LoginForm
    template_name = 'log_in.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Вход")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('profile')