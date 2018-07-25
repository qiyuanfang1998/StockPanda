from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from .forms import SignUpForm, AccountInformationChangeForm
from django.shortcuts import render_to_response
from django.template import RequestContext

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
    if request.method == 'POST':
        form = AccountInformationChangeForm(request.POST, request = request, initial = {'username': request.user.username , 'first_name': request.user.first_name, 'last_name': request.user.last_name,'email': request.user.email})
        if form.is_valid():
            user = form.save()
            return redirect('account')
    else:
        form = AccountInformationChangeForm(request = request,initial = {'username': request.user.username , 'first_name': request.user.first_name, 'last_name': request.user.last_name,'email': request.user.email})

    return render(request, 'account.html', {'form': form})

#404 view
def view_404(request):
    response = render_to_response('404.html', {},
    context_instance=RequestContext(request))
    response.status_code = 404
    return response



