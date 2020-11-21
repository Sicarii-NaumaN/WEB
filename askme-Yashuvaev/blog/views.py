from django.shortcuts import render
from blog.models import Article
from django.views.generic import ListView
from django.core.paginator import Paginator
from blog.models import Comment




def index(request):
    articles = Article.objects.all()
    page = paginate(articles, request)
    return render(request, 'index.html', {
        'page_obj': page
    })

def new_question(request):
    return render(request, 'ask.html', {})

def login_page(request):
    return render(request, 'login.html', {})

def settings_page(request):
    return render(request, 'settings.html', {})
def tags_page(request):
    articles = Article.objects.all()
    page = paginate(articles, request)
    return render(request, 'tag.html', {
        'page_obj' : page,
        })

def register_page(request):
    return render(request, 'register.html', {})

def question_page(request, pk):
    comments = Comment.objects.filter(article__pk=pk)
    article_conc = Article.objects.get(id = pk)
    
    page = paginate(comments, request)
    return render(request, 'question.html', {
        'page_obj' : page,
        'state': article_conc
        })
def paginate(objects_list, request, per_page=2):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page