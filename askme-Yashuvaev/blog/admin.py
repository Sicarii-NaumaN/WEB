from django.contrib import admin
from blog import models

admin.site.register(models.Profile)
admin.site.register(models.Article)
admin.site.register(models.Comment)
admin.site.register(models.AnswerLike)
admin.site.register(models.QuestionLike)
admin.site.register(models.Tag)
