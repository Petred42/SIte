from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from articles import views as user_views
from django.contrib.auth import views as auth_views
from Site import settings

urlpatterns = [
    path('admin/', admin.site.urls),  # админка
    path('main', user_views.main, name='main'),  # главная
    path('log_in', user_views.LoginView.as_view(template_name='log_in.html'), name='log_in'),  # вход
    re_path('log_out', auth_views.LogoutView.as_view(template_name='log_out.html'), name='log_out'),  # выход
    path('register', user_views.register, name='log_in'),  # регистрация
    path('articles/article/<int:pk>/delete', user_views.article_delete, name='article'),  # удаление статьи
    path('articles/article/<int:pk>/edit', user_views.article_edit, name='article_edit'),  # редактирование статьи
    path('articles/article/<int:id>/download', user_views.download_article, name='article_edit'),  # загрузить статью
    path('articles/article/<int:pk>/', user_views.article, name='article'),  # страница статьи
    path('articles/add', user_views.article_add, name='article_add'),  # добавить статью
    path('articles', user_views.articles, name='articles'),  # статьи
    path('events/event/<int:pk>/delete', user_views.event_delete, name='event_delete'),  # удаление конференции
    path('events/event/<int:pk>/edit', user_views.event_edit, name='event_edit'),  # редактирование конференции
    path('events/event/<int:pk>/speakers', user_views.event_speakers, name='event_speakers'),  # список участников
    path('events/event/<int:pk>/take_part/<int:art>', user_views.choose_article),  # подать статью на участие
    path('events/event/<int:pk>/take_part', user_views.take_part),  # выбрать статью для участия
    path('events/event/<int:pk>/', user_views.event, name='event'),  # страница конференции
    path('events/add', user_views.add_event, name='add_event'),  # добавить конференцию
    path('my_events', user_views.my_events, name='my_events'),  # конференции
    path('events', user_views.events, name='events'),  # конференции
    path('profile/edit', user_views.profile_edit, name='profile'),  # редактирование профиля
    path('profile', user_views.profile, name='profile'),  # профиль
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
