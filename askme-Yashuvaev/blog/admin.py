from django.contrib import admin
from blog import models

admin.site.register(models.Author)
admin.site.register(models.Article)
admin.site.register(models.Comment)
