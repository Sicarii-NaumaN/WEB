from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'index.html', {})

def new_question(request):
	return render(request, 'ask.html', {})

def login_page(request):
	return render(request, 'login.html', {})

def settings_page(request):
	return render(request, 'settings.html', {})
def tags_page(request):
	return render(request, 'tag.html', {})

def register_page(request):
	return render(request, 'register.html', {})

def question_page(request):
	return render(request, 'question.html', {})