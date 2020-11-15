from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator


from myapp.models import Contact

# Create your views here.

questions = [
    {
    'id': idx,
     'title': f'title {idx}',
     'text': 'text text',
    } for idx in range(10)

]

def index(request):
	contact_list = Contact.objects.all()
	paginator = Paginator(contact_list, 25)
	page_number = request.GET.get('page')
	questions = paginator.get_page(page_number)
	return render(request, 'index.html', {
		'questions' :questions,
		}) 

def new_question(request):
	return render(request, 'ask.html', {})

def login_page(request):
	return render(request, 'login.html', {})

def settings_page(request):
	return render(request, 'settings.html', {})
def tags_page(request):
	return render(request, 'tag.html', {
		'questions' :questions,
		})

def register_page(request):
	return render(request, 'register.html', {})

def question_page(request, pk):
	question = questions[pk]
	return render(request, 'question.html', {
		'questions' : questions,
		})
def paginate(objects_list, request, per_page=10):
    # do smth with Paginator, etc…
    return page