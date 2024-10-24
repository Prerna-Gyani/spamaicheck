# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import SpamDetectionForm
from .models import SpamWebsite
import requests

def home(request):
    return render(request, 'mainpg.html')


def detect_spam(request):
    spam_result = None
    if request.method == 'POST':
        form = SpamDetectionForm(request.POST)
        if form.is_valid():
            website_url = form.cleaned_data['website_url']
            spam_type = form.cleaned_data['spam_type']
            spam_result = check_spam(website_url, spam_type)
    else:
        form = SpamDetectionForm()
    
    return render(request, 'detect_spam.html', {'form': form, 'spam_result': spam_result})


def check_spam(url, spam_type):
    # Simple mock logic for spam detection
    if "spam" in url or spam_type == "phishing":
        return "This website is detected as spam."
    return "This website is not spam."

from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def spam_website_listing(request):
    search_results = []
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        spam_type = request.POST.get('spam_type')
        
        # Combine keyword and spam type for the search
        query = f"{keyword} {spam_type}"
        search_results = google_search(query)

    context = {
        'search_results': search_results,
    }
    return render(request, 'spam_listing.html', context)

def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)

    print(f"Requested URL: {url}")
    print(f"Response Status Code: {response.status_code}")

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    for g in soup.find_all('div', class_='BVG0Nb'):  # Adjust as needed
        title = g.find('h3')
        link = g.find('a')

        if title and link:
            results.append((title.text, link['href']))
            print(f"Found: {title.text} - {link['href']}")

    return results
