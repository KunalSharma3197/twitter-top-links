"""twitter_top_links URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include, url
from django.contrib.auth.views import LoginView as auth_login
from django.contrib.auth.views import LogoutView as auth_logout
from accounts import views as core_views
from twitter_top_links import settings
from toplinks import views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', core_views.home, name='home'),
    url(r'^login/$', auth_login.as_view(), name='login'),
    url(r'^logout/$', auth_logout.as_view(), name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    path('getusertweet/', views.get_user_tweets, name='getusertweet'),
    path('getfriends', views.get_friends, name='getfriends'),
]
