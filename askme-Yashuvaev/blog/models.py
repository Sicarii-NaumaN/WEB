from django.db import models
from django.utils import timezone


class Author(models.Model):
    name = models.CharField(max_length=256, verbose_name='Имя')
    birthday = models.DateField(verbose_name='Дата рождения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(is_published=True, date_published__lte=timezone.now())


class Article(models.Model):
    title = models.CharField(max_length=1024, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    date_published = models.DateTimeField(null=True, blank=True, verbose_name='Дата создания')
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    objects = ArticleManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

class Comment(models.Model):
    text = models.TextField(verbose_name='Текст')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    date_published = models.DateTimeField(null=True, blank=True, verbose_name='Дата создания')
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)

    objects = ArticleManager()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'