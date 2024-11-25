from django.shortcuts import render,get_object_or_404
from .models import News
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.views.generic import ListView
from .models import Article
from django.db.models import Count
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Photo,PhotoComment
from .forms import PhotoCommentForm


def home(request):
   
    news_list = News.objects.all().order_by('-created_at')[:5] # Son 5 haberi alıyoruz
    article_list = Article.objects.all().order_by('-created_at')[:4]  # Son 4 makale
    # En çok yorum alan makaleyi bul
    most_commented_article = (
        Article.objects.annotate(annotated_comment_count=Count('comments'))
        .order_by('-annotated_comment_count')
        .first()
    )
    gallery_photos = Photo.objects.all().order_by('-uploaded_at')[:5]  # Galeri için fotoğrafları getiriyoruz (Son 5 fotoğraf)
    
    return render(request, 'news/home.html', {'news_list': news_list,
                                              'article_list' : article_list,
                                              'most_commented_article': most_commented_article,
                                              'gallery_photos': gallery_photos})

def search(request):
    query = request.GET.get('q')
    results = None
    if query:
        results = News.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )  # Başlık veya içerik içinde arama yap
    return render(request, 'news/search_results.html', {'results': results, 'query': query})


def news_list(request):
    all_news = News.objects.all().order_by('-created_at')  # Tüm haberler
    return render(request, 'news/news_list.html', {'all_news': all_news})


def news_detail(request, id):
    news = get_object_or_404(News, id=id)  # Haber nesnesini al
    return render(request, 'news/news_detail.html', {'news': news})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hoş geldiniz {username}! Kayıt işleminiz tamamlandı.')
            return redirect('login')  # Kayıt olduktan sonra giriş sayfasına yönlendir
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})



def article_list(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 5)  # Her sayfada 5 makale
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/article_list.html', {'articles': page_obj})


def article_detail(request, id):
    # ID'ye göre makaleyi getir, yoksa 404 hatası döndür
    article = get_object_or_404(Article, id=id)
    context = {
        'article': article
    }
    return render(request, 'news/article_detail.html', context)

#galeri
def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'news/photo_list.html', {'photos': photos})

def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'news/photo_detail.html', {'photo': photo})

@login_required
def like_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.user in photo.likes.all():
        photo.likes.remove(request.user)  # Beğeniyi kaldır
    else:
        photo.likes.add(request.user)  # Beğeniyi ekle
    return redirect('photo_detail', pk=pk)

# Fotoğraf yorumlarını listeleme ve yeni yorum ekleme
def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    comments = photo.comments.all()  # Fotoğrafa ait tüm yorumlar
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PhotoCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.photo = photo
                comment.user = request.user
                comment.save()
                return redirect('photo_detail', pk=pk)
        else:
            return redirect('login')  # Kullanıcı giriş yapmadıysa giriş sayfasına yönlendir
    else:
        form = PhotoCommentForm()
    return render(request, 'news/photo_detail.html', {'photo': photo, 'comments': comments, 'form': form})

# Yorum silme
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(PhotoComment, id=comment_id)
    if comment.user == request.user:
        comment.delete()  # Yalnızca yorumu yapan kullanıcı silebilir
    return redirect('photo_detail', pk=comment.photo.pk)