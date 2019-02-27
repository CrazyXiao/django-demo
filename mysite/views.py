#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.shortcuts import render

def first_page(request):
    return render(request, 'index.html')
