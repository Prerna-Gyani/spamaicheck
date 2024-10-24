from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('detect/', views.detect_spam, name='detect_spam'),
    path('spam-listing/', views.spam_website_listing, name='spam_listing'),  
]
