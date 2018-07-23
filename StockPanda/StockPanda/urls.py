"""StockPanda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import url

from App import views

urlpatterns = [
    #admin interface
    url('adminforpandas/', admin.site.urls),
    #homepage interface
    url(r'^$', views.home, name='home'),
    #signup interface
    url(r'^signup/$', views.signup, name='signup'),
    #authenticate email interface

    #todo

    #login interface
    url(r'login/$', auth_views.login, {'template_name': '../templates/login.html'} , name = 'login'),
    #logout interface
    url(r'logout/$', auth_views.logout, {'next_page':'/'},name = 'logout'),
    #about interface
    url(r'about/$',views.about, name = "about"),
    #contact interface
    url(r'contact/$',views.contact, name = "contact"),

    #stock/crypto search interface
    url(r'search/$',views.search, name = "search"),
    #overview interface
    url(r'overview/$',views.overview, name = "overview"),
    #portfolios interface
    url(r'portfolios/$',views.portfolios, name = "portfolios"),
    #markets interface
    url(r'markets/$',views.markets, name = "markets"),
    #discover interface
    url(r'discover/$',views.discover, name = "discover"),
    #analyze interface
    url(r'analyze/$',views.analyze, name = "analyze"),
    #account interface
    url(r'account/$',views.account, name = "account")

]
