from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
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