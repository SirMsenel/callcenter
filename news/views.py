from django.shortcuts import render
from .models import News
from django.db.models import Q

def news_list(request):
    news = News.objects.all().order_by('-created_at')  # Tüm haberleri en yeniye göre sırala
    return render(request, 'news/news_list.html', {'news': news})

def home(request):
    # Son 5 haberi getir
    news = News.objects.all().order_by('-created_at')[:5]  # En yeni 5 haber
    return render(request, 'news/home.html', {'news': news})

def search(request):
    query = request.GET.get('q')
    results = None
    if query:
        results = News.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )  # Başlık veya içerik içinde arama yap
    return render(request, 'news/search_results.html', {'results': results, 'query': query})