from django.shortcuts import render
from django.http import HttpResponse
from west.models import Character

# Create your views here.

def staff(request):
    staff_list = Character.objects.all()
    return render(request, 'templay.html', {'staffs': staff_list})


def first_page(request):
    return HttpResponse("<p>hello, west.</p>")