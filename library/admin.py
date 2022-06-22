from django.contrib import admin

# Register your models here.
from library import models

admin.site.register(models.user)
admin.site.register(models.books)
