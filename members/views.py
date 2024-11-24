from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from .forms import SpamDetectionForm
from .models import SpamWebsite
import pandas as pd
import joblib
import os
import io
import base64
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for Matplotlib



def home(request):
    """Render the home page."""
    return render(request, 'mainpg.html')

def detect_spam(request):
    """Check if a given URL is malicious."""
    spam_result = None
    if request.method == 'POST':
        form = SpamDetectionForm(request.POST)
        if form.is_valid():
            website_url = form.cleaned_data['website_url']
            # Check URL against the malicious dataset
            spam_result = check_spam(website_url)
    else:
        form = SpamDetectionForm()
    
    return render(request, 'detect_spam.html', {'form': form, 'spam_result': spam_result})

def check_spam(url):
    """Check if the URL is in the malicious URLs dataset or predicted malicious by the model."""
    if url.lower() in df['url_lower'].values:
        return "This website is detected as malicious."
    
    # Use the model for prediction
    vectorized_input = vectorizer.transform([url])
    prediction = model.predict(vectorized_input)[0]
    probability = model.predict_proba(vectorized_input)[0][1]

    if prediction == 1:
        return f"This website is likely malicious. Confidence: {round(probability * 100, 2)}%"
    return "This website is not malicious."


# Base directory setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the malicious URLs dataset
DATASET_PATH = os.path.join(BASE_DIR, 'malicious_urls.csv')
df = pd.read_csv(DATASET_PATH)

# Preprocess dataset for efficient search
df['url_lower'] = df['url'].str.lower()
urls_by_type = {
    'phishing': df[df['type'] == 'phishing'],
    'malware': df[df['type'] == 'malware'],
    'defacement': df[df['type'] == 'defacement'],
    'benign': df[df['type'] == 'benign']
}

# Load pre-trained model and vectorizer
VECTOR_PATH = os.path.join(BASE_DIR, 'vectorizer.pkl')
MODEL_PATH = os.path.join(BASE_DIR, 'malicious_url_model.pkl')
vectorizer = joblib.load(VECTOR_PATH)
model = joblib.load(MODEL_PATH)


def generate_word_cloud(dataframe, colormap='Paired'):
    """Generate a WordCloud image and return it as a base64 string."""
    text = " ".join(url for url in dataframe['url'])
    
    # Generate word cloud
    wordcloud = WordCloud(width=1600, height=800, colormap=colormap).generate(text)
    
    # Save to buffer
    buffer = io.BytesIO()
    plt.figure(figsize=(8, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close()  # Close the figure explicitly to free resources
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    return base64.b64encode(image_png).decode('utf-8')


def generate_pie_chart(dataframe):
    """Generate a pie chart of URL types and return it as a base64 string."""
    type_counts = dataframe['type'].value_counts()
    buffer = io.BytesIO()
    plt.figure(figsize=(8, 6))
    type_counts.plot.pie(
        autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors, labels=type_counts.index
    )
    plt.title("URL Type Distribution")
    plt.ylabel('')
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')


def spam_website_listing(request):
    """Search for malicious URLs and display results with visualizations."""
    search_results = None  # Changed from empty list to None for clarity
    keyword = None
    wordclouds = {}
    pie_chart = None

    if request.method == 'POST':
        keyword = request.POST.get('keyword', '').strip().lower()
        if keyword:
            # Search for URLs matching the keyword
            filtered_df = df[df['url_lower'].str.contains(keyword)]
            # Limit to 10 results
            search_results = filtered_df[['url', 'type']].head(10).to_dict(orient='records') if not filtered_df.empty else []

            # AJAX response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'search_results': search_results, 'keyword': keyword})

    # Generate word clouds for each type
    for type_name, type_df in urls_by_type.items():
        wordclouds[type_name] = generate_word_cloud(type_df)

    # Generate pie chart
    pie_chart = generate_pie_chart(df)

    context = {
        'search_results': search_results,
        'keyword': keyword,
        'wordclouds': wordclouds,
        'pie_chart': pie_chart,
    }
    return render(request, 'spam_listing.html', context)
