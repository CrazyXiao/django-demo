from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def first_page(request):
    return HttpResponse("<p>hello, west.</p>")