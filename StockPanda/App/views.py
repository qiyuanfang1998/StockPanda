from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from .forms import SignUpForm

# home-splashpage view
def home(request):
    return render(request,'home.html')

#sign up view
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

#login, logout using default django views

#about page view

def about(request):
    return render(request,'about.html')

#contact page view
def contact(request):
    return render(request,'contact.html')


