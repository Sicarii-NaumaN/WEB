from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator





# Create your views here.

questions = [
    {
    'id': idx,
     'title': f'title {idx}',
     'text': 'text text',
    } for idx in range(10)
]



def index(request):
	page = paginate(questions, request)
	return render(request, 'index.html', {
		'page_obj' :page,
		}) 

def new_question(request):
	return render(request, 'ask.html', {})

def login_page(request):
	return render(request, 'login.html', {})

def settings_page(request):
	return render(request, 'settings.html', {})
def tags_page(request):
	page = paginate(questions, request, 3)
	return render(request, 'tag.html', {
		'page_obj' : page,
		})

def register_page(request):
	return render(request, 'register.html', {})

def question_page(request, pk):
	question = questions[pk]
	page = paginate(questions, request, 3)
	return render(request, 'question.html', {
		'page_obj' : page,
		})
def paginate(objects_list, request, per_page=2):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page