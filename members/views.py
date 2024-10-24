# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
import requests

def home(request):
    return render(request, 'mainpg.html')