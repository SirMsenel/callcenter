from django.shortcuts import render,get_object_or_404
from .models import News
from django.db.models import Q

def news_list(request):
    all_news = News.objects.all().order_by('-created_at')  # Tüm haberler
    return render(request, 'news/news_list.html', {'all_news': all_news})


def home(request):
    latest_news = News.objects.all().order_by('-created_at')[:5]  # Son 5 haber
    return render(request, 'news/home.html', {'latest_news': latest_news})


def search(request):
    query = request.GET.get('q')
    results = None
    if query:
        results = News.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )  # Başlık veya içerik içinde arama yap
    return render(request, 'news/search_results.html', {'results': results, 'query': query})

def news_detail(request, id):
    news = get_object_or_404(News, id=id)  # Haber nesnesini al
    return render(request, 'news/news_detail.html', {'news': news})