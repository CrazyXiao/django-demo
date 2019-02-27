#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.urls import path
from west import views

urlpatterns = [
    path('', views.first_page),
    path('staff/', views.staff),
    path('investigate/', views.investigate),
]