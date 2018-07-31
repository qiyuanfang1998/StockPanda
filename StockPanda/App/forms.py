from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Portfolio
'''
This subset of forms is for User Sign Up section of the website
'''
class SignUpForm(UserCreationForm):
    '''
    This form extends django.contrib.auth.forms.UserCreationForm
    It adds an email field, and a first name, last name field to
    create a User model from django.contrib.auth.models with those
    attributes.
    '''
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    first_name = forms.CharField(max_length = 30, required = True)
    last_name = forms.CharField(max_length= 150, required = True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2','first_name','last_name')

    def save(self, commit = True):
        user = super(SignUpForm, self).save(commit = False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email is already in use")
        return data

'''
This subset of forms is for the Account Nav Section of the website
'''
class AccountInformationChangeForm(forms.ModelForm):
    '''
    This form extends django.forms.ModelForm
    It's purpose is to allow the User to change account info [email, first name, last name]
    '''

    first_name = forms.CharField(max_length = 30, required = True)
    last_name = forms.CharField(max_length = 150, required = True)
    email = forms.CharField(max_length = 254, required = True, widget = forms.EmailInput())

    class Meta:
        model = User
        fields = ('email','first_name','last_name')        

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AccountInformationChangeForm, self).__init__(*args, **kwargs)


    def save(self, commit = True):
        user = self.request.user
        
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit :
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email = email).exists() and not email == self.request.user.email:
            raise forms.ValidationError("This email is already in use")
        return email

class AccountSecurityChangeForm(forms.Form):
    #deprecated, using built in Django password change form implemented in views.py
    pass

'''
This subset of forms is for the Overview section of the website
'''

'''
This subset of forms is for the Portfolio section of the website
'''

class PortfolioCreationForm(forms.Form):
    '''
    This form extends django.forms.ModelForm
    It's purpose is to allow the User to create a new portfolio with a new unique portfolio name
    '''

    portfolio_name = forms.CharField(max_length = 50, required = True)
    description = forms.CharField(max_length = 250, required = True, widget = forms.Textarea())

    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.superportfolio = self.request.user.superportfolio
        super(PortfolioCreationForm, self).__init__(*args,**kwargs)
    
    def save(self, commit = True):
        #Model validation
        pname = self.cleaned_data['portfolio_name']
        pdescription = self.cleaned_data['description']
        #Model creation and saving
        portfolio = Portfolio(name = pname, description = pdescription, owned_by = self.superportfolio)
        if commit:
            portfolio.save()
        return portfolio

    def clean_name(self):
        pname = self.cleaned_data['portfolio_name']
        if self.superportfolio.portfolios.all().filter(name = pname):
            raise forms.ValidationError("You already have a portfolio with this name")
        return pname 





