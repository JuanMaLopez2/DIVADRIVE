from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def home (request):
    #return HttpResponse('<h1>Welcome to DivaDrive</h1>')
    return render(request, 'home.html')