from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Student)
admin.site.register(Event)
admin.site.register(Article)
admin.site.register(Article_User)
admin.site.register(Event_User)
admin.site.register(Event_Article)