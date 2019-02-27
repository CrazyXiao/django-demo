from django.shortcuts import render
from django.http import HttpResponse
from west.models import Character
from django import forms
# Create your views here.

def staff(request):
    staff_list = Character.objects.all()
    return render(request, 'templay.html', {'staffs': staff_list})


def first_page(request):
    return HttpResponse("<p>hello, west.</p>")


class CharacterForm(forms.Form):
    name = forms.CharField(max_length = 200)


def investigate(request):
    if request.POST:
        form = CharacterForm(request.POST)
        if form.is_valid():
            submitted  = form.cleaned_data['name']
            new_record = Character(name = submitted)
            new_record.save()
    form = CharacterForm()
    ctx ={}
    all_records = Character.objects.all()
    ctx['staff'] = all_records
    ctx['form']  = form
    return render(request, "investigate.html", ctx)