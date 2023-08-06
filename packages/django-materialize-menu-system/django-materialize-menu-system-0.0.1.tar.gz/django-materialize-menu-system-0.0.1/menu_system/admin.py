from django.contrib import admin

from .models import Menu, App, Social, UserLink

# Register your models here.
admin.site.register(UserLink)
admin.site.register(Menu)
admin.site.register(App)
admin.site.register(Social)