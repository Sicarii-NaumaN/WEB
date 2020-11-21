from django.db import models
from django.utils import timezone
from random import choice
from django.contrib.auth.models import User
import operator




class ProfileManager(models.Manager):
    def getByUsername(self, username):
        return self.all().filter()

class LikeManager(models.Manager):
    def get_likes(self, instance):
        return self.filter(value=True, linked_with__pk=instance.pk)

    def get_dislikes(self, instance):
        return self.filter(value=False, linked_with__pk=instance.pk)

    def get_rating(self, instance):
        return self.get_likes(instance).count() - self.get_dislikes(instance).count()

    def check_if_liked(self, instance):
        return self.get_likes(instance).count() > 0

    def check_if_disliked(self, instance):
        return self.get_dislikes(instance).count() > 0


class TagManager(models.Manager):
    def popular_tags(self):
        return self.all()[:10]

    # должен возвращать теги вопроса
    def question_tags(self, question_pk):
        self.filter(question__id=question_pk)
        pass


class ArticleManager(models.Manager):
    def popular_questions(self):
        return self.all()[:10]

    def answers_count(self):
        return Comment.objects.question_answers_count(self.pk)

    def answers(self):
        return Comment.objects.get_answers_by_question_pk(self.pk)

    def with_special_tag(self, tag):
        import logging
        logger = logging.getLogger(__name__)
        logger.error(tag)
        return self.filter(tag__contains=tag)

    def get_likes(self):
        return QuestionLike.objects.get_rating(self)

    def hot(self):
        unordered = self.all()
        ordered = sorted(unordered, key=lambda elem: elem.likes_count(), reverse=True)[:2]
        return ordered

    def get_username(self):
        return self.user.username

class CommentManager(models.Manager):
    def get_all(self):
        return self.all()

    def get_answers_by_question_pk(self, pk):
        return self.filter(article_pk=pk)

    def question_answers_count(self, pk):
        return self.get_answers_by_question_pk(pk).count()

    def get_likes(self):
        return AnswerLike.objects.get_rating(self)



class Article(models.Model):
    title = models.CharField(max_length=1024, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    published = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='Автор')

    tags = models.ManyToManyField('Tag', verbose_name="Теги")
    answers = ArticleManager.answers
    answers_count = ArticleManager.answers_count
    with_special_tag = ArticleManager.with_special_tag
    likes_count = ArticleManager.get_likes
    hot = ArticleManager.hot
    objects = ArticleManager()
    

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

class Comment(models.Model):
    text = models.TextField(verbose_name='Текст')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    date_published = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='Дата публикации')

    right = models.BooleanField(default=False, verbose_name="Ответ является правильным")    


    objects = CommentManager()
    likes_count = CommentManager.get_likes

    def __str__(self):
        return self.text[0:20]

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'



class Tag(models.Model):
    name = models.CharField(unique=True, max_length=30, verbose_name="Название тега")
    def __str__(self):
        return self.name

class Profile(models.Model):
    avatar = models.ImageField(
        verbose_name="Изображение профиля"
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Связанный пользователь")
    objects = ProfileManager()

    def __str__(self):
        return self.objects.user.username

class AnswerLike(models.Model):
    value = models.BooleanField(
        default=True,
        verbose_name="True if like"
    )
    linked_with = models.ForeignKey(
        'Comment',
        on_delete=models.CASCADE,
        verbose_name="Отмеченный ответ"
    )
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Пользователь"
    )
    objects = LikeManager()

    def __str__(self):
        return f"Лайк №{self.pk}"

    class Meta:
        unique_together = ('linked_with', 'user',)


class QuestionLike(models.Model):
    value = models.BooleanField(
        default=True,
        verbose_name="True if like"
    )
    linked_with = models.ForeignKey(
        'Article',
        on_delete=models.CASCADE,
        verbose_name="Отмеченный вопрос"
    )
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Пользователь"
    )
    objects = LikeManager()

    def __str__(self):
        return f"Лайк №{self.pk}"

    class Meta:
        unique_together = ('linked_with', 'user',)