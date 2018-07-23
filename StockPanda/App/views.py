from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from .forms import SignUpForm

# home-splashpage view
def home(request):
    if request.user.is_authenticated:
        return render(request,'overview.html')
    else:
        return render(request,'home.html')

#sign up view
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('overview')
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

#search page view
def search(request):
    return render(request,'search.html')

#overview page view
def overview(request):
    return render(request,'overview.html')

#portfolios page view
def portfolios(request):
    return render(request,'portfolios.html')

#markets page view
def markets(request):
    return render(request,'markets.html')

#discover page view
def discover(request):
    return render(request,'discover.html')

#analyze
def analyze(request):
    return render(request,'analyze.html')

#account
def account(request):
    return render(request,'account.html')



