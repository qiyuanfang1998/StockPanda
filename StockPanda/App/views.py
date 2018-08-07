from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from .forms import SignUpForm
from .forms import AccountInformationChangeForm
from .forms import PortfolioCreationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.http import Http404

#importing stocklib
from App.stocklib import stockinfo


#importing all the models from our db. Wildcard import shouldn't create any issues.
from .models import *

# home-splashpage view
def home(request):
    '''
    Redirect to home.html if user is not auth, overview.html if user is authenticated
    '''
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

#user name validation   -- not working , not used currently for ajax val
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)

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

#stock page view
def stock(request, pk):
    try:
        stock = Stock.objects.get(pk = pk)
        realtime_data = stockinfo.realtime_price(stock.symbol)
        stock_logo_String = stock.website[11:]
        return render(request,'stock.html',{'stock': stock, 'logostring' : stock_logo_String, 'realtime_data': realtime_data})
    except Stock.DoesNotExist:
        raise Http404()


#overview page view
def overview(request):
    user = request.user
    superportfolio = user.superportfolio
    return render(request,'overview.html' ,{'superportfolio': superportfolio})

#portfolios page view
    #default view -- no specific portfolio
def portfolios(request):
    user = request.user
    username = user.username
    portfolios = user.superportfolio.portfolios.all()
    return render(request, 'portfolios.html', {'username' : username, 'portfolios': portfolios})

def new_portfolio(request):
    if request.method == 'POST':
        form = PortfolioCreationForm(request.POST, request = request)
        if form.is_valid():
            portfolio = form.save()
            messages.success(request, 'New Portfolio was succesfully created')
            return redirect('portfolios')
        else:
            messages.error(request, 'Portfolio creation encountered an error')
    else:
        form = PortfolioCreationForm(request = request)

    return render(request,'portfolios_new.html',{'form':form})

def portfolios_view(request, pk):
    portfolio =  get_object_or_404(Portfolio, pk=pk)
    if portfolio.owned_by.owned_by == request.user:
        return render(request,'portfolios_view.html',{'portfolio' : portfolio})
    else:
        raise Http404()

#markets page view
def markets(request):
    return render(request,'markets.html')

#discover page view
def discover(request):
    return render(request,'discover.html')

#analyze
def analyze(request):
    return render(request,'analyze.html')

#account-information
def account(request):
    if request.method == 'POST':
        form = AccountInformationChangeForm(request.POST, request = request, initial = {'username': request.user.username , 'first_name': request.user.first_name, 'last_name': request.user.last_name,'email': request.user.email})
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your Account information was succesfully updated')
            return redirect('account')
        else:
            messages.error(request, 'Account information update failed. Please try again')            
    else:
        form = AccountInformationChangeForm(request = request,initial = {'username': request.user.username , 'first_name': request.user.first_name, 'last_name': request.user.last_name,'email': request.user.email})

    return render(request, 'account.html', {'form': form})
#account-security -- using built in Django PasswordChangeForm instead of previously used self defined form in forms.py
def account_security(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('security')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account.html', {'form': form})

#404 view
def view_404(request):
    response = render_to_response('404.html', {},
    context_instance=RequestContext(request))
    response.status_code = 404
    return response



