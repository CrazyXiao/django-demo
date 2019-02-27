#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.urls import path
from user import views

urlpatterns = [
    path('', views.user_login),
    path('login/', views.user_login),
    path('logout/', views.user_logout),
    path('register/', views.register),
]