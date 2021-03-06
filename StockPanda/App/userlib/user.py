from django.contrib.auth.models import User 
from App.models import *

'''
This module is for User related functions
Module functions:
new_user(username,email,password) :- returns a new User, params: username, email, password
user_superportfolio(User) :- returns superportfolio of user, params: User
user_portfolios(User) :- returns queryset of User portfolios, params: User
new_portfolio(User) :- creates new portfolio for User, params: User

'''

#shell use only
def test_auth(username,password):
    user = authenticate(username = username, password = password)
    if user is not None:
        print("Authenticated")
    else:
        print("User does not exist")

#for shell use only
def test_new_user(username,email,password):
    user = User.objects.create_user(username,email,password)
    user.save()

#production use
def change_password(User,new_password):
    User.set_password(new_password)
    User.save()


def get_user_superportfolio(User):
    return 








