from django.shortcuts import render, redirect
from django.contrib.auth import *
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def user_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user     = authenticate(username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return redirect('/')
    ctx = {}
    return render(request, 'login.html',ctx)

def user_logout(request):
    logout(request)
    return redirect('/')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
        return redirect("/")
    form = UserCreationForm()
    ctx = {'form': form}
    return render(request, "register.html", ctx)
