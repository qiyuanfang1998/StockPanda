from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

# Create your views here.

def signup(request):
    sign_up_form = UserCreationForm()
    return render(request,'signup.html',{'sign_up_form':sign_up_form})
