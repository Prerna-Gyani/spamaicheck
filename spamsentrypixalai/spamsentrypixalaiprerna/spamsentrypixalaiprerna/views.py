from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
import requests
import os

def home(request):
    return render(request, 'spamsentrypixalaiprerna/mainpg.html')
