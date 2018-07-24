from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

class AccountInformationChangeForm(forms.Form):
    '''
    This form extends django.forms.Form
    It's purpose is to allow the User to change account info
    It is served in the account.html page with AJAX
    '''
    pass
